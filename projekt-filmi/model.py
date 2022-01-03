import baza
import sqlite3
from sqlite3 import IntegrityError
from pomozne_funkcije import Seznam
from geslo import sifriraj_geslo, preveri_geslo

conn = sqlite3.connect('filmi.db')
baza.ustvari_bazo_ce_ne_obstaja(conn)
conn.execute('PRAGMA foreign_keys = ON')

uporabnik, zanr, oznaka, film, oseba, vloga, pripada = baza.pripravi_tabele(conn)


class LoginError(Exception):
    """
    Napaka ob napačnem uporabniškem imenu ali geslu.
    """
    pass


class Uporabnik:
    """
    Razred za uporabnika.
    """

    def __init__(self, ime, *, id=None):
        """
        Konstruktor uporabnika.
        """
        self.id = id
        self.ime = ime

    def __str__(self):
        """
        Znakovna predstavitev uporabnika.
        Vrne uporabniško ime.
        """
        return self.ime

    @staticmethod
    def prijava(ime, geslo):
        """
        Preveri, ali sta uporabniško ime geslo pravilna.
        """
        sql = """
            SELECT id, zgostitev, sol FROM uporabnik
            WHERE ime = ?
        """
        try:
            id, zgostitev, sol = conn.execute(sql, [ime]).fetchone()
            if preveri_geslo(geslo, zgostitev, sol):
                return Uporabnik(ime, id=id)
        except TypeError:
            pass
        raise LoginError(ime)

    def dodaj_v_bazo(self, geslo):
        """
        V bazo doda uporabnika s podanim geslom.
        """
        assert self.id is None
        zgostitev, sol = sifriraj_geslo(geslo)
        try:
            with conn:
                self.id = uporabnik.dodaj_vrstico(ime=self.ime, zgostitev=zgostitev, sol=sol)
        except IntegrityError:
            raise LoginError(self.ime)


class Film:
    """
    Razred za film.
    """

    def __init__(self, naslov, leto, ocena, *, id=None):
        """
        Konstruktor filma.
        """
        self.id = id
        self.naslov = naslov
        self.leto = leto
        self.ocena = ocena

    def __str__(self):
        """
        Znakovna predstavitev filma.
        Vrne naslov filma.
        """
        return self.naslov

    @staticmethod
    def najboljsi_v_letu(leto):
        """
        Vrne najboljših 10 filmov v danem letu.
        """
        sql = """
            SELECT id, naslov, leto, ocena
            FROM film
            WHERE leto = ? AND glasovi > 100000
            ORDER BY ocena DESC
            LIMIT 10
        """
        for id, naslov, leto, ocena in conn.execute(sql, [leto]):
            yield Film(naslov, leto, ocena, id=id)

    def dodaj_v_bazo(self, reziserji, igralci):
        """
        V bazo doda film s podanimi režiserji in igralci
        """
        assert self.id is None
        with conn:
            id = film.dodaj_vrstico(naslov=self.naslov, leto=self.leto, ocena=self.ocena)
            for mesto, oseba in enumerate(reziserji, 1):
                vloga.dodaj_vrstico(film=id, oseba=oseba.id, tip=TipVloge.R.name, mesto=mesto)
            for mesto, oseba in enumerate(igralci, 1):
                vloga.dodaj_vrstico(film=id, oseba=oseba.id, tip=TipVloge.I.name, mesto=mesto)
            self.id = id


class Oseba:
    """
    Razred za osebo.
    """

    def __init__(self, ime, *, id=None):
        """
        Konstruktor osebe.
        """
        self.id = id
        self.ime = ime

    def __str__(self):
        """
        Znakovna predstavitev osebe.
        Vrne ime osebe.
        """
        return self.ime

    def poisci_vloge(self):
        """
        Vrne vloge osebe.
        """
        sql = """
            SELECT film.naslov, film.leto, vloga.tip
            FROM film
                JOIN vloga ON film.id = vloga.film
            WHERE vloga.oseba = ?
            ORDER BY leto
        """
        for naslov, leto, tip_vloge in conn.execute(sql, [self.id]):
            yield (naslov, leto, TipVloge[tip_vloge])

    @staticmethod
    def poisci(niz):
        """
        Vrne vse osebe, ki v imenu vsebujejo dani niz.
        """
        sql = "SELECT id, ime FROM oseba WHERE ime LIKE ?"
        for id, ime in conn.execute(sql, [f'%{niz}%']):
            yield Oseba(ime=ime, id=id)

    def dodaj_v_bazo(self):
        """
        Doda osebo v bazo.
        """
        assert self.id is None
        with conn:
            self.id = oseba.dodaj_vrstico(ime=self.ime)


class TipVloge(Seznam):
    """
    Oznake za tip vloge.
    """
    I = 'igralec'
    R = 'režiser'