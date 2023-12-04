#
#   Model (razreda Film in Oseba) k
#   programu
#         filmi_tekstovni_vmesnik.py
#   za delo z bazo filmi.sqlite
#
#   J. Vidali, dec. 2023
#   Prirejeno po M. Pretnar, 2019, M. Lokar, dec. 2020
#
import sqlite3 as dbapi

conn = dbapi.connect('filmi.sqlite')


class Film:
    """
    Opomba: lastnosti niso izvedene preko
    metod s @property - TODO!
    """
        
    def __init__(self, idf, naslov, leto, ocena):
        self.id = idf
        self.naslov = naslov
        self.leto = leto
        self.ocena = ocena
        self._dolzina = None
    
    def __str__(self):
        return self.naslov

    def zasedba(self):
        sql = """
          SELECT oseba.id, oseba.ime, vloga.tip
            FROM oseba JOIN vloga
              ON vloga.oseba = oseba.id
           WHERE vloga.film = ?
           ORDER BY vloga.tip, vloga.mesto
        """
        cur = conn.cursor()
        try:
            cur.execute(sql, [self.id])
            return [(Oseba(*oseba), tip) for *oseba, tip in cur]
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
        if self._dolzina is None:
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


class Oseba:
    """
    Opomba: lastnosti niso izvedene preko
    metod s @property - TODO!
    """

    def __init__(self, ido, ime):
        self.id = ido
        self.ime = ime
    
    def __str__(self):
        return self.ime

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
