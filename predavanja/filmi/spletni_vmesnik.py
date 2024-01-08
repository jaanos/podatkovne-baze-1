#
#   Spletni vmesnik 
#   za delo z bazo filmi.sqlite
#
#   J. Vidali, dec. 2023
#

import bottle
import json
from functools import wraps
from model import Film, Oseba, Uporabnik


SKRIVNOST = 'nekaj, kar bo zelo težko uganiti!!!! djnskfndkjfnsd'


def nastavi_sporocilo(sporocilo, piskotek='sporocilo'):
    """
    Nastavi piškotek s sporočilom.
    """
    bottle.response.set_cookie(piskotek, sporocilo, secret=SKRIVNOST, path='/')


def preberi_sporocilo(piskotek='sporocilo'):
    """
    Preberi sporočilo in pobriši pripadajoči piškotek.
    """
    sporocilo = bottle.request.get_cookie(piskotek, secret=SKRIVNOST)
    bottle.response.delete_cookie(piskotek, path='/')
    return sporocilo


def nastavi_obrazec(piskotek, obrazec):
    """
    Zapiši vrednosti obrazca v obliki slovarja v piškotek kot niz JSON.
    """
    nastavi_sporocilo(json.dumps(obrazec), piskotek)


def preberi_obrazec(piskotek):
    """
    Preberi vrednosti obrazca in pobriši pripadajoči piškotek.
    """
    try:
        return json.loads(preberi_sporocilo(piskotek))
    except (TypeError, json.JSONDecodeError):
        return {}


def prijavljeni_uporabnik():
    """
    Vrni prijavljenega uporabnika z ID-jem iz piškotka.
    """
    idu = bottle.request.get_cookie('uporabnik', secret=SKRIVNOST)
    return Uporabnik.z_id(idu)


def prijavi_uporabnika(uporabnik, piskotek=None):
    """
    Nastavi piškotek na podanega uporabnika.
    """
    if not uporabnik:
        nastavi_sporocilo("Prijava ni bila uspešna!")
        bottle.redirect('/prijava/')
    bottle.response.set_cookie('uporabnik', str(uporabnik.id), secret=SKRIVNOST, path='/')
    if piskotek:
        bottle.response.delete_cookie(piskotek, path='/')
    bottle.redirect('/')


def odjavi_uporabnika():
    """
    Pobriši piškotek z ID-jem prijavljenega uporabnika.
    """
    bottle.response.delete_cookie('uporabnik', path='/')
    bottle.redirect('/')


def status(preveri):
    """
    Vrni dekorator, ki preveri prijavljenega uporabnika v skladu s podano funkcijo
    in elemente vrnjenega zaporedja preda kot začetne argumente dekorirani funkciji.
    """
    @wraps(preveri)
    def decorator(fun):
        @wraps(fun)
        def wrapper(*largs, **kwargs):
            uporabnik = prijavljeni_uporabnik()
            out = fun(*preveri(uporabnik), *largs, **kwargs)
            if out is None:
                out = {}
            if isinstance(out, dict):
                out['uporabnik'] = uporabnik
            return out
        return wrapper
    return decorator


@status
def admin(uporabnik):
    """
    Preveri, ali ima uporabnik administratorske pravice.

    Dekorirana funkcija kot prvi argument sprejme prijavljenega uporabnika.
    """
    if not uporabnik.admin:
        bottle.abort(401, "Dostop prepovedan!")
    return (uporabnik, )


@status
def prijavljen(uporabnik):
    """
    Preveri, ali je uporabnik prijavljen.

    Dekorirana funkcija kot prvi argument sprejme prijavljenega uporabnika.
    """
    if not uporabnik:
        bottle.redirect('/prijava/')
    return (uporabnik, )


@status
def odjavljen(uporabnik):
    """
    Preveri, ali je uporabnik odjavljen.
    """
    if uporabnik:
        bottle.redirect('/')
    return ()


@bottle.get('/static/<datoteka:path>')
def static(datoteka):
    return bottle.static_file(datoteka, root='static')


@bottle.get('/')
@bottle.view('index.html')
def index():
    pass


