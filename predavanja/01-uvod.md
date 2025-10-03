---
marp: true
style: "@import url('style.css')"
---

# Podatkovne baze 1

* Predavanja:
  - Janoš Vidali ([janos.vidali@fmf.uni-lj.si](mailto:janos.vidali@fmf.uni-lj.si)), kabinet 1.14
  - ponedeljek 10-12 v predavalnici 3.04
  - ponedeljek 12-13 v predavalnici 3.04 (seminar, za 3. letnike)
* Vaje:
  - Ajda Lampe ([ajda.lampe@fmf.uni-lj.si](mailto:ajda.lampe@fmf.uni-lj.si)), kabinet 1.09
  - četrtek 9-11 v predavalnici 3.11

---

# Zakaj podatkovne baze?

* Kakšne programe pišemo sedaj?
  - Podatki "zapečeni" v program
  - Preberemo preko tipkovnice
* V banki bi bilo strahotno nepraktično, če bi morali ob vašem dvigu vtipkati vse vaše prejšnje pologe in dvige, da bi videli vaše stanje.
* Vnos podatkov in hranjenje podatkov
  - Podatki naj se obdržijo tudi medtem, ko program ne deluje.
  - Datoteke
* Kaj je dobrega z datotekami?
* Kaj pa je problem?

---

# Seznam e-naslovov prijateljev

* Lahko hranimo v datoteki?
* Ni problem:
  - Vsak naslov v svoji vrsti
  - Ali pa ločen z \|
  - Dokler poštni naslov ne vsebuje prehoda v novo vrsto ali \|, vse deluje kot namazano ...
  - Res?
* Iskanje je počasno
  - Ali je [janos.vidali@fmf.uni-lj.si](mailto:janos.vidali@fmf.uni-lj.si) že na seznamu?
  - Pregled cele datoteke

---

# Seznam e-naslovov prijateljev (2)

- Iskanje je počasno in drago.
  * Uporabimo indekse.
    + Spomnimo se na knjige!
    + Razpršene tabele, zgoščevalne funkcije, iskalna drevesa, ...
    + B-drevesa, ...
  * Zakaj ne bi za vsa opravila v zvezi z indeksi skrbel nekdo drug, mi pa bi jih le uporabljali?
    + In uživali v vseh blagodatih, ki nam jih indeksi nudijo ... <small>(če parafraziramo določenega slovenskega pisatelja)</small>

---

# Sočasen dostop

<span class="small">

* Program, ki omogoča vpis novih naslovov
  - Recimo, da ga sočasno uporablja več ljudi!
* Dva hočeta sočasno vnesti nov e-naslov?
* Sočasen dostop do iste datoteke!
* Možnosti:
  - Oba vnosa sta OK
  - Eden od vnosov se izgubi
  - Informacija iz obeh vnosov se "pomeša" in oba vnosa sta "zanič"
    + Verjetno programi, ki uporabljajo to datoteko, ne bodo delali več.
* Denimo, da bi na ta način poslovala banka!
  + Dva tipa računov: tekoči in varčevalni
  + Transakcije (dvige in pologe) za vsak račun hranimo v dveh datotekah, `tekoci.txt` in `varcevalni.txt`.

</span>

---

# Sočasen dostop (2)

* Janez želi prenesti 10 000 evrov z varčevalnega na tekoči račun,
* Micka pa položiti na isti varčevalni račun 5 evrov.
* Program uspešno zapiše novo stanje:
  * za +10 000 evrov na tekočem računu Janeza
  * in za -10 000 evrov na varčevalnem računu.
  * A še preden se ta zadnja akcija konča, se začne vpis Mickinih 5 evrov ...
* Potrebujemo kontrolo sočasnosti dostopa.
* To **gre** tudi za datoteke. Problem rešen ...
  - <small>če odštejemo ves trud pri programiranju, da bomo to dosegli.</small>

---

# Kontrola transakcij

* Janez želi prenesti 10 000 evrov z varčevalnega na tekoči račun.
  - Delo z dvema datotekama
  - Najprej opraviti posel na eni, nato še na drugi
* Kaj, če vmes zmanjka elektrike?
* Transakcije:
  - Zaporedja dogodkov, za katere velja, da se morajo zgoditi vsi, ali pa noben!
  - Potrebujemo način, da to zagotovimo.

---

# *A*CID

ACID: **A**tomicity, **C**onsistency, **I**solation, **D**urability

* **Atomarnost**:
  - Transakcija je celota.
  - Ali uspe vsa, ali pa sploh ne.
  - Ne sme uspeti le del transakcije.
  
---

# A*C*ID

- **Konsistentnost**:
  - Vsaka transakcija prevede dovoljeno stanje v dovoljeno.
  - Ob vsaki spremembi je treba torej preveriti, če se s tem ne kršijo pravila.
  - Primeri:
    + Bančni sistem ne sme dopuščati vnosa pologa osebi, ki ni registrirana kot klient banke.
    + Uporabniško ime ima lahko le študent FMF. Če nekoga izbrišemo iz podatkovne baze študentov FMF, se mora pobrisati tudi pripadajoče uporabniško ime!

---

# AC*I*D

