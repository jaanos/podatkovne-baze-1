#
#   Model (razreda Film in Oseba) k
#   programu
#         filmi_tekstovni_vmesnik.py
#   za delo z bazo filmi.sqlite
#
#   J. Vidali, dec. 2023
#   Prirejeno po M. Pretnar, 2019, M. Lokar, dec. 2020
#
import bcrypt
import sqlite3 as dbapi

conn = dbapi.connect('filmi.sqlite')
conn.execute("PRAGMA foreign_keys = ON;")


class Entiteta:
    """
    Nadrazred za posamezne entitetne tipe.
    """

    def __bool__(self):
        return self.id is not None
    
    def __init_subclass__(cls, /, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.NULL = cls()


class Film(Entiteta):
    """
    Opomba: lastnosti niso izvedene preko
    metod s @property - TODO!
    """
        
    def __init__(self, idf=None, naslov=None, leto=None, ocena=None,
                 dolzina=None, metascore=None, glasovi=0,
                 zasluzek=None, oznaka=None, opis=None):
        self.id = idf
        self.naslov = naslov
        self.leto = leto
        self.ocena = ocena
        self._dolzina = dolzina
        self.metascore = metascore
        self.glasovi = glasovi
        self.zasluzek = zasluzek
        self.oznaka = oznaka
        self.opis = opis
    
    def __str__(self):
        return self.naslov

    @staticmethod
    def z_id(ido):
        """
        Vrni film z navedenim ID-jem.
        """
        sql = """
          SELECT id, naslov, leto, ocena, dolzina, metascore,
                 glasovi, zasluzek, oznaka, opis
            FROM film WHERE id = ?
        """
        cur = conn.cursor()
        try:
            cur.execute(sql, [ido])
            vrstica = cur.fetchone()
            if vrstica is None:
                raise ValueError(f"Film z ID-jem {ido} ne obstaja!")
            return Film(*vrstica)
        finally:
            cur.close()

    def zasedba(self, tip=None):
        data = [self.id]
        if tip is None:
            sql_tip = ""
        else:
            sql_tip = "AND tip = ?"
            data.append(tip)
        sql = f"""
          SELECT oseba.id, oseba.ime, vloga.tip
            FROM oseba JOIN vloga
              ON vloga.oseba = oseba.id
           WHERE vloga.film = ?
           {sql_tip}
           ORDER BY vloga.tip, vloga.mesto
        """
        cur = conn.cursor()
        try:
            cur.execute(sql, data)
            return [(Oseba(*oseba), tip) for *oseba, tip in cur]
        finally:
            cur.close()

    def nastavi_zasedbo(self, igralci=None, reziserji=None):
        seznam = []
        data = [self.id]
        for tip, osebe in (('I', igralci), ('R', reziserji)):
            if osebe is not None:
                seznam.append((tip, osebe))
        if not seznam:
            return
        if len(seznam) == 1:
            (tip, _), = seznam
            sql_tip = """
              AND tip = ?
            """
            data.append(tip)
        else:
            sql_tip = ""
        sql_izbrisi = f"""
          DELETE FROM vloga WHERE film = ?
          {sql_tip}
        """
        sql_vstavi = """
          INSERT INTO vloga (film, oseba, tip, mesto)
          VALUES (?, ?, ?, ?)
        """
        cur = conn.cursor()
        try:
            with conn:
                cur.execute(sql_izbrisi, data)
                for tip, osebe in seznam:
                    for i, oseba in enumerate(osebe, 1):
                        cur.execute(sql_vstavi, [self.id, oseba.id, tip, i])
        except dbapi.IntegrityError:
            raise ValueError(f"Prišlo je do napake pri nastavljanju zasedbe filma z ID-jem {self.id}!")
        finally:
            cur.close()

    @staticmethod
    def najboljsi_v_letu(leto, n=10):
        """
        Vrni najboljših n filmov v danem letu.
        """
        sql = """
          SELECT id, naslov, leto, ocena
            FROM film
           WHERE leto = ?
           ORDER BY ocena DESC
           LIMIT ?
        """
        cur = conn.cursor()
        try:
            cur.execute(sql, [leto, n])
            return [Film(idf, naslov, leto, ocena) for idf, naslov, leto, ocena in cur]
        finally:
            cur.close()

    @property
    def dolzina(self):
        if self._dolzina is None and self:
            sql = """
              SELECT dolzina FROM film
               WHERE id = ?
            """
            cur = conn.cursor()
            try:
                cur.execute(sql, [self.id])
                self._dolzina, = cur.fetchone()
            finally:
                cur.close()
        return self._dolzina

    @dolzina.setter
    def dolzina(self, value):
        sql = """
          UPDATE film SET dolzina = ?
           WHERE id = ?
        """
        cur = conn.cursor()
        try:
            with conn:
                cur.execute(sql, [value, self.id])
        finally:
            cur.close()
        self._dolzina = value

    def komentarji(self):
        sql = """
          SELECT komentar, cas, uporabnik, uporabnisko_ime
            FROM komentar JOIN uporabnik
              ON komentar.uporabnik = uporabnik.id
           WHERE film = ?
        """
        cur = conn.cursor()
        try:
            cur.execute(sql, [self.id])
            return [(komentar, cas, Uporabnik(*uporabnik)) for komentar, cas, *uporabnik in cur]
        finally:
            cur.close()

    def vpisi_komentar(self, uporabnik, komentar):
        assert uporabnik, "Uporabnik ni prijavljen!"
        sql = """
          INSERT INTO komentar (film, uporabnik, komentar)
          VALUES (?, ?, ?)
        """
        cur = conn.cursor()
        try:
            with conn:
                cur.execute(sql, [self.id, uporabnik.id, komentar])
        finally:
            cur.close()

    def dodaj(self):
        """
        Dodaj film v bazo.
        """
        data = [self.naslov, self.leto, self.ocena, self.dolzina,
                self.metascore, self.glasovi, self.zasluzek,
                self.oznaka, self.opis]
        if self:
            sql = """
              UPDATE film SET naslov = ?, leto = ?, ocena = ?, dolzina = ?,
                metascore = ?, glasovi = ?, zasluzek = ?, oznaka = ?, opis = ?
                WHERE id = ?
            """
            data.append(self.id)
        else:
            sql = """
              INSERT INTO film (naslov, leto, ocena, dolzina, metascore,
                                glasovi, zasluzek, oznaka, opis)
              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
        cur = conn.cursor()
        try:
            with conn:
                cur.execute(sql, data)
            self.id = cur.lastrowid
        except dbapi.IntegrityError:
            raise ValueError("Obvezni podatki niso navedeni!")
        finally:
            cur.close()

    def izbrisi(self):
        assert self, "Film še ni vpisan v bazo!"
        sql_vloga = """
          DELETE FROM vloga WHERE film = ?
        """
        sql_komentar = """
          DELETE FROM komentar WHERE film = ?
        """
        sql_film = """
          DELETE FROM film WHERE id = ?
        """
        cur = conn.cursor()
        try:
            with conn:
                cur.execute(sql_vloga, [self.id])
                cur.execute(sql_komentar, [self.id])
                cur.execute(sql_film, [self.id])
        except dbapi.IntegrityError:
            raise ValueError(f"Prišlo je do napake pri brisanju filma z ID-jem {self.id}!")
        finally:
            cur.close()


class Oseba(Entiteta):
    """
    Opomba: lastnosti niso izvedene preko
    metod s @property - TODO!
    """

    def __init__(self, ido=None, ime=None):
        self.id = ido
        self.ime = ime
    
    def __str__(self):
        return self.ime

    @staticmethod
    def z_id(ido):
        """
        Vrni osebo z navedenim ID-jem.
        """
        sql = """
          SELECT id, ime FROM oseba WHERE id = ?
        """
        cur = conn.cursor()
        try:
            cur.execute(sql, [ido])
            vrstica = cur.fetchone()
            if vrstica is None:
                raise ValueError(f"Oseba z ID-jem {ido} ne obstaja!")
            return Oseba(*vrstica)
        finally:
            cur.close()

    @staticmethod
    def seznam(seznam_idjev):
        if not seznam_idjev:
            return []
        elif len(seznam_idjev) == 1:
            ido, = seznam_idjev
            return [Oseba.z_id(ido)]
        sql = f"""
          SELECT id, ime FROM oseba
           WHERE id IN ({', '.join(['?'] * len(seznam_idjev))})
        """
        cur = conn.cursor()
        try:
            cur.execute(sql, seznam_idjev)
            slovar = {ido: Oseba(ido, ime) for ido, ime in cur}
            return [slovar[ido] for ido in seznam_idjev]
        finally:
            cur.close()

    def poisci_vloge(self):
        """
        Vrni seznam vseh filmov, kjer
        je oseba self imela vlogo, 
        urejeno po letih
        """
        sql = """
          SELECT film.id, film.naslov, film.leto, film.ocena, vloga.tip
            FROM film
            JOIN vloga ON film.id = vloga.film
           WHERE vloga.oseba = ?
           ORDER BY leto
        """
        cur = conn.cursor()
        try:
            cur.execute(sql, [self.id])
            return [(Film(*film), tip) for *film, tip in cur]
        finally:
            cur.close()

    @staticmethod
    def poisci(niz):
        """
        Vrni vse osebe, ki v imenu vsebujejo dani niz.
        """
        sql = """
          SELECT id, ime FROM oseba WHERE ime LIKE ?
        """
        cur = conn.cursor()
        try:
            cur.execute(sql, ['%' + niz + '%'])
            return [Oseba(*vrstica) for vrstica in cur]
        finally:
            cur.close()


class Oznaka(Entiteta):
    @staticmethod
    def seznam():
        sql = """
          SELECT kratica FROM oznaka
        """
        cur = conn.cursor()
        try:
            cur.execute(sql)
            return [kratica for kratica, in cur]
        finally:
            cur.close()

class Uporabnik(Entiteta):
    def __init__(self, idu=None, uporabnisko_ime=None, admin=False):
        self.id = idu
        self.uporabnisko_ime = uporabnisko_ime
        self.admin = admin

    def __str__(self):
        return self.uporabnisko_ime or '(gost)'

    @staticmethod
    def prijavi(uporabnisko_ime, geslo):
        """
        Vrni uporabnika z navedenim uporabniškim imenom in geslom.
        Če takega uporabnika ni, vrni neprijavljenega uporabnika.
        """
        sql = """
          SELECT id, uporabnisko_ime, admin, geslo
            FROM uporabnik WHERE uporabnisko_ime = ?
        """
        cur = conn.cursor()
        try:
            cur.execute(sql, [uporabnisko_ime])
            vrstica = cur.fetchone()
            if vrstica is None:
                return Uporabnik.NULL
            *data, zgostitev = vrstica
            if bcrypt.checkpw(geslo.encode("utf-8"), zgostitev):
                return Uporabnik(*data)
            else:
                return Uporabnik.NULL
        finally:
            cur.close()

    @staticmethod
    def z_id(idu):
        """
        Vrni uporabnika z navedenim ID-jem.
        Če takega uporabnika ni, vrni neprijavljenega uporabnika.
        """
        sql = """
          SELECT id, uporabnisko_ime, admin
            FROM uporabnik WHERE id = ?
        """
        cur = conn.cursor()
        try:
            cur.execute(sql, [idu])
            vrstica = cur.fetchone()
            if vrstica is None:
                return Uporabnik.NULL
            return Uporabnik(*vrstica)
        finally:
            cur.close()

    @staticmethod
    def zgostitev(geslo):
        """
        Vrni zgostitev podanega gesla.
        """
        sol = bcrypt.gensalt()
        return bcrypt.hashpw(geslo.encode("utf-8"), sol)

    def dodaj(self, geslo):
        """
        Dodaj uporabnika v bazo z navedenim geslom.
        """
        assert not self, "Uporabnik je že vpisan v bazo!"
        assert self.uporabnisko_ime, "Uporabniško ime ni določeno!"
        sql = """
          INSERT INTO uporabnik (uporabnisko_ime, geslo, admin)
          VALUES (?, ?, ?)
        """
        cur = conn.cursor()
        try:
            zgostitev = self.zgostitev(geslo)
            with conn:
                cur.execute(sql, [self.uporabnisko_ime, zgostitev, self.admin])
            self.id = cur.lastrowid
        except dbapi.IntegrityError:
            raise ValueError("Uporabniško ime že obstaja!")
        finally:
            cur.close()

    def spremeni_geslo(self, geslo):
        """
        Spremeni uporabnikovo geslo.
        """
        assert self, "Uporabnik še ni vpisan v bazo!"
        sql = """
          UPDATE uporabnik SET geslo = ?
           WHERE id = ?
        """
        cur = conn.cursor()
        try:
            zgostitev = self.zgostitev(geslo)
            with conn:
                cur.execute(sql, [zgostitev, self.id])
        finally:
            cur.close()
