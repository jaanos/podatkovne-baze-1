---
marp: true
---

# SQL

---

# Kako do podatkov iz baze

* Vsebina tabel je uporabniku dostopna s pomočjo poizvedovalnih jezikov.
* Uveljavil se je standardni jezik **SQL** (*Structured Query Language*, strukturirani poizvedovalni jezik).
* Enostavno berljiv:
  ```sql
  SELECT tecajnica.simbol, vp.opis, tecajnica.eTecaj
    FROM tecajnica LEFT JOIN vp
         ON tecajnica.simbol = vp.simbol
   WHERE tecajnica.simbol LIKE 'Z%' AND 
         tecajnica.datum = '2004-02-26';
  ```

---

# `SELECT`

* Najpogosteje uporabljen ukaz
* Povpraševanje po podatkih
* Rezultat je tabela
  - `SELECT` torej vrne tabelo!
* Če ukaz uporabljamo v konzoli, se ta tabela izpiše.

---

# `SELECT` - osnovna struktura

`SELECT` *seznam stolpcev, ki jih želimo videti*
`FROM` *seznam tabel, kjer bomo podatke našli*
`WHERE` *pogoji, ki določajo, katere podatke želimo videti*

```sql
SELECT * FROM knjige 
 WHERE cena > 100.00
 ORDER BY naslov;
```

---

# `SELECT * FROM tabela`

* `*`
  - Izpiši vse stolpce
  - V izhodu naj bodo vsi stolpci izvorne tabele
* `tabela`
  - Ime tabele, katere stolpce želimo dobiti
* Zgledi z <http://ucisesql.fmf.uni-lj.si>
  ```sql
  SELECT * FROM drzave;
  ```

---

# SQLiteStudio

