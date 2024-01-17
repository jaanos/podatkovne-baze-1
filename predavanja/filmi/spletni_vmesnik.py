#
#   Spletni vmesnik 
#   za delo z bazo filmi.sqlite
#
#   J. Vidali, dec. 2023
#

import bottle
import json
from functools import wraps
from model import Film, Oseba, Oznaka, Uporabnik


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
    uporabnik = prijavljeni_uporabnik()
    spremenjeno = False
    if uporabnik.admin:
        igralci = preberi_obrazec(f'film{idf}I', None, izbrisi=False)
        reziserji = preberi_obrazec(f'film{idf}R', None, izbrisi=False)
        if igralci is None:
            igralci = [oseba for oseba, _ in Film.z_id(idf).zasedba('I')]
        else:
            igralci = Oseba.seznam(igralci)
            spremenjeno = True
        if reziserji is None:
            reziserji = [oseba for oseba, _ in Film.z_id(idf).zasedba('R')]
        else:
            reziserji = Oseba.seznam(reziserji)
            spremenjeno = True
    else:
        vloge = film.zasedba()
        igralci = [oseba for oseba, tip in vloge if tip == 'I']
        reziserji = [oseba for oseba, tip in vloge if tip == 'R']
    komentarji = film.komentarji()
    return dict(film=film, igralci=igralci, reziserji=reziserji,
                komentarji=komentarji, uporabnik=prijavljeni_uporabnik(),
                spremenjeno=spremenjeno)


@bottle.post('/filmi/<idf:int>/')
@prijavljen
def podatki_filma_post(uporabnik, idf):
    komentar = bottle.request.forms.komentar
    Film.z_id(idf).vpisi_komentar(uporabnik, komentar)
    bottle.redirect(f'/filmi/{idf}/')


@bottle.get('/filmi/dodaj/')
@bottle.view('filmi.dodaj.html', film=Film.NULL)
@admin
def dodaj_film(uporabnik):
    pass


@bottle.post('/filmi/dodaj/')
@admin
def dodaj_film_post(uporabnik):
    naslov = bottle.request.forms.naslov or None
    leto = bottle.request.forms.leto or None
    ocena = bottle.request.forms.ocena or None
    dolzina = bottle.request.forms.dolzina or None
    zasluzek = bottle.request.forms.zasluzek or None
    glasovi = bottle.request.forms.glasovi or None
    metascore = bottle.request.forms.metascore or None
    oznaka = bottle.request.forms.oznaka or None
    opis = bottle.request.forms.opis or ''
    data = dict(naslov=naslov, leto=leto, ocena=ocena,
                dolzina=dolzina, metascore=metascore,
                glasovi=glasovi, zasluzek=zasluzek, oznaka=oznaka,
                opis=opis)
    nastavi_obrazec('filmi-dodaj', data)
    film = Film(**data)
    try:
        film.dodaj()
    except ValueError:
        nastavi_sporocilo("Navedi vse potrebne podatke!")
        bottle.redirect('/filmi/dodaj/')
    izbrisi_piskotek('filmi-dodaj')
    bottle.redirect(f'/filmi/{film.id}/')


@bottle.get('/filmi/<idf:int>/uredi/')
@bottle.view('filmi.uredi.html')
@admin
def uredi_film(uporabnik, idf):
    try:
        film = Film.z_id(idf)
    except ValueError:
        bottle.abort(404, f'Film z ID-jem {idf} ne obstaja!')
    return dict(film=film)


