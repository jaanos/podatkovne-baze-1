import baza
import sqlite3

conn = sqlite3.connect('filmi.db')
baza.ustvari_bazo_ce_ne_obstaja(conn)
conn.execute('PRAGMA foreign_keys = ON')

uporabnik, zanr, oznaka, film, oseba, vloga, pripada = baza.pripravi_tabele(conn)