@bottle.get('/filmi/najbolje-ocenjeni/')
@bottle.view('filmi.najbolje-ocenjeni.html')
def najbolje_ocenjeni():
    leto = bottle.request.query.leto
    filmi = Film.najboljsi_v_letu(leto)
    return dict(leto=leto, filmi=filmi)


@bottle.get('/filmi/<idf:int>/')
@bottle.view('filmi.podatki.html')
def podatki_filma(idf):
    try:
        film = Film.z_id(idf)
    except ValueError:
        bottle.abort(404, f'Film z ID-jem {idf} ne obstaja!')
    vloge = film.zasedba()
    igralci = [oseba for oseba, tip in vloge if tip == 'I']
    reziserji = [oseba for oseba, tip in vloge if tip == 'R']
    komentarji = film.komentarji()
    return dict(film=film, igralci=igralci, reziserji=reziserji,
                komentarji=komentarji)


@bottle.post('/filmi/<idf:int>/')
@prijavljen
def podatki_filma_post(uporabnik, idf):
    komentar = bottle.request.forms.komentar
    Film.z_id(idf).vpisi_komentar(uporabnik, komentar)
    bottle.redirect(f'/filmi/{idf}/')


@bottle.get('/osebe/poisci/')
@bottle.view('osebe.poisci.html')
def poisci_osebo():
    ime = bottle.request.query.ime
    osebe = Oseba.poisci(ime)
    if len(osebe) == 1:
        oseba, = osebe
        bottle.redirect(f'/osebe/{oseba.id}/')
    return dict(ime=ime, osebe=osebe)


@bottle.get('/osebe/<ido:int>/')
@bottle.view('osebe.podatki.html')
def podatki_osebe(ido):
    try:
        oseba = Oseba.z_id(ido)
    except ValueError:
        bottle.abort(404, f'Oseba z ID-jem {ido} ne obstaja!')
    vloge = oseba.poisci_vloge()
    igralec = [film for film, tip in vloge if tip == 'I']
    reziser = [film for film, tip in vloge if tip == 'R']
    return dict(oseba=oseba, igralec=igralec, reziser=reziser)


@bottle.get('/prijava/')
@bottle.view('prijava.html')
@odjavljen
def prijava():
    pass


@bottle.post('/prijava/')
@odjavljen
def prijava_post():
    uporabnisko_ime = bottle.request.forms.uporabnisko_ime
    geslo = bottle.request.forms.geslo
    nastavi_obrazec('prijava', {'uporabnisko_ime': uporabnisko_ime})
    prijavi_uporabnika(Uporabnik.prijavi(uporabnisko_ime, geslo), piskotek='prijava')


@bottle.get('/registracija/')
@bottle.view('registracija.html')
@odjavljen
def registracija():
    pass


@bottle.post('/registracija/')
@odjavljen
def registracija_post():
    uporabnisko_ime = bottle.request.forms.uporabnisko_ime
    geslo = bottle.request.forms.geslo
    geslo2 = bottle.request.forms.geslo2
    nastavi_obrazec('registracija', {'uporabnisko_ime': uporabnisko_ime})
    if geslo != geslo2:
        nastavi_sporocilo("Gesli se ne ujemata!")
        bottle.redirect('/registracija/')
    uporabnik = Uporabnik(uporabnisko_ime=uporabnisko_ime)
    try:
        uporabnik.dodaj(geslo)
        prijavi_uporabnika(uporabnik, piskotek='registracija')
    except ValueError:
        nastavi_sporocilo("Uporabniško ime že obstaja!")
        bottle.redirect('/registracija/')


@bottle.post('/odjava/')
@prijavljen
def odjava(uporabnik):
    odjavi_uporabnika()


bottle.BaseTemplate.defaults['prijavljeni_uporabnik'] = prijavljeni_uporabnik
bottle.BaseTemplate.defaults['preberi_sporocilo'] = preberi_sporocilo
bottle.BaseTemplate.defaults['preberi_obrazec'] = preberi_obrazec

if __name__ == '__main__':
    bottle.run(debug=True, reloader=True)
