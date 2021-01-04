import baza
import sqlite3

conn = sqlite3.connect('nobel.db')
baza.ustvari_bazo_ce_ne_obstaja(conn)
conn.execute('PRAGMA foreign_keys = ON')

nobel = baza.pripravi_tabele(conn)


class Nobel:
    def __init__(self, leto, tema, zmagovalec):
        self.leto = leto
        self.tema = tema
        self.zmagovalec = zmagovalec

    def dodaj_v_bazo(self):
        with conn:
            conn.execute("""
                INSERT INTO nobel (yr, subject, winner) VALUES (?, ?, ?)
            """, (self.leto, self.tema, self.zmagovalec))

    @staticmethod
    def poisci(od, do):
        for leto, tema, zmagovalec in conn.execute("""
            SELECT yr, subject, winner FROM nobel
            WHERE yr BETWEEN ? AND ?
        """, (od, do)):
            yield Nobel(leto, tema, zmagovalec)
