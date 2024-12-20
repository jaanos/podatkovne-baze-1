#
#   Spletni vmesnik 
#   za delo z bazo filmi.sqlite
#
#   J. Vidali, nov. 2024
#

import bottle
import json
from functools import wraps
from model import Film, Oseba, Oznaka, Uporabnik, Komentar


SKRIVNOST = 'nekaj, kar bo zelo težko uganiti!!!! djnskfndkjfnsd'


def izbrisi_piskotek(piskotek):
    bottle.response.delete_cookie(piskotek, path='/')


def nastavi_sporocilo(sporocilo, piskotek='sporocilo'):
    """
    Nastavi piškotek s sporočilom.
    """
    bottle.response.set_cookie(piskotek, sporocilo, secret=SKRIVNOST, path='/')


def preberi_sporocilo(piskotek='sporocilo', izbrisi=True):
    """
    Preberi sporočilo in pobriši pripadajoči piškotek.
    """
    sporocilo = bottle.request.get_cookie(piskotek, secret=SKRIVNOST)
    if izbrisi:
        izbrisi_piskotek(piskotek)
    return sporocilo


def nastavi_obrazec(piskotek, obrazec):
    """
    Zapiši vrednosti obrazca v obliki slovarja v piškotek kot niz JSON.
    """
    nastavi_sporocilo(json.dumps(obrazec), piskotek)


def preberi_obrazec(piskotek, privzeto={}, izbrisi=True):
    """
    Preberi vrednosti obrazca in pobriši pripadajoči piškotek.
    """
    try:
        return json.loads(preberi_sporocilo(piskotek, izbrisi))
    except (TypeError, json.JSONDecodeError):
        return privzeto


def iz_obrazca(cls, obrazec=None, /, **kwargs):
    """
    Vrni objekt s podatki iz obrazca.
    """
    if obrazec is None:
        obrazec = bottle.request.forms
    podatki = {k: getattr(obrazec, k) for k in cls.NULL.to_dict()}
    podatki.update(kwargs)
    return cls(**podatki)


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
        izbrisi_piskotek(piskotek)
    bottle.redirect('/')


def odjavi_uporabnika():
    """
    Pobriši piškotek z ID-jem prijavljenega uporabnika.
    """
    izbrisi_piskotek('uporabnik')
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


@bottle.get('/filmi/film/<idf:int>/')
@bottle.view('filmi.film.html')
def filmi_film(idf):
    try:
        film = Film.z_id(idf)
    except IndexError as ex:
        bottle.abort(404, *ex.args)
    zasedba = list(film.zasedba())
    igralci = [vloga for vloga in zasedba if vloga.tip == 'I']
    reziserji = [vloga for vloga in zasedba if vloga.tip == 'R']
    return dict(film=film, igralci=igralci, reziserji=reziserji, uporabnik=prijavljeni_uporabnik())


@bottle.post('/filmi/film/<idf:int>/')
@bottle.view('filmi.film.html')
@prijavljen
def filmi_film_post(uporabnik, idf):
    komentar = iz_obrazca(Komentar, film=idf, uporabnik=uporabnik)
    try:
        komentar.shrani()
    except ValueError:
        nastavi_obrazec(f'filmi-film-{idf}', komentar.to_dict())
        nastavi_sporocilo("Dodajanje komentarja neuspešno!")
    bottle.redirect(f"/filmi/film/{idf}/")


@bottle.get('/filmi/najbolje-ocenjeni/')
@bottle.view('filmi.najbolje-ocenjeni.html')
def filmi_najbolje_ocenjeni():
    leto = bottle.request.query.leto
    filmi = list(Film.najboljsi_v_letu(leto))
    return dict(filmi=filmi, leto=leto)


@bottle.get('/filmi/dodaj/')
@bottle.view('filmi.dodaj.html')
@admin
def filmi_dodaj(uporabnik):
    pass


@bottle.post('/filmi/dodaj/')
@admin
def filmi_dodaj_post(uporabnik):
    film = iz_obrazca(Film)
    try:
        film.shrani()
    except ValueError:
        nastavi_obrazec('filmi-dodaj', film.to_dict())
        nastavi_sporocilo("Dodajanje filma neuspešno!")
        bottle.redirect("/filmi/dodaj/")
    bottle.redirect(f"/filmi/film/{film.id}/")


@bottle.get('/filmi/uredi/<idf:int>/')
@bottle.view('filmi.uredi.html')
@admin
def filmi_uredi(uporabnik, idf):
    return dict(film=Film.z_id(idf))


@bottle.post('/filmi/uredi/<idf:int>/')
@admin
def filmi_uredi_post(uporabnik, idf):
    film = iz_obrazca(Film, id=idf)
    try:
        film.shrani()
    except ValueError:
        nastavi_obrazec(f'filmi-uredi-{idf}', film.to_dict())
        nastavi_sporocilo("Urejanje filma neuspešno!")
        bottle.redirect(f"/filmi/uredi/{idf}")
    bottle.redirect(f"/filmi/film/{film.id}/")


@bottle.post('/filmi/izbrisi/<idf:int>/')
@admin
def filmi_izbrisi_post(uporabnik, idf):
    try:
        Film(id=idf).izbrisi()
    except (ValueError, IndexError):
        nastavi_sporocilo("Brisanje filma neuspešno!")
        bottle.redirect(f"/filmi/film/{idf}/")
    bottle.redirect("/")


@bottle.post('/filmi/izbrisi_komentar/<idf:int>/<idk:int>/')
@admin
def komentarji_izbrisi_post(uporabnik, idf, idk):
    try:
        Komentar(id=idk, film=idf).izbrisi()
    except (ValueError, IndexError):
        nastavi_sporocilo("Brisanje komentarja neuspešno!")
    bottle.redirect(f"/filmi/film/{idf}/")
    

@bottle.get('/osebe/oseba/<ido:int>/')
@bottle.view('osebe.oseba.html')
def osebe_oseba(ido):
    try:
        oseba = Oseba.z_id(ido)
    except IndexError as ex:
        bottle.abort(404, *ex.args)
    vloge = list(oseba.poisci_vloge())
    igralec = [vloga for vloga in vloge if vloga.tip == 'I']
    reziser = [vloga for vloga in vloge if vloga.tip == 'R']
    return dict(oseba=oseba, igralec=igralec, reziser=reziser)


@bottle.get('/osebe/poisci/')
@bottle.view('osebe.poisci.html')
def osebe_poisci():
    ime = bottle.request.query.ime
    osebe = list(Oseba.poisci(ime))
    if len(osebe) == 1:
        oseba, = osebe
        bottle.redirect(f'/osebe/oseba/{oseba.id}/')
    return dict(osebe=osebe, ime=ime)


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
bottle.BaseTemplate.defaults['Film'] = Film
bottle.BaseTemplate.defaults['Oseba'] = Oseba
bottle.BaseTemplate.defaults['Oznaka'] = Oznaka
bottle.BaseTemplate.defaults['Komentar'] = Komentar

if __name__ == '__main__':
    bottle.run(debug=True, reloader=True)