@bottle.post('/filmi/<idf:int>/uredi/')
@admin
def uredi_film_post(uporabnik, idf):
    naslov = bottle.request.forms.naslov or None
    leto = bottle.request.forms.leto or None
    ocena = bottle.request.forms.ocena or None
    dolzina = bottle.request.forms.dolzina or None
    zasluzek = bottle.request.forms.zasluzek or None
    glasovi = bottle.request.forms.glasovi or None
    metascore = bottle.request.forms.metascore or None
    oznaka = bottle.request.forms.oznaka or None
    opis = bottle.request.forms.opis or ''
    data = dict(naslov=naslov, leto=leto, ocena=ocena,
                dolzina=dolzina, metascore=metascore,
                glasovi=glasovi, zasluzek=zasluzek, oznaka=oznaka,
                opis=opis, idf=idf)
    nastavi_obrazec(f'filmi{idf}', data)
    film = Film(**data)
    try:
        film.dodaj()
    except ValueError:
        nastavi_sporocilo("Navedi vse potrebne podatke!")
        bottle.redirect(f'/filmi/{idf}/uredi/')
    izbrisi_piskotek(f'filmi{idf}')
    bottle.redirect(f'/filmi/{idf}/')


@bottle.post('/filmi/<idf:int>/izbrisi/')
@admin
def izbrisi_film_post(uporabnik, idf):
    try:
        Film.z_id(idf).izbrisi()
    except ValueError:
        nastavi_sporocilo("Napaka pri brisanju filma!")
        bottle.redirect(f'/filmi/{idf}/')
    bottle.redirect('/')


@bottle.post('/filmi/<idf:int>/<tip:re:[IR]>/izbrisi/<ord:int>/')
@admin
def izbrisi_vlogo_post(uporabnik, idf, tip, ord):
    osebe = preberi_obrazec(f'film{idf}{tip}', None, izbrisi=False)
    if osebe is None:
        osebe = [oseba.id for oseba, _ in Film.z_id(idf).zasedba(tip)]
    try:
        if ord < 0:
            raise IndexError
        del osebe[ord]
        nastavi_obrazec(f'film{idf}{tip}', osebe)
    except IndexError:
        nastavi_sporocilo("Brisanje iz zasedbe ni uspelo!")
    bottle.redirect(f'/filmi/{idf}/')


@bottle.post('/filmi/<idf:int>/<tip:re:[IR]>/premakni/<ord:int>/')
@admin
def premakni_vlogo_post(uporabnik, idf, tip, ord):
    osebe = preberi_obrazec(f'film{idf}{tip}', None, izbrisi=False)
    if osebe is None:
        osebe = [oseba.id for oseba, _ in Film.z_id(idf).zasedba(tip)]
    try:
        if ord < 0:
            raise IndexError
        osebe[ord], osebe[ord+1] = osebe[ord+1], osebe[ord]
        nastavi_obrazec(f'film{idf}{tip}', osebe)
    except IndexError:
        nastavi_sporocilo("Preurejanje zasedbe ni uspelo!")
    bottle.redirect(f'/filmi/{idf}/')


@bottle.post('/filmi/<idf:int>/shrani/')
@admin
def shrani_zasedbo_post(uporabnik, idf):
    igralci = preberi_obrazec(f'film{idf}I', None, izbrisi=False)
    reziserji = preberi_obrazec(f'film{idf}R', None, izbrisi=False)
    if igralci is not None:
        igralci = [Oseba(ido) for ido in igralci]
    if reziserji is not None:
        reziserji = [Oseba(ido) for ido in reziserji]
    try:
        Film.z_id(idf).nastavi_zasedbo(igralci, reziserji)
    except ValueError:
        nastavi_sporocilo("Napaka pri shranjevanju zasedbe!")
        bottle.redirect(f'/filmi/{idf}/')
    ponastavi_zasedbo_post.__wrapped__(uporabnik, idf)


@bottle.post('/filmi/<idf:int>/ponastavi/')
@admin
def ponastavi_zasedbo_post(uporabnik, idf):
    izbrisi_piskotek(f'film{idf}I')
    izbrisi_piskotek(f'film{idf}R')
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
bottle.BaseTemplate.defaults['oznake'] = Oznaka.seznam

if __name__ == '__main__':
    bottle.run(debug=True, reloader=True)
