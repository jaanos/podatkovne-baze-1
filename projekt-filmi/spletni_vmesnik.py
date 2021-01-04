import json
import random
import bottle
from sqlite3 import IntegrityError
from model import LoginError, Uporabnik, Film, Oseba

NASTAVITVE = 'nastavitve.json'

try:
    with open(NASTAVITVE) as f:
        nastavitve = json.load(f)
        SKRIVNOST = nastavitve['skrivnost']
except FileNotFoundError:
    SKRIVNOST = "".join(chr(random.randrange(32, 128)) for _ in range(32))
    with open(NASTAVITVE, "w") as f:
        json.dump({'skrivnost': SKRIVNOST}, f)


def zahtevaj_prijavo():
    if bottle.request.get_cookie('uporabnik', secret=SKRIVNOST) != 'admin':
        bottle.abort(401, 'Nimate pravice za urejanje!')


def zahtevaj_odjavo():
    if bottle.request.get_cookie('uporabnik', secret=SKRIVNOST):
        bottle.redirect('/')


def prijavi_uporabnika(uporabnik):
    bottle.response.set_cookie('uporabnik', uporabnik.ime, path='/', secret=SKRIVNOST)
    bottle.response.set_cookie('uid', str(uporabnik.id), path='/', secret=SKRIVNOST)
    bottle.redirect('/')


@bottle.get('/static/<filename:path>')
def static(filename):
    return bottle.static_file(filename, root='static')


@bottle.get('/prijava/')
def prijava():
    zahtevaj_odjavo()
    return bottle.template(
        'prijava.html',
        napaka=None, ime=""
    )


@bottle.post('/prijava/')
def prijava_post():
    zahtevaj_odjavo()
    ime = bottle.request.forms['uporabnisko_ime']
    geslo = bottle.request.forms['geslo']
    try:
        prijavi_uporabnika(Uporabnik.prijava(ime, geslo))
    except LoginError:
        return bottle.template(
            'prijava.html',
            napaka='Uporabniško ime in geslo se ne ujemata!',
            ime=ime
        )


@bottle.get('/vpis/')
def vpis():
    zahtevaj_odjavo()
    return bottle.template(
        'vpis.html',
        napaka=None, ime=""
    )


@bottle.post('/vpis/')
def vpis_post():
    zahtevaj_odjavo()
    ime = bottle.request.forms['uporabnisko_ime']
    geslo1 = bottle.request.forms['geslo1']
    geslo2 = bottle.request.forms['geslo2']
    if geslo1 != geslo2:
        return bottle.template(
            'vpis.html',
            napaka='Gesli se ne ujemata!',
            ime=ime
        )
    try:
        uporabnik = Uporabnik(ime)
        uporabnik.dodaj_v_bazo(geslo1)
        prijavi_uporabnika(uporabnik)
    except IntegrityError:
        return bottle.template(
            'vpis.html',
            napaka='Uporabniško ime že obstaja!',
            ime=ime
        )


@bottle.get('/odjava/')
def odjava():
    bottle.response.delete_cookie('uporabnik', path='/')
    bottle.response.delete_cookie('uid', path='/')
    bottle.redirect('/')


@bottle.get('/')
def zacetna_stran():
    return bottle.template(
        'zacetna_stran.html',
        leta=range(1950, 2020),
        ime=bottle.request.get_cookie('uporabnik', secret=SKRIVNOST)
    )


@bottle.get('/najboljsi/<leto:int>/')
def najboljsi_filmi(leto):
    return bottle.template(
        'najboljsi_filmi.html',
        leto=leto,
        filmi=Film.najboljsi_v_letu(leto)
    )


@bottle.get('/dodaj-osebo/')
def dodaj_osebo():
    zahtevaj_prijavo()
    return bottle.template(
        'dodaj_osebo.html',
        napaka=None, ime=""
    )


@bottle.post('/dodaj-osebo/')
def dodaj_osebo_post():
    zahtevaj_prijavo()
    ime = bottle.request.forms.getunicode('ime')
    if not ime[0].isupper():
        return bottle.template(
            'dodaj_osebo.html',
            napaka='Ime se mora začeti z veliko začetnico!',
            ime=ime
        )
    else:
        oseba = Oseba(ime)
        oseba.dodaj_v_bazo()
        bottle.redirect('/')


@bottle.get('/isci/')
def isci():
    iskalni_niz = bottle.request.query.getunicode('iskalni_niz')
    osebe = Oseba.poisci(iskalni_niz)
    return bottle.template(
        'rezultati_iskanja.html',
        iskalni_niz=iskalni_niz,
        osebe=osebe
    )


bottle.run(debug=True, reloader=True)