* Program za delo z RDBMS [SQLite](https://www.sqlite.org/)
* Na voljo kot [samostojen program](https://sqlitestudio.pl/) ali kot [različica za nameščanje](https://github.com/pawelsalawa/sqlitestudio/releases)

![](slike/sqlitestudio1.png) ![](slike/sqlitestudio2.png)

---

# `SELECT s1, s2 FROM tabPod`

* `s1, s2`
  - V izhodno tabelo uvrsti stolpca `s1` in `s2` iz tabele `tabPod`
* Primer (<https://sqlzoo.net/wiki/SELECT_basics>):
  - Vrni ime in število prebivalcev za vsako posamezno državo
    ```sql
    SELECT name, population FROM world;

    SELECT population, name FROM world;
    ```

---

# `SELECT s1, s2 FROM tabPod` (2)

* Kaj, če v izvorni tabeli ni stolpca s tem imenom?
  - Dobimo napako.
* `AS`: poimenovanje stolpca v izhodu

  ```sql
  SELECT name AS drzava, population AS st_prebivalcev FROM world;

  SELECT name AS "Ime države" FROM world;
  ```

---

# `SELECT DISTINCT`

* V izhodno tabelo uvrsti le med seboj različne vrstice.
* Primer: vrni tabelo kontinentov, ki nastopajo v tabeli.
  ```sql
  SELECT DISTINCT continent FROM world;
  ```
* Kaj vrneta sledeči poizvedbi?
  ```sql
  SELECT leto FROM film;

  SELECT DISTINCT leto FROM film;
  ```

---

# Primer

<small>

`Ime` | `Priimek` | `Starost` | `Kraj`
----- | --------- | --------- | ------
Janez | Slovenec  | 42        | Kranj
Ivan  | Slovenec  | 44        | Celje
Peter | Slovenec  | 33        | Kranj
Miha  | Slovenski | 12        | Celje

</small>

```sql
SELECT DISTINCT Kraj FROM T;               -- 2 vrstici
SELECT DISTINCT Priimek, Kraj FROM T;      -- 3 vrstice
SELECT DISTINCT Ime, Priimek, Kraj FROM T; -- 4 vrstice
SELECT Kraj FROM T;                        -- 4 vrstice
SELECT Priimek, Kraj FROM T;               -- 4 vrstice
SELECT Ime, Priimek, Kraj FROM T;          -- 4 vrstice
```

---

# Poizvedba po določenih podatkih

* Zanimajo nas le podatki o evropskih državah.
  ```sql
  SELECT * FROM world WHERE continent = 'Europe'
  ```
* **Konstantni nizi v enojnih narekovajih!**
* Možni relacijski operatorji:
  - `=`, `<>`, `<`, `<=`, `>`, `>=`,
  - `IS NULL`, `IS NOT NULL`,
  - `e [NOT] BETWEEN a AND b`,
  - `e [NOT] IN (v1, v2, ...)`,
  - `e [NOT] LIKE vzorec`,
  - in še kak specifičen za vsak RDBMS.
* Pogoje lahko sestavljamo z logičnimi operatorji `NOT`, `AND`, `OR`, `XOR` (in še kakimi specifičnimi za vsak RDBMS).

---

# Izrazi

* Kakšna je gostota prebivalstva vseh evropskih držav?
  ```sql
  SELECT name, population / area 
    FROM world
   WHERE continent = 'Europe';

  SELECT name AS ime_drzave,
         population / area AS gostota_prebivalstva
    FROM world
   WHERE continent = 'Europe';
  ```

* Zaokroži na dve decimalki in upoštevaj le države z več kot 2M prebivalstva.
  ```sql
  SELECT name AS "ime države", 
         ROUND(population / area, 2) AS "gostota prebivalstva" 
    FROM world
   WHERE continent = 'Europe' AND population > 2000000;
  ```

---

# Urejanje

* Izhodne podatke lahko uredimo.
* Na **koncu** dodamo `ORDER BY`.
* Primer: vrni imena države in število prebivalstva, urejeno po številu prebivalcev.
  ```sql
  SELECT name, population FROM world ORDER BY population;

  SELECT name, population FROM world ORDER BY 2;

  -- Uredimo padajoče
  SELECT name, population FROM world ORDER BY population DESC;
  ```
* Uporabimo lahko tudi izraze.
  - Vrni imena evropskih držav, urejena po gostoti prebivalstva.
    ```sql
    SELECT name FROM world
     WHERE continent = 'Europe'
     ORDER BY population/area;
    ```
  
---

# `SELECT` - dodatki

* Vrnjeni stolpci so poljubni izrazi!
  ```sql
  SELECT naslov, ROUND(cena * 1.10, 2) FROM knjige 
   WHERE cena * (1 + davek/100.0) > 100.00;
  ```
* Dodatki
  - `AS`: pre(po)imenujemo izhodni stolpec
  - `ORDER BY`: uredimo vrstice
  - `DISTINCT`: v končnem rezultatu upoštevamo le različne vrstice

---

# `SELECT` - primer

```sql
SELECT name, ROUND(population/1000000) AS prebMilijoni
  FROM world
 WHERE continent IN ('Asia', 'Europe') AND
       name LIKE 'C%';
```

* Razčlenimo:
  * Izpiši ime in število prebivalcev v milionih. 
  * Drugi stolpec poimenuj `prebMilijoni`,
  * Podatke pridobi iz tabele `world`,
  * Upoštevaj tiste vrstice, kjer je vrednost stolpca `continent` bodisi *Asia* bodisi *Europe* in kjer se vrednost v stolpcu `ime` začne s črko *C*.
* Pomen:
  - Izpiši imena in število prebivalcev tistih evropskih in azijskih držav, katerih imena se začnejo s *C*.

---

# Enostavna oblika stavka `SELECT`

```sql
SELECT * FROM world;

SELECT name, population FROM world;

SELECT name AS "Ime države" FROM world;

SELECT name AS Ime FROM world
 ORDER BY population DESC;

SELECT DISTINCT continent FROM world;

SELECT 2 FROM world WHERE continent = 'Europe';

SELECT population/area FROM world
 WHERE continent IN ('Europe', 'Asia', 'Africa') AND
       area BETWEEN 100000 AND 1000000;

SELECT name FROM world
 WHERE continent = 'Europe'
 ORDER BY population/area;
```

---

# Zahtevnejše poizvedbe

* **Izpiši imena držav, ki imajo manj prebivalcev kot Slovenija.**
* Lahko gremo po korakih
  * Najprej ugotovimo, koliko prebivalcev ima Slovenija
    ```sql
    SELECT population FROM world WHERE name = 'Slovenia';
    ```
    - Dobimo rezultat *2117674*
  * Uporabimo v ustrezni poizvedbi
    ```sql
    SELECT name FROM world WHERE population <= 2117674;
    ```
---

# S podpoizvedbami

* Kot vrednost v izrazih lahko uporabimo tudi rezultate ukaza `SELECT`
  ```sql
  SELECT name FROM world
   WHERE population <= (
           SELECT population FROM world  
            WHERE name = 'Slovenia'
         );
  ```
  * Izračunamo tabelo s stolpcem `population`, kjer upoštevamo le tiste vrstice, kjer je ime države *Slovenia*.
  * Ker ima ta tabela le eno vrstico, jo lahko uporabimo kot vrednost v zunanji poizvedbi.
* Ali bomo dobili tudi Slovenijo?

---

# Poizvedbe s podpoizvedbami

* Izpiši imena evropskih držav, ki imajo manj prebivalcev kot Slovenija.
  ```sql
  SELECT name FROM world
   WHERE population < (
           SELECT population FROM world
            WHERE name = 'Slovenia'
         ) AND
         continent = 'Europe';
  ```
* Ali bomo dobili tudi Slovenijo?

---

# Poizvedbe s podpoizvedbami (2)

* Izpiši imena držav, ki imajo število prebivalcev med številom prebivalcev Alžirije in Kanade.
* Po korakih:
  * ```sql
    SELECT population FROM world
     WHERE name = 'Canada';
    ```
    - Dobimo rezultat *40282200*.
  * ```sql
    SELECT population FROM world
     WHERE name = 'Algeria';
    ```
    - Dobimo rezultat *45400000*.
  * ```sql
    SELECT name FROM world
     WHERE population BETWEEN 40282200 AND 45400000;
    ```

---

# Poizvedbe s podpoizvedbami (3)

```sql
SELECT name FROM world
 WHERE population BETWEEN (
         SELECT population FROM world
          WHERE name = 'Canada'
       ) AND (
         SELECT population FROM world
          WHERE name = 'Algeria'
       );
```

---

# Omejitve

* Podpoizvedbe naj bi vračale le en stolpec z eno vrednostjo! Drugače pride do napake.
  - Npr. če bi v našem primeru imeli dve ali več držav z imenom *Canada*.
* Z nekaterimi operatorji lahko podpoizvedba vrača tudi več vrstic.
  - `e [NOT] IN (SELECT ... )` - ali je (ni) vrednost `e` ena izmed vrednosti v stolpcu
  - `e < ALL (SELECT ...)` - ali je vrednost `e` manjša od vseh vrednosti v stolpcu
  - `e >= ANY (SELECT ...)` - ali je vrednost `e` večja ali enaka vsaj eni vrednosti v stolpcu
  - `[NOT] EXISTS (SELECT ...)` - ali podpoizvedba vrne vsaj eno vrstico (oz. nobene)

---

# Primer

* [Tabela]((https://sqlzoo.net/wiki/SELECT_from_Nobel_Tutorial)): `nobel(yr, subject, winner)`
* Izpiši leta, kjer je bila podeljena Nobelova nagrada za fiziko in ne za kemijo.
* Kako?
  - Upoštevamo stolpce, kjer velja `subject = 'physics'`.
  - Izločimo vrstice, kjer je vrednost v stolpcu `yr` ena od tistih vrednosti, ki nastopajo v stolpcu `yr` pri tistih vrsticah, kjer je `subject = 'chemistry'`.
* ```sql
  SELECT DISTINCT yr FROM nobel
   WHERE subject = 'physics' AND
         yr NOT IN (
           SELECT yr FROM nobel
            WHERE subject = 'chemistry'
         );
  ```
* Zakaj `DISTINCT`?
  - Lahko je več dobitnikov za fiziko v istem letu!