- **Izolacija**:
  - Rezultat transakcije mora biti neviden ostalim transakcijam, dokler transakcija ni izvedena v celoti.
  - Primer: če preverjamo stanje na Janezovih računih med prenosom iz varčevalnega na tekoči račun, moramo videti bodisi stanje pred to transakcijo, bodisi po tej transakciji, nikakor pa ne vmes (ko smo npr. zabeležili nižje stanje na varčevalnem računu, višjega na tekočem pa še ne).

---

# ACI*D*

- **Stalnost**:
  - Rezultati transakcij morajo biti stalni in "preživeti" okvare sistema ali medijev.
  - Primer: če vam rezervacijski sistem v kinu dodeli sedež 15C in izda karto, trenutek za tem pa se "sesuje", mora po obnovitvi sistema še vedno veljati, da imate vi sedež 15C.

* Je to možno zagotoviti z ustrezno kodo v programih?
  - Seveda!
  - A za kakšno ceno?
* Zakaj ne bi vzeli sistema, ki to že "zna", in ge le uporabili?

---

# Sistemi za upravljanje z bazami podatkov

* DBMS: **D**ata**b**ase **M**anagement **S**ystem
  - Skrbijo za vse navedeno
  - Programski paket (skupek programov), ki omogoča, da ustvarjamo baze ter v bazah hranimo podatke in delamo z njimi
  - <http://en.wikipedia.org/wiki/Database_management_system>
* Več tipov baz
  - Hierarhični, mrežni, grafovski, ...
  - Relacijski (Codd, 1970)
* Danes praktično večina baz:
  - **R**elacijske podatkovne baze
  - **R**DMBS

---

# Sistemi za upravljanje z relacijskimi bazami podatkov

* Primeri RDMBS:
  - MS Access, MySQL, PostgreSQL, Oracle, MS SQL, DB2, SQLite, ...
* Pogosto rečemo *baza MySQL*.
  - To je narobe!
  - MySQL je RDBMS.
  - Baza je pa tisto, kar upravljamo z MySQL (npr. baza študentov, ...).

---

# Relacijske baze podatkov

<span class="small">

* Po domače: *Relacijska baza podatkov je skupek preglednic, ki jih lahko več ljudi sočasno popravlja.*
* Podatke hranimo v *tabelah* (*relacijah*), ki imajo *vrstice* in *stolpce*.
* Stolpci:
  - Lastnosti objektov
  - Ime in tip
* Vrstica: zapis
  - Podatki o določenem objektu
  - Vsaka vrstica predstavlja element relacije
* Podatkovna baza: skupek več tabel
  - Podatki so povezani preko referenc (tujih ključev)
* Najprej se bomo naučili delati z najbolj enostavnimi bazami, ki bodo sestavljene le iz ene tabele.

</span>

---

# Primeri

- Baza zaposlenih

  `IDZaposlenega` | `ImePriimek` | `IDOddelka` | `Stopnja`
  --------------- | ------------ | ----------- | ---------
  MK1             | Miha Kranjc  | PO          | IV
  MH1             | Maja Hrust   | KO          | VII
  LS1             | Lidija Svet  | RO          | V
  MK2             | Mitja Kern   | NO          | IV

---

# Primeri (2)

- Baza podatkov o državah (<http://sqlzoo.net>)

  `Name`      | `Region`   | `Area` | `Population` | `gdp`
  ----------- | ---------- | ------ | ------------ | ----------
  Afghanistan | South Asia | 652225 | 26000000     |
  Albania     | Europe     | 28728  | 3200000      | 6656000000

---

# Primeri (3)

- <http://uciSeSql.fmf.uni-lj.si/Nivo1/>, tabela `narocnik`

  `id_narocnik` [integer] | `ime` [character varying(255)] | `priimek` [character varying(255)] | `naslov` [character varying(255)] | `mesto` [character varying(255)]
  -- | -- | -- | -- | --
  1 | Janez | Novak  | Novi dom 32       | Trbovlje
  2 | Miha  | Jazbec | Stari trg 42      | Ljubljana
  3 | Mojca | Smodic | Trg revolucije 18 | Maribor
  4 | Ana   | Kolar  | Opekarna 66       | Ljubljana
  5 | Anja

---

# Entiteta, vrstica, stolpec, celica

* Entiteta
  - Stvar ali dogodek, ki ga opazujemo
  - Navadno ustrezajo razredom v objektno usmerjenih programskih jezikih (npr. Java, Python)
  - Primer: zaposleni, oddelek, ...
  - Vsaki entiteti pripada ena tabela.
* <span class="green">Vrstica</span>: primerek entitete
* <span class="red">Stolpec</span>: lastnost (npr. ime in priimek, stopnja izobrazbe)
* <span class="blue">Celica</span>: vrednost lastnosti določenega primerka

---

`IDZaposlenega` | <span class="red">`ImePriimek`</span> | `IDOddelka` | `Stopnja`
--------------- | ------------ | ----------- | ---------
MK1             | <span class="red">Miha Kranjc</span>  | PO          | IV
<span class="green">MH1</span> | <span class="blue">Maja Hrust</span> | <span class="green">KO</span> | <span class="green">VII</span>
LS1             | <span class="red">Lidija Svet</span>  | RO          | V
MK2             | <span class="red">Mitja Kern</span>   | NO          | IV