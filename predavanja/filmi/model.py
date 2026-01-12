#
#   Model za delo z bazo filmi.sqlite
#
#   J. Vidali, nov. 2024
#   Prirejeno po M. Pretnar, 2019, M. Lokar, dec. 2020
#

import bcrypt
import csv
import sqlite3 as dbapi
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json


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
        with open(f"podatki/{cls.VIR}", encoding='utf-8') as f:
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


@dataclass_json
@dataclass
class Uporabnik(Tabela, Entiteta):
    """
    Razred za uporabnika.
    """
    id: int = field(default=None)
    uporabnisko_ime: str = field(default=None)
    admin: bool = field(default=False)
    geslo: bytes = field(default=None)

    IME = 'uporabnisko_ime'
    VIR = 'uporabnik.csv'

    @classmethod
    def ustvari_tabelo(cls, cur=None):
        """
        Ustvari tabelo "uporabnik".
        """
        with Kazalec(cur) as cur:
            cur.execute("""
                CREATE TABLE uporabnik (
                    id              INTEGER PRIMARY KEY,
                    uporabnisko_ime TEXT    UNIQUE NOT NULL,
                    admin           INTEGER NOT NULL DEFAULT 0,
                    geslo           BLOB
                );
            """)

    @classmethod
    def pobrisi_tabelo(cls, cur=None):
        """
        Pobriši tabelo "uporabnik".
        """
        with Kazalec(cur) as cur:
            cur.execute("""
                DROP TABLE IF EXISTS uporabnik;
            """)

    @classmethod
    def uvozi_podatke(cls, cur=None):
        """
        Uvozi podatke v tabelo "uporabnik".
        """
        with Kazalec(cur) as cur:
            for vrstica in cls.preberi_vir():
                if vrstica["geslo"]:
                    vrstica["geslo"] = cls.zgostitev(vrstica["geslo"])
                else:
                    vrstica["geslo"] = None
                cur.execute("""
                    INSERT INTO uporabnik (uporabnisko_ime, admin, geslo)
                    VALUES (:uporabnisko_ime, :admin, :geslo);
                """, vrstica)

    @staticmethod
    def prijavi(uporabnisko_ime, geslo):
        """
        Vrni uporabnika z navedenim uporabniškim imenom in geslom.
        Če takega uporabnika ni, vrni neprijavljenega uporabnika.
        """
        sql = """
          SELECT id, uporabnisko_ime, admin, geslo
            FROM uporabnik WHERE uporabnisko_ime = ?;
        """
        with Kazalec() as cur:
            cur.execute(sql, [uporabnisko_ime])
            vrstica = cur.fetchone()
            if vrstica is None:
                return Uporabnik.NULL
            *data, zgostitev = vrstica
            if zgostitev and bcrypt.checkpw(geslo.encode("utf-8"), zgostitev):
                return Uporabnik(*data)
            else:
                return Uporabnik.NULL

    @classmethod
    def z_id(cls, idu):
        """
        Vrni uporabnika z navedenim ID-jem.
        Če takega uporabnika ni, vrni neprijavljenega uporabnika.
        """
        sql = """
          SELECT id, uporabnisko_ime, admin
            FROM uporabnik WHERE id = ?;
        """
        with Kazalec() as cur:
            cur.execute(sql, [idu])
            vrstica = cur.fetchone()
            if vrstica is None:
                return cls.NULL
            return cls(*vrstica)

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
        assert not self.id, "Uporabnik je že vpisan v bazo!"
        assert self.uporabnisko_ime, "Uporabniško ime ni določeno!"
        sql = """
          INSERT INTO uporabnik (uporabnisko_ime, geslo, admin)
          VALUES (?, ?, ?);
        """
        zgostitev = self.zgostitev(geslo)
        with Kazalec() as cur:
            try:
                with conn:
                    cur.execute(sql, [self.uporabnisko_ime, zgostitev, self.admin])
                self.id = cur.lastrowid
            except dbapi.IntegrityError:
                raise ValueError("Uporabniško ime že obstaja!")

    def spremeni_geslo(self, geslo):
        """
        Spremeni uporabnikovo geslo.
        """
        assert self.id, "Uporabnik še ni vpisan v bazo!"
        sql = """
          UPDATE uporabnik SET geslo = ?
           WHERE id = ?;
        """
        zgostitev = self.zgostitev(geslo)
        with Kazalec() as cur:
            with conn:
                cur.execute(sql, [zgostitev, self.id])


