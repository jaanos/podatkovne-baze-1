class Nobel:
    def __init__(self, conn):
        """
        Konstruktor razreda.
        """
        self.conn = conn

    def ustvari_in_uvozi(self):
        with open("nobel.sql", encoding="UTF-8") as f:
            sql = f.read()
        self.conn.executescript(sql)


def ustvari_bazo(conn):
    """
    Izvede ustvarjanje baze.
    """
    nobel = pripravi_tabele(conn)
    nobel.ustvari_in_uvozi()


def pripravi_tabele(conn):
    """
    Pripravi objekte za tabele.
    """
    return Nobel(conn)


def ustvari_bazo_ce_ne_obstaja(conn):
    """
    Ustvari bazo, če ta še ne obstaja.
    """
    with conn:
        cur = conn.execute("SELECT COUNT(*) FROM sqlite_master")
        if cur.fetchone() == (0, ):
            ustvari_bazo(conn)
