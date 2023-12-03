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
    
    def __str__(self):
        return self.naslov

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
            return [Film(*vrstica) for vrstica in cur]
        finally:
            cur.close()


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
        SELECT film.naslov, film.leto, vloga.tip
          FROM film
          JOIN vloga ON film.id = vloga.film
         WHERE vloga.oseba = ?
         ORDER BY leto
        """
        cur = conn.cursor()
        try:
            cur.execute(sql, [self.id])
            return cur.fetchall()
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