@dataclass_json
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

    @staticmethod
    def seznam():
        sql = """
            SELECT kratica FROM oznaka
            ORDER BY kratica;
        """
        with Kazalec() as cur:
            cur.execute(sql)
            yield from (Oznaka(kratica) for kratica, in cur)

@dataclass_json
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
                else:
                    vrstica['oznaka'] = None
                cur.execute("""
                    INSERT INTO film (id, naslov, dolzina, leto, ocena,
                                    metascore, glasovi, zasluzek, oznaka, opis)
                    VALUES (:id, :naslov, :dolzina, :leto, :ocena,
                            :metascore, :glasovi, :zasluzek, :oznaka, :opis);
                """, vrstica)

    @classmethod
    def z_id(cls, idf):
        """
        Vrni film z navedenim ID-jem.
        Če takega filma ni, sproži napako.
        """
        sql = """
          SELECT id, naslov, dolzina, leto, ocena,
                 metascore, glasovi, zasluzek, oznaka, opis
            FROM film WHERE id = ?;
        """
        with Kazalec() as cur:
            cur.execute(sql, [idf])
            vrstica = cur.fetchone()
            if vrstica is None:
                raise ValueError(f"Film z ID-jem {idf} ne obstaja!")
            return Film(*vrstica)

    def dodaj(self):
        """
        Dodaj film v bazo.
        """
        assert self.id is None, "Film je že v bazi!"
        sql = """
            INSERT INTO film (naslov, dolzina, leto, ocena,
                metascore, glasovi, zasluzek, oznaka, opis)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        try:
            with Kazalec() as cur:
                with conn:
                    cur.execute(sql, [self.naslov, self.dolzina, self.leto,
                                    self.ocena, self.metascore, self.glasovi,
                                    self.zasluzek, self.oznaka, self.opis])
                    self.id = cur.lastrowid
        except dbapi.IntegrityError:
            raise ValueError("Dodajanje filma ni bilo uspešno!")

    def posodobi(self):
        """
        Posodobi film v bazi.
        """
        assert self.id is not None, "Filma še ni v bazi!"
        sql = """
            UPDATE film SET naslov = ?, dolzina = ?, leto = ?,
                ocena = ?, metascore = ?, glasovi = ?,
                zasluzek = ?, oznaka = ?, opis = ?
            WHERE id = ?;
        """
        try:
            with Kazalec() as cur:
                with conn:
                    cur.execute(sql, [self.naslov, self.dolzina, self.leto,
                                    self.ocena, self.metascore, self.glasovi,
                                    self.zasluzek, self.oznaka, self.opis, self.id])
        except dbapi.IntegrityError:
            raise ValueError("Posodabljanje filma ni bilo uspešno!")

    def izbrisi(self):
        """
        Izbriši film v bazi.
        """
        assert self.id is not None, "Filma še ni v bazi!"
        sql = """
            DELETE FROM film
            WHERE id = ?;
        """
        try:
            with Kazalec() as cur:
                with conn:
                    cur.execute(sql, [self.id])
                    self.id = None
        except dbapi.IntegrityError:
            raise ValueError("Brisanje filma ni bilo uspešno!")

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
        Vrni seznam vseh oseb,
        ki so sodelovale pri filmu self:
        najprej režiserji, potem igralci,
        v ustreznem vrstnem redu
        """
        sql = """
            SELECT oseba.id, oseba.ime, vloga.tip, vloga.mesto
              FROM oseba
              JOIN vloga ON oseba.id = vloga.oseba
             WHERE vloga.film = ?
             ORDER BY tip DESC, mesto;
        """
        with Kazalec() as cur:
            cur.execute(sql, [self.id])
            yield from (Vloga(self, Oseba(oid, ime), tip, mesto)
                        for oid, ime, tip, mesto in cur)

@dataclass_json
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

    @classmethod
    def z_id(cls, ido):
        """
        Vrni oseob z navedenim ID-jem.
        Če take osebe ni, sproži napako.
        """
        sql = """
          SELECT id, ime
            FROM oseba WHERE id = ?;
        """
        with Kazalec() as cur:
            cur.execute(sql, [ido])
            vrstica = cur.fetchone()
            if vrstica is None:
                raise ValueError(f"Oseba z ID-jem {ido} ne obstaja!")
            return Oseba(*vrstica)

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


@dataclass_json
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


@dataclass_json
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


@dataclass_json
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
