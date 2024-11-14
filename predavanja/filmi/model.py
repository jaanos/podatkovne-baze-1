#
#   Model za delo z bazo filmi.sqlite
#
#   J. Vidali, nov. 2024
#   Prirejeno po M. Pretnar, 2019, M. Lokar, dec. 2020
#

import csv
import sqlite3 as dbapi
from dataclasses import dataclass, field


conn = dbapi.connect('filmi.sqlite')
conn.execute("PRAGMA foreign_keys = ON;")


class Kazalec:
    """
    Upravitelj konteksta za kazalce.
    """

    def __init__(self, cur=None):
        """
        Konstruktor upravitelja konteksta.

        Če kazalec ni podan, odpre novega, sicer uporabi podanega.
        """
        if cur is None:
            self.cur = conn.cursor()
            self.close = True
        else:
            self.cur = cur
            self.close = False

    def __enter__(self):
        """
        Vstop v kontekst z `with`.

        Vrne kazalec - ta se shrani v spremenljivko, podano z `as`.
        """
        return self.cur

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Izstop iz konteksta.

        Če je bil ustvarjen nov kazalec, se ta zapre.
        """
        if self.close:
            self.cur.close()


class Tabela:
    """
    Nadrazred za tabele.
    """

    TABELE = []

    def __init_subclass__(cls, /, **kwargs):
        """
        Inicializacija podrazreda.

        Doda podrazred v seznam tabel.
        """
        super().__init_subclass__(**kwargs)
        cls.TABELE.append(cls)

    @classmethod
    def uvozi_podatke(cls, cur=None):
        """
        Uvozi podatke v tabelo.

        Privzeto ne naredi ničesar, podrazredi naj povozijo definicijo.
        """
        pass

    @classmethod
    def preberi_vir(cls):
        """
        Preberi vir v obliki CSV in vračaj slovarje za vsako vrstico.
        """
        with open(f"podatki/{cls.VIR}") as f:
            rd = csv.reader(f)
            stolpci = next(rd)
            for vrstica in rd:
                yield dict(zip(stolpci, vrstica))


class Entiteta:
    """
    Nadrazred za posamezne entitetne tipe.
    """
    def __bool__(self):
        """
        Pretvorba v logično vrednost.
        """
        return getattr(self, self.IME) is not None

    def __str__(self):
        """
        Znakovna predstavitev.
        """
        return getattr(self, self.IME) if self \
            else f"<entiteta tipa {self.__class__}>"

    def __init_subclass__(cls, /, **kwargs):
        """
        Inicializacija podrazreda.

        Pripravi prazen objekt.
        """
        super().__init_subclass__(**kwargs)
        cls.NULL = cls()


@dataclass
class Oznaka(Tabela, Entiteta):
    """
    Razred za oznako filma.
    """

    kratica: str = field(default=None)

    IME = 'kratica'

    @classmethod
    def ustvari_tabelo(cls, cur=None):
        """
        Ustvari tabelo "oznaka".
        """
        with Kazalec(cur) as cur:
            cur.execute("""
                CREATE TABLE oznaka (
                    kratica TEXT PRIMARY KEY
                );
            """)

    @classmethod
    def pobrisi_tabelo(cls, cur=None):
        """
        Pobriši tabelo "oznaka".
        """
        with Kazalec(cur) as cur:
            cur.execute("""
                DROP TABLE IF EXISTS oznaka;
            """)


@dataclass
class Film(Tabela, Entiteta):
    """
    Razred za film.
    """

    id: int = field(default=None)
    naslov: str = field(default=None)
    dolzina: int = field(default=None)
    leto: int = field(default=None)
    ocena: float = field(default=None)
    metascore: int = field(default=None)
    glasovi: int = field(default=0)
    zasluzek: int = field(default=None)
    oznaka: Oznaka = field(default=None)
    opis: str = field(default=None)

    VIR = "film.csv"
    IME = 'naslov'

    @classmethod
    def ustvari_tabelo(cls, cur=None):
        """
        Ustvari tabelo "film".
        """
        with Kazalec(cur) as cur:
            cur.execute("""
                CREATE TABLE film (
                    id        INTEGER PRIMARY KEY,
                    naslov    TEXT    NOT NULL,
                    dolzina   INTEGER NOT NULL,
                    leto      INTEGER NOT NULL,
                    ocena     REAL    NOT NULL,
                    metascore INTEGER,
                    glasovi   INTEGER NOT NULL
                                    CHECK (glasovi >= 0) 
                                    DEFAULT (0),
                    zasluzek  INTEGER,
                    oznaka    TEXT    REFERENCES oznaka (kratica),
                    opis      TEXT    NOT NULL
                );
            """)

    @classmethod
    def pobrisi_tabelo(cls, cur=None):
        """
        Pobriši tabelo "film".
        """
        with Kazalec(cur) as cur:
            cur.execute("""
                DROP TABLE IF EXISTS film;
            """)

    @classmethod
    def uvozi_podatke(cls, cur=None):
        """
        Uvozi podatke v tabeli "film" in "oznaka".
        """
        with Kazalec(cur) as cur:
            for vrstica in cls.preberi_vir():
                if vrstica['oznaka']:
                    cur.execute("""
                        SELECT kratica FROM oznaka
                        WHERE kratica = :oznaka;
                    """, vrstica)
                    if not cur.fetchone():
                        cur.execute("""
                            INSERT INTO oznaka (kratica) VALUES (:oznaka);
                        """, vrstica)
                        vrstica["zanr"] = cur.lastrowid
                else:
                    vrstica['oznaka'] = None
                cur.execute("""
                    INSERT INTO film (id, naslov, dolzina, leto, ocena,
                                    metascore, glasovi, zasluzek, oznaka, opis)
                    VALUES (:id, :naslov, :dolzina, :leto, :ocena,
                            :metascore, :glasovi, :zasluzek, :oznaka, :opis);
                """, vrstica)

    @staticmethod
    def najboljsi_v_letu(leto, n=10):
        """
        Vrni najboljših n filmov v danem letu.
        """
        sql = """
            SELECT id, naslov, dolzina, leto, ocena
              FROM film
             WHERE leto = ?
             ORDER BY ocena DESC
             LIMIT ?;
        """
        with Kazalec() as cur:
            cur.execute(sql, [leto, n])
            yield from (Film(*vrstica) for vrstica in cur)

    def zasedba(self):
        """
        Vrni zasedbo filma.
        """
        sql = """
            SELECT oseba.id, oseba.ime, vloga.tip, vloga.mesto
              FROM oseba
              JOIN vloga ON oseba.id = vloga.oseba
             WHERE vloga.film = ?
             ORDER BY vloga.tip, vloga.mesto;
        """
        with Kazalec() as cur:
            cur.execute(sql, [self.id])
            yield from (Vloga(self, Oseba(id, ime), tip, mesto) for id, ime, tip, mesto in cur)
            

@dataclass
class Oseba(Tabela, Entiteta):
    """
    Razred za osebo.
    """
    id: int = field(default=None)
    ime: str = field(default=None)

    VIR = "oseba.csv"
    IME = 'ime'

    @classmethod
    def ustvari_tabelo(cls, cur=None):
        """
        Ustvari tabelo "oseba".
        """
        with Kazalec(cur) as cur:
            cur.execute("""
                CREATE TABLE oseba (
                    id  INTEGER PRIMARY KEY,
                    ime TEXT    NOT NULL
                );
            """)

    @classmethod
    def pobrisi_tabelo(cls, cur=None):
        """
        Pobriši tabelo "oseba".
        """
        with Kazalec(cur) as cur:
            cur.execute("""
                DROP TABLE IF EXISTS oseba;
            """)

    @classmethod
    def uvozi_podatke(cls, cur=None):
        """
        Uvozi podatke v tabelo "oseba".
        """
        with Kazalec(cur) as cur:
            cur.executemany("""
                INSERT INTO oseba (id, ime)
                VALUES (:id, :ime);
            """, cls.preberi_vir())

    def poisci_vloge(self):
        """
        Vrni seznam vseh filmov, kjer
        je oseba self imela vlogo, 
        urejeno po letih
        """
        sql = """
            SELECT film.id, film.naslov, film.leto, vloga.tip, vloga.mesto
              FROM film
              JOIN vloga ON film.id = vloga.film
             WHERE vloga.oseba = ?
             ORDER BY leto;
        """
        with Kazalec() as cur:
            cur.execute(sql, [self.id])
            yield from (Vloga(Film(fid, naslov, leto=leto), self, tip, mesto)
                        for fid, naslov, leto, tip, mesto in cur)

    @staticmethod
    def poisci(niz):
        """
        Vrni vse osebe, ki v imenu vsebujejo dani niz.
        """
        sql = """
            SELECT id, ime FROM oseba WHERE ime LIKE ?;
        """
        with Kazalec() as cur:
            cur.execute(sql, ['%' + niz + '%'])
            yield from (Oseba(*vrstica) for vrstica in cur)


@dataclass
class Zanr(Tabela, Entiteta):
    """
    Razred za žanr.
    """

    id: int = field(default=None)
    naziv: str = field(default=None)

    IME = 'naziv'

    @classmethod
    def ustvari_tabelo(cls, cur=None):
        """
        Ustvari tabelo "zanr".
        """
        with Kazalec(cur) as cur:
            cur.execute("""
                CREATE TABLE zanr (
                    id    INTEGER PRIMARY KEY AUTOINCREMENT,
                    naziv TEXT    NOT NULL UNIQUE
                );
            """)

    @classmethod
    def pobrisi_tabelo(cls, cur=None):
        """
        Pobriši tabelo "zanr".
        """
        with Kazalec(cur) as cur:
            cur.execute("""
                DROP TABLE IF EXISTS zanr;
            """)


@dataclass
class Vloga(Tabela):
    """
    Razred za vlogo.
    """

    film: Film
    oseba: Oseba
    tip: str
    mesto: int

    VIR = "vloga.csv"
    VLOGE = {'I': 'igralec', 'R': 'režiser'}

    def __str__(self):
        """
        Znakovna predstavitev vloge.
        """
        return f"{self.oseba}: {self.tip_vloge} {self.mesto} v filmu {self.film}"

    @classmethod
    def ustvari_tabelo(cls, cur=None):
        """
        Ustvari tabelo "vloga".
        """
        with Kazalec(cur) as cur:
            cur.execute("""
                CREATE TABLE vloga (
                    film  INTEGER   REFERENCES film (id),
                    oseba INTEGER   REFERENCES oseba (id),
                    tip   CHARACTER CHECK (tip IN ('I', 'R') ),
                    mesto INTEGER   CHECK (mesto >= 1) 
                                    NOT NULL,
                    PRIMARY KEY (film, oseba, tip),
                    UNIQUE (film, tip, mesto)
                );
            """)

    @classmethod
    def pobrisi_tabelo(cls, cur=None):
        """
        Pobriši tabelo "vloga".
        """
        with Kazalec(cur) as cur:
            cur.execute("""
                DROP TABLE IF EXISTS vloga;
            """)

    @classmethod
    def uvozi_podatke(cls, cur=None):
        """
        Uvozi podatke v tabelo "vloga".
        """
        with Kazalec(cur) as cur:
            cur.executemany("""
                INSERT INTO vloga (film, oseba, tip, mesto)
                VALUES (:film, :oseba, :tip, :mesto);
            """, cls.preberi_vir())

    @property
    def tip_vloge(self):
        return self.VLOGE[self.tip]


@dataclass
class Pripada(Tabela):
    """
    Razred za pripadnost filma žanru.
    """

    film: Film
    zanr: Zanr

    VIR = "zanr.csv"

    def __str__(self):
        """
        Znakovna predstavitev pripadnosti.
        """
        return f"{self.film} pripada žanru {self.zanr}"

    @classmethod
    def ustvari_tabelo(cls, cur=None):
        """
        Ustvari tabelo "pripada".
        """
        with Kazalec(cur) as cur:
            cur.execute("""
                CREATE TABLE pripada (
                    film INTEGER REFERENCES film (id) ON DELETE CASCADE,
                    zanr INTEGER REFERENCES zanr (id) ON UPDATE CASCADE,
                    PRIMARY KEY (film, zanr)
                );
            """)

    @classmethod
    def pobrisi_tabelo(cls, cur=None):
        """
        Pobriši tabelo "pripada".
        """
        with Kazalec(cur) as cur:
            cur.execute("""
                DROP TABLE IF EXISTS pripada;
            """)

    @classmethod
    def uvozi_podatke(cls, cur=None):
        """
        Uvozi podatke v tabeli "pripada" in "zanr".
        """
        with Kazalec(cur) as cur:
            for vrstica in cls.preberi_vir():
                cur.execute("""
                    SELECT id FROM zanr
                    WHERE naziv = :naziv;
                """, vrstica)
                rezultat = cur.fetchone()
                if rezultat:
                    vrstica["zanr"], = rezultat
                else:
                    cur.execute("""
                        INSERT INTO zanr (naziv) VALUES (:naziv);
                    """, vrstica)
                    vrstica["zanr"] = cur.lastrowid
                cur.execute("""
                    INSERT INTO pripada (film, zanr)
                    VALUES (:film, :zanr);
                """, vrstica)


def ustvari_tabele(cur=None):
    """
    Ustvari vse tabele.
    """
    with Kazalec(cur) as cur:
        for t in Tabela.TABELE:
            t.ustvari_tabelo(cur=cur)


def pobrisi_tabele(cur=None):
    """
    Pobriši vse tabele.
    """
    with Kazalec(cur) as cur:
        for t in reversed(Tabela.TABELE):
            t.pobrisi_tabelo(cur=cur)


def uvozi_podatke(cur=None):
    """
    Uvozi vse podatke.
    """
    with Kazalec(cur) as cur:
        for t in Tabela.TABELE:
            t.uvozi_podatke(cur=cur)


def ustvari_bazo(pobrisi=False, cur=None):
    """
    Ustvari tabele in uvozi podatke.
    """
    with Kazalec(cur) as cur:
        try:
            with conn:
                cur.execute("PRAGMA foreign_keys = OFF;")
                if pobrisi:
                    pobrisi_tabele(cur=cur)
                ustvari_tabele(cur=cur)
                uvozi_podatke(cur=cur)
        finally:
            cur.execute("PRAGMA foreign_keys = ON;")
