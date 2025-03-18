---
marp: true
style: "@import url('style.css')"
---

# Delo s podatkovnimi bazami v Pythonu

<span class="small">

* Podatke hranimo v bazi.
* S pomočjo jezika SQL lahko enostavno dobimo ustrezne podatke.
* Sedaj pa bi s temi podatki radi še kaj naredili.
  - Kaj narisali, poiskali optimalno podzaporedje, ...
* Kako iz baze dobiti podatke, da jih uporabimo v izbranem programskem jeziku?
* Ali tudi, če počnemo take stvari, ki so bolj ali manj enostavno izvedljive kar s `SELECT` in ostalimi stavki v SQL?
  - Ja! Zakaj?
  - SQL je za običajnega uporabnika "pretežek".
  - Potrebujemo gumbke, vnosna polja, ...
  - Podatki morajo biti prikazani "lepo".

</span>

---

# Programski dostop do baze

Potrebovali bomo sledeče:

* Ustrezen ukaz, s katerim se povežemo z bazo.
  - Podobno kot pri delu z datotekami odpremo datoteko.
  - Po potrebi bo potrebno izvesti prijavo na podatkovno bazo.
* Ustrezen ukaz v našem programskem jeziku, s katerim bazi posredujemo ukaz v jeziku SQL (običajno v obliki niza).
  - Baza našemu programu vrne podatke - podobno, kot bi brali datoteko.
* Podatke ustrezno preoblikujemo za potrebe programa.
  - Podatke iz baze predstavimo z ustreznimi tipi v programskem jeziku.
* V ta namen imamo običajno ustrezne razrede, ki omogočajo tako funkcionalnost (objekti, gradniki, komponente, ...).

---

# Python in podatkovne baze

* Vsi programski jeziki se pogovarjajo z relacijskimi bazami preko **podatkovnega vmesnika**, ki je na voljo kot knjižnica.
* Podatkovni vmesnik omogoča komunikacijo med programom in RDBMS.
  - Za različne RDBMS so na voljo [različne knjižnice](http://wiki.python.org/moin/DatabaseInterfaces).
* Standard [DB-API 2.0](https://peps.python.org/pep-0249/) določa, kako se morajo obnašati te knjižnice za Python.
* Primeri:
  ```python
  import MySQLdb  # za MySQL
  import sqlite3  # za SQLite - vgrajena v Python
  import psycopg2 # za PostgreSQL
  ```
* Pogosto pišemo kar:
  ```python
  import sqlite3 as dbapi # in potem delamo kar z dbapi
  ```

---

# Osnovni koncepti

* Podatkovni vir: izvor podatkov
  - Podatkovne baze
  - Pa tudi: datoteke XML, ...
* Povezava do podatkovnega vira
  - Ustrezen objekt, ki vsebuje podatke o tem, kje je podatkovni vir in kako se do njega dostopa
  - Povezava je aktivna (odprta - delujoča) ali zaprta
  - `povezava = dbapi.connect(povezovalni_niz)`
    + Povezovalni niz vsebuje podatke za prijavo na podatkovno bazo.
    + SQLite: ime datoteke

---

# Osnovni koncepti (2)

* Kazalec
  - Prostor v pomnilniku, ki vsebuje podatke, ki jih dobimo iz tabel v bazi
  - Objekt, ki predstavlja ukaz, ki ga RDBMS izvede nad virom
  - Potrebuje odprto povezavo
  - `kazalec = povezava.cursor()`
  - `kazalec.execute(ustrezen_ukaz_SQL)`
* Podatki
  - Tabele, ki jih vrne ukaz
  - Predstavitev podatkov v programu
  - `kazalec.fetchall()`, `kazalec.fetchone()`, `kazalec.fetchmany(število)`

---

# Primer s SQLite

* Uporabimo bazo [`bbc.db`](jupyter/bbc.db).
* Izpišimo imena vseh evropskih držav.

  ```python
  import sqlite3 as dbapi
  povezava = dbapi.connect("bbc.db")
  kazalec = povezava.cursor()
  sql = "SELECT * FROM bbc WHERE region = 'Europe'"
  kazalec.execute(sql)        # izvedemo ukaz
  zapisi = kazalec.fetchall() # preberemo tabelo z rezultati
  for vrstica in zapisi:
      print(vrstica[0])       # ime je prvi element nabora
  kazalec.close()
  povezava.close()
  ```

---

# Še en primer

<span class="small">

```python
import sqlite3 as dbapi
# Povežemo se na novo bazo - s tem jo ustvarimo
conn = dbapi.connect("testdb.sqlite")
cur = conn.cursor()                        # Odpremo kazalec
cur.execute("DROP TABLE IF EXISTS test;")  # Zbrišemo tabelo, če že obstaja
# Izvedemo ukaz - ustvarimo tabelo
cur.execute("""
      CREATE TABLE test (
        id   integer PRIMARY KEY AUTOINCREMENT,
        num  integer,
        data text
      );
    """)
# Vstavimo podatke v tabelo
cur.execute("INSERT INTO test (num, data) VALUES (100, 'KU-KU');")
cur.execute("SELECT * FROM test;")         # Preberemo zapisane podatke
rezultat  = cur.fetchone()                 # Hočemo le eno vrstico
print(rezultat)                            # Izpiše se (1, 100, "KU-KU")
conn.commit()                              # Poskrbimo, da so spremembe trajne
# Zapremo povezave z bazo
cur.close()
conn.close()
```

</span>

---

# Uporaba `with`

<span class="small">

* Spomnimo: z datotekami lahko v Pythonu "varno" delamo tako, da jih odpremo v bloku `with`:
  ```python
  with open('datoteka.txt') as f:
      # delamo z datoteko
  ```
  - Po koncu izvajanja (tudi, če gre kaj narobe) se datoteka zapre.
* Če bloku `with` podamo povezavo na bazo, bo ob uspešnem dokončanju potrdil transakcijo, sicer jo bo pa preklical:
  <span class="smaller">
  ```python
  import sqlite3 as dbapi
  conn = dbapi.connect("testdb.sqlite")
  cur = conn.cursor()
  try:
      with conn:  
          cur.execute("""
                INSERT INTO test (id, num, data)
                VALUES (1, 200, 'kaj pa zdaj?');
              """)
  except dbapi.IntegrityError as ex:
      print(f"Napaka: {ex}")
  ```
  - Povezava in kazalec ostaneta odprta!
  </span>

</span>

---

# Parametriziranje ukazov SQL

<span class="small">

* Če želimo v ukaz SQL vstaviti parametre, na njihova mesta vstavimo `?`, vrednosti pa podamo s seznamom (ali naborom) kot drugi argument metode `execute`.
  ```python
  cur.execute("SELECT * FROM bbc WHERE name = ?;", ('Slovenia', ))
  cur.execute("""
        SELECT * FROM bbc
         WHERE population BETWEEN ? AND ?;
      """, [min, max])
  ```
  - Za ustrezno predstavitev podatkov poskrbi podatkovni vmesnik - ne pišemo navednic za nize!
* Druga možnost: poimenovani parametri, vrednosti podamo s slovarjem.
  ```python
  cur.execute("SELECT * FROM bbc WHERE name = :ime;", {'ime': 'Slovenia'})
  cur.execute("""
        SELECT * FROM bbc
         WHERE population >= :vrednost AND
               area >= :vrednost;
      """, {'vrednost': vrednost})
  ```

</span>

---

# SQL injection

<span class="small">

* Kaj, če bi aplikacija za potrebe prijave uporabnika izvedla tako poizvedbo?
  ```python
  cur.execute(f"""
        SELECT id, admin FROM uporabnik
         WHERE uporabnisko_ime = '{uporabnisko_ime}' AND
               geslo = '{geslo}';
      """)
  ```
  - Če uporabnik poda svoje uporabniško ime in ustrezno geslo, rezultat poizvedbe pove, ali ima uporabnik administratorske pravice, sicer pa ne vsebuje nobene vrstice.
* Zlonamerni uporabnik lahko podtakne sledeče podatke:
  ```python
  uporabnisko_ime = "admin' OR 0 AND --"
  geslo = ""
  ```
* Izvedla se bo taka poizvedba:
  <span class="smaller">
  ```sql
  SELECT id, admin FROM uporabnik
   WHERE uporabnisko_ime = 'admin' OR 0 AND --' AND
         geslo = '';
  ```
  </span>

</span>

---

# SQL injection (2)

<span class="small">

* Podatkov, nad katerimi nimamo popolnega nadzora (npr. jih lahko vnese uporabnik), nikoli ne vstavljamo neposredno v poizvedbo.
  - V Pythonu v ta namen **ne** uporabljamo `f`-nizov, metod `format` in `join`, operatorjev `%` in `+`, ...
* Namesto tega naj za vstavljanje poskrbi podatkovni vmesnik.

  ![h:300px](https://imgs.xkcd.com/comics/exploits_of_a_mom.png)

</span>

---

# Izvajanje več ukazov

* Z metodo `execute` lahko izvajamo samo en ukaz SQL.
  - Če navedemo več ukazov SQL (ločeni s `;`), dobimo napako.
* Z metodo `executemany` večkrat izvedemo en ukaz SQL z različnimi podatki.
  - Kot drugi parameter navedemo seznam naborov parametrov, ki se vsakič uporabijo.
  - Sledeče je (skoraj) ekvivalentno:
    ```python
    cur.executemany(sql, podatki)

    for nabor in podatki:
        cur.execute(sql, nabor)
    ```
* Z metodo `executescript` lahko izvajamo več ukazov SQL (ločeni s `;`).
  - Parametrov ne moremo navajati.

---

# Pridobivanje ID-ja vstavljene vrstice

* Denimo, da imamo tabelo z glavnim ključem, ki se sam generira.
  ```sql
  CREATE TABLE tabela (
    id integer PRIMARY KEY AUTOINCREMENT,
    stolpec text ...
  );
  ```
* Na kurzorju izvedemo ukaz za vstavljanje vrstice.
  ```python
  cur.execute("INSERT INTO tabela (stolpec) VALUES (?);", [vrednost])
  ```
* Vrednost glavnega ključa vstavljene vrstice dobimo s `cur.lastrowid`.
  - SQLite v vsako tabelo doda (skrit) stolpec `rowid` (če ne zahtevamo drugače).

---

# Uvoz podatkov iz datoteke CSV

* Če imamo podatke v datoteki CSV, jih lahko v Python uvozimo z vgrajeno knjižnico `csv`, npr.
  ```python
  import csv

  with open("nobel.csv") as f:
      rd = csv.reader(f)
      next(rd) # izpustimo prvo vrstico z naslovi stolpcev
      for vrstica in rd:
          # obdelamo vrstico - shranimo, uvozimo v bazo, ...
  ```

---

# Organizacija kode

Pri pisanju aplikacij kodo organiziramo po shemi MVC.

* _**M**odel_: podatkovni model aplikacije
  - Programski opis entitet, odnosov in atributov
  - Skrbi za komunikacijo s podatkovno bazo
  - Neodvisen od uporabniškega vmesnika
* _**V**iew_: vizualna predstavitev informacij
  - Tekstovna predstavitev, spletna stran, ...
* _**C**ontroller_: obdelava podatkov, prejetih od uporabnika
