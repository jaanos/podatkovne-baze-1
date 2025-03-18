---
marp: true
style: "@import url('style.css')"
---

# Načrtovanje podatkovnih baz

<span class="small">

* Načrtovanje podatkovne baze je postopek opredelitve in razvoja strukture podatkovne baze.
  - Formalni model nekaterih vidikov realnega sveta (problemske domene)
* Mera za pravilnost načrtovane sheme podatkovne baze je realni svet.
  - Od tod sledi, da mora vsebina podatkovne baze odražati podatke, pravila in izjeme iz realnega sveta.

  ![h:260px](slike/nacrtovanje.png)

</span>

---

# Zgradba/arhitektura podatkovnih baz

Zgradbo podatkovnih baz opisuje trinivojska arhitektura [ANSI-SPARC](https://en.wikipedia.org/wiki/ANSI-SPARC_Architecture).

* **Zunanji nivo:** uporabnikov pogled na podatkovno bazo.
* **Konceptualni nivo:** kakšni podatki so shranjeni v bazi podatkov, odnosi med njimi.
* **Notranji nivo:** kako so podatki shranjeni v podatkovni bazi.

---

# Podatkovna neodvisnost

* **Logična podatkovna neodvisnost:** spremembe na konceptualnem nivoju ne povzročajo sprememb na zunanjem nivoju.
  - Dodajanje novih entitet, atributov, odnosov, ...
* **Fizična podatkovna neodvisnost:** spremembe na notranjem nivoju ne povzročajo sprememb na konceptualnem nivoju.
  - Sprememba datotečnega sistema, zunanjega pomnilnika, načina indeksiranja, ...

---

# Problemi pri načrtovanju podatkovnih baz

<span class="small">

* Nepoznavanje področja
  - Načrtovalec problemskega področja načeloma ne pozna.
  - Zato se mora najprej seznaniti in potem podrobno spoznati domeno problema in bodoče aplikacije.
* Pravila in izjeme
  - Poleg pravil v realnem svetu obstaja tudi veliko izjem.
  - Realni svet in njegovo okolje sta dinamična sistema, ki se pogosto spreminjata.
  - Načrtovalec mora pri svojem delu mora upoštevati vsa pravila in tudi vse izjeme.
  - Hkrati mora narediti dovolj fleksibilno shemo, ki bo prilagojena bodočim spremembam.
* Velikost
  - Načrti PB so pogosto zelo kompleksni.
  - Zato so za človeka (načrtovalca) težko obvladljivi.

</span>

---

# Ključ uspeha je v sodelovanju z uporabniki!

Pri sodelovanju morajo načrtovalci podatkovnih baz in uporabniki govoriti 'isti' jezik, sicer pride do večjih razhajanj med dejanskimi in realiziranimi nalogami.

![w:500px](slike/nacrtovanje1.png) ![w:500px](slike/nacrtovanje2.png)

---

# Nivoji načrtovanja

* **Konceptualni model:** izdelava modela podatkov v organizaciji, ki naj zadovolji vse informacijske potrebe oz. zahteve na izbranem področju.
  - Primer: poslovni sistem - računovodstvo / finance, kadri, proizvodnja, prodaja, nabava, razvoj
* **Logični model:** izdelava modela podatkov, ki upošteva ciljno podatkovno bazo.
  - Primer: relacijska podatkovna baza
* **Fizični model:** izdelava fizične podatkovne baze, ki je odvisna od izbranega DBMS.
  - Tabele, povezave, pravila, poizvedbe, ...

---

# Koraki načrtovanja

* Zbiranje in analiza zahtev uporabnikov
* Konceptualno načrtovanje
* Izbira DBMS
* Logično načrtovanje
* Fizično načrtovanje
* Implementacija podatkovne baze

---

# Konceptualni nivo načrtovanja

Izhodišče:

* Opis problema v pisni ali ustni obliki ter zahteve oz. želje uporabnikov
* Dokumentacija (predpisana/zakonska ali interna)
* Datotečna struktura (če obstaja)

---

# Celovit pristop h konceptualnemu načrtovanju

* Celovit pogled na izdelavo konceptualnega modela
* Možni koraki konceptualnega načrtovanja:
  - K1.1: Identificiraj entitetne tipe
  - K1.2: Identificiraj odnose
  - K1.3: Identificiraj in z entitetnimi tipi poveži atribute
  - K1.4: Atributom določi domene
  - K1.5: Določi kandidate za ključe; izmed kandidatov izberi glavni ključ
  - K1.6: Po potrebi uporabi elemente razširjenega ER diagrama
  - K1.7: Preveri, če v modelu obstajajo odvečni elementi
  - K1.8: Preveri, če model “zdrži” transakcije
  - K1.9: Preveri model z uporabnikom

---

# Zbiranje podatkov

* Intervjuji
* Pregled dosedanjega poslovanja
* Podatki na papirju
* Podatki v računalniških programih
* Podatki na spletnih straneh
* ...

---

# Predstavitev podatkov

<span class="small">

* Pregledamo vse omenjene samostalnike in fraze (npr. *profesor*, *predmet*, *izpit*, *rok*, *datum izpita*, ...).
* Pozorni smo na pomembne objekte (npr. ljudje, lokacije, ...).
* Skušamo ločiti objekte (npr. profesor, izpit, ...) od lastnosti objektov (ime, vpisna številka, ...).
* Vsako vrsto objekta predstavimo z **entitetnim tipom**, lastnosti objektov določene vrste pa z njegovimi **atributi**.
* Primerku entitetnega tipa rečemo **entiteta**.
* V relacijskih podatkovnih bazah bo vsakemu entitetnemu tipu pripadala ustrezna tabela, vsaki entiteti pa vrstica v tej tabeli.
  - Za glavni ključ izberemo atribut, ki enolično določa entiteto.
  - Če ga ni, uporabimo zaporedni ali naključni ID.

</span>

---

# Primer

<span class="small">

Naziv entitetnega tipa | Opis | Sinonim | Število entitet
---------------------- | ---- | ------- | ---------------
Profesor | Pedagoški delavec, ki je nosilec enega ali več predmetov | Pedagoški delavec | Vsaka katedra ima enega ali več profesorjev
Izpitni rok | Datum, na katerega je za nek predmet in določeno ciljno skupino (letnik, smer, ...) razpisan izpitni rok | Rok, pisni izpit, kolokvij | Na leto se razpiše okrog 300 pisnih izpitov; vsak predmet mora imeti vsaj tri roke letno
... | | |

</span>

---

# Odnosi med entitetami

<span class="small">

(angl. *relationship*, včasih rečemo tudi *relacija*)

* Omogočajo povezovanje informacij, ki pripadajo različnim entitetnim tipom.
* Opisujejo odnose med podatki.
* Trije osnovni tipi:
  - ena na ena
  - ena na več
  - več na več
* Uporabimo pregled uporabniških zahtev.
  - Iščemo glagole (npr. profesor *razpiše* rok, študent *polaga* izpit, študent *izbere* mentorja, študent *se vpiše* v letnik, ...)
  - Zanimajo nas samo tisti odnosi, ki so res potrebni za našo poslovno domeno (sposobnost abstrakcije).

</span>

---

# Odnosi ena na ena (1:1)

* Eni entiteti prvega entitetnega tipa ustreza natanko določena entiteta drugega entitetnega tipa in obratno.
  - To je skoraj ekvivalentno temu, da bi imeli en sam entitetni tip (oziroma eno samo širšo tabelo).
* Primer:
  - Oseba : Rojstni list
  - Odnos: ima / je izdan
    + Vsaka oseba ima natanko en rojstni list.

---

# Odnosi ena na več (1:*n*)

* Vsaki entiteti prvega entitetnega ustreza nič ali več entitet drugega entitetnega tipa, vsaka entiteta drugega entitetnega tipa pa ustreza eni entiteti prvega entitetnega tipa.
  - V relacijski podatkovni bazi predstavimo tako, da v drugi tabeli dodamo stolpec z referenco na prvo tabelo.
* Primer:
  - Naslov : Oseba
  - Odnos: je stalni naslov : ima stalni naslov
    + Vsaka oseba ima le en stalni naslov, na istem naslovu pa je lahko več oseb.

---

# Odnosi več na več (*m*:*n*)

* Vsaki entiteti prvega entitetnega tipa lahko ustreza več entitet drugega entitetnega tipa in obratno.
  - V relacijski podatkovni bazi predstavimo z vmesno (povezovalno) tabelo, katere glavni ključ sestoji iz referenc (tujih ključev) na tabeli za vsak entitetni tip.
* Primer:
  - Študent : Predavatelj
  - Odnos: posluša predavanja / predava
    + Vsak študent posluša predavanja več predavateljev, vsak predavatelj predava več študentom

---

# Konceptualni nivo načrtovanja

Postopek:

* Identifikacija entitetnih tipov
* Identifikacija odnosov
* Identifikacija atributov (ime, opis, privzeta vrednost, ...)
* Opredelitev domen (zaloge vrednosti)
* Določitev kandidatnih ključev in glavnega ključa
* Specializacija/posplošitev entitetnih tipov (po potrebi)
* Risanje ER diagrama
* Konzultacija z uporabniki

---

# Primer opisa sistema

* Podan je naslednji opis sistema.
  - Obstajajo osebe, ki jih opišemo z imenom, priimkom, starostjo, krajem bivanja in krajem rojstva. Osebe so lahko moškega in ženskega spola. Za moške nas zanima še vojaški čin, če ga ima, za ženske pa dekliški priimek. Za kraj nas zanima še čas bivanja v kraju (leta bivanja) in število prebivalstva. Tako za kraj rojstva kot tudi kraj bivanja nas zanima država, v kateri se nahaja. Poleg imena države nas zanima še število prebivalstva države.

* Izdelajmo konceptualni model.

---

# ER diagram

<span class="small">

(angl. *entity-relationship diagram*, tudi *entitetno-odnosni diagram*)

![h:350px](slike/er-ljudje.png)

* **Entitetne tipe** predstavimo s **pravokotniki**.
* **Atribute** predstavimo z **elipsami**.
* **Odnose** predstavimo z **rombi**.

</span>

---

# Orodja

* Papir in svinčnik
* Orodja, ki podpirajo le konceptualno modeliranje (risanje ER diagramov):
  - [Creately](http://creately.com/)
  - [Dia Diagram Editor](http://dia-installer.de/)
  - ...
* Orodja, kjer je ER diagram le ena od faz:
  - [Case Studio 2](http://case-studio.en.softonic.com/)
  - [DB Designer](https://www.fabforce.net/dbdesigner4/)
  - [Open Model Sphere](http://www.modelsphere.com/org/)
  - ...

---

# Entitetni tip - primeri risanja

<span class="columns small" style="--cols: 2;">
<span>

![w:400px](slike/entiteta-chen.png)

![w:400px](slike/entiteta-tipi.png)

</span>
<span>

![w:400px](slike/entiteta-uml.png)

</span>
</span>

---

# Števnosti odnosov

* Za vsak entitetni tip v nekem odnosu lahko določimo največje in najmanjše število, kolikokrat se posamezna entiteta pojavi v odnosu.
  * Najmanj: 0 (neobvezni odnos - tanka črta) ali 1 (obvezni odnos - debela črta)
  * Največ: 1 (puščica v smeri odnosa) ali *n* (poljubno mnogo - brez puščice)
  * Označujemo tudi z (*min*, *max*).
* Primera:

  <span class="columns small" style="--cols: 2;">
  <span>

  ![](slike/odnos-11-0n.png)

  </span>
  <span>

  ![](slike/odnos-01-1n.png)

  </span>
  </span>

---

# Vranja notacija

(angl. *crow's foot notation*)

* Odnose predstavimo s povezavami med entitetnimi tipi.
* S simboli pri entitetnem tipu povemo, koliko entitet povezanega entitetnega tipa je v odnosu z njim.

  <span class="columns small" style="--cols: 2;">
  <span>

  ![](slike/cfn-11-0n.png)

  </span>
  <span>

  ![](slike/cfn-01-1n.png)

  </span>
  </span>

* Dandanes najpogosteje uporabljana notacija.
* Pomanjkljivosti:
  - Odnosi ne morejo imeti atributov.
  - Možni so samo dvojiški odnosi.

---

# Logični nivo načrtovanja

* Izhajamo iz konceptualnega modela.
* Postopek:
  * Identifikacija tabel (entitetni tipi, odnosi)
  * Normalizacija podatkov (vsaj do 3. normalne oblike)
  * Transakcije (model mora omogočati vse transakcije, ki jih zahteva uporabnik)
  * Polni ER diagram
  * Definiranje integritetnih omejitev
  * Konzultacija z uporabniki
  * Predvideti je potrebno tudi bodoči razvoj!
* Orodja: Oracle Designer, Power Designer, DBDesigner, ...

---

# Identifikacija tabel

<span class="small">

* Za vsak entitetni tip naredimo tabelo.
  - Atribute predstavimo s stolpci tabele.
  - Če nimamo ustreznega glavnega ključa, ga dodamo (npr. zaporedni ID).
  - Pazimo, da je v vsaki celici samo en podatek!
* Odnos z največjo števnostjo 1 pri enem entitetnem tipu lahko predstavimo s tujim ključem na tabelo za drugi entitetni tip.
  - Kam gredo atributi takega odnosa?
* Odnos z najmanjšo števnostjo 0 pri vseh entitetnih tipih lahko predstavimo s povezovalno tabelo.
  - Glavni ključ sestoji iz tujih ključev na ustrezne tabele, atribute predstavimo s stolpci v tabeli.
  - Običajno uporabimo tak pristop tudi pri odnosih več na več z najmanjšo števnostjo 1.

</span>

---

# Integritetne omejitve

* Obvezni vnos podatka - `NOT NULL`
* Omejitev domene atributa - npr. spol je lahko *M* ali *Ž*
* Entitetna omejitev - glavni ključ ne more imeti vrednosti `NULL`
* Referenčna integriteta - tuji ključi
* Omejitve na nivoju uporabnikov - vloge, ki jim lahko določamo pravila dostopa do podatkov v podatkovni bazi

---

# Logični model - primer

```
oseba   (#id_osebe, ime, priimek, starost, kraj_rojstva->kraj(id_kraja))
moski   (#id_osebe->oseba(id_osebe), vojaski_cin)
zenska  (#id_osebe->oseba(id_osebe), dekliski_priimek)
kraj    (#id_kraja, ime, prebivalstvo, drzava->drzava(id_drzave))
drzava  (#id_drzave, ime, prebivalstvo)
bivanje (#id_osebe->oseba(id_osebe), #id_kraja->kraj(id_kraja), leta)
```

---

# Anomalije in normalizacija podatkov

* Denimo, da trgovina hrani podatke o prenosnikih, ki jih prodaja:
  
  <span class="small">

  Model          | Cena | Proizvajalec | Spletna stran | Pomoč
  -------------- | ---- | ------------ | ------------- | ----------------------------
  Inspiron B120  | 499€ | Dell         | http://www.dell.com    | support@dell.com
  Inspiron B130  | 599€ | Dell         | http://www.dell.com    | support@dell.com
  Inspiron E1705 | 949€ | Dell         | http://www.dell.com    | support@dell.com
  Satellite A100 | 549€ | Toshiba      | http://www.toshiba.com | support@toshiba.com
  Satellite P100 | 934€ | Toshiba      | http://www.toshiba.com | support@toshiba.com

  </span>

* Kakšne so težave?
  - Npr. spremeni se naslov servisa pri Dellu.
  - Ali pa Toshiba spremeni strukturo spletnih strani.

---

# Napake in potrata prostora

<span class="small">

* Z ustreznimi stavki `UPDATE` lahko sočasno popravimo podatke v vseh ustreznih vrsticah - načeloma je to počasno!
* Lahko se zgodi, da bomo posamezne vrstice vstavljali ali popravljali ročno in bo čez čas tabela izgledala tako:

  Model          | Cena | Proizvajalec | Spletna stran              | Pomoč
  -------------- | ---- | ------------ | -------------------------- | -------------------
  Inspiron B120  | 499€ | Del          | http://www.dell.com        | supp@dell.com
  Inspiron B130  | 599€ | Dell         | http://www.dell.com/laptop | supportLT@dell.com
  Inspiron E1705 | 949€ | DELL         | http://www.dell.com        | support@dell.com
  Satellite A100 | 549€ | To šiba      | http://www.toshiba.com     | support@toshiba.com
  Satellite P100 | 934€ | Toshiba      | https://www.toshiba.com    | support@toshiba.eu

* Poleg tega isti podatek po nepotrebnem vodimo večkrat!

</span>

---

# Rešitev

* Podatke porazdelimo po več tabelah.
* Poskrbimo, da še vedno podatke lahko pravilno uporabljamo.
* Primer:
  - V tabeli strank hranimo le poštno številko.
  - Če potrebujemo še kraj, potem iz druge tabele s pari (poštna številka, kraj) dobimo ustrezno ime kraja.

---

# Zgled

<span class="columns" style="--cols: 2;">
<span>

* Ustvarimo tabeli proizvajalcev in izdelkov.
* Odnos med njima (tipa ena na več) ohranimo z referenco (dodamo ustrezen stolpec).

</span>
<span class="small">

* Izdelki:

  Model          | Cena | ID proizvajalca
  -------------- | ---- | ---------------
  Inspiron B120  | 499€ | 1
  Inspiron B130  | 599€ | 1
  Inspiron E1705 | 949€ | 1
  Satellite A100 | 549€ | 2
  Satellite P100 | 934€ | 2

</span>
</span>

<span class="small">

* Proizvajalci:

  ID proizvajalca | Proizvajalec | Spletna stran          | Pomoč
  --------------- | ------------ | ---------------------- | -------------------
  1               | Dell         | http://www.dell.com    | support@dell.com
  2               | Toshiba      | http://www.toshiba.com | support@toshiba.com

</span>

---

# Kaj želimo doseči?

<span class="small">

* Preverimo poimenovanje atributov
  - Imena stolpcev naj ustrezajo njihovi vsebini.
  - V tabelah naj ne bo atributov (stolpcev), ki pripadajo različnim entitetnim tipom.
* Zmanjšamo podvajanje podatkov
  - Anomalije pri posodabljanju podatkov
    + Isti podatek vodimo večkrat
  - Anomalije pri vstavljanju podatkov
    + Kako vstaviti podatke, če del podatkov manjka?
    + Možnost vstavljanja nekonsistentnih podatkov
  - Anomalije pri brisanju podatkov
    + Izguba podatkov
* Anomalije rešujemo z dekompozicijo - eno tabelo razbijemo v več.

</span>

---

# Funkcijske odvisnosti in ključi

<span class="small">

* Naj bosta $X, Y$ podmnožici množice atributov tabele.
* Množica $Y$ je *funkcijsko odvisna* od množice $X$ (pišemo $X \to Y$), če nabor vrednosti atributov iz $X$ enolično določa vrednost vsakega atributa iz $Y$.
  - Funkcijska odvisnost $X \to Y$ je *trivialna*, če velja $Y \subseteq X$.
  - Funkcijska odvisnost $X \to Y$ je *tranzitivna*, če obstaja množica $Z$, da veljata netrivialni funkcijski odvisnosti $X \to Z$ in $Z \to Y$.
* Primera:
  - EMŠO enolično določa ime, priimek in datum rojstva osebe.
  - Dan, ura in predavalnica enolično določajo predmet in izvajalca.
* Množica $X$ je *nadključ*, če so vsi atributi tabele funkcijsko odvisni od $X$.
* Množica $X$ je *(kandidat za) ključ*, če je nadključ in nobena njena prava podmnožica ni nadključ.
  - Izmed kandidatov za ključ izberemo glavni ključ tabele.

</span>

---

# Prva normalna oblika (1NF)

* Tabela je v prvi normalni obliki, če so vsi njeni atributi atomarni - vsaka celica vsebuje le eno vrednost.
* Primer:
  
  <span class="small">

  <u>Predmet</u>   | Profesor  | Smer
  ---------------- | --------- | -------------------------------
  Seminar I        | J. Moder  | Pedagoška
  Analiza III      | B. Novak  | Teoretična, Uporabna
  Računalništvo II | K. Perko  | Uporabna
  Fizika           | M. Jazbec | Pedagoška, Uporabna, Teoretična

  - Glavni ključ: *Predmet*

  </span>

* V stolpcu *Smer* se lahko pojavi več vrednosti - tabela ni v prvi normalni obliki!

---

# Dekompozicija

<span class="columns small" style="--cols: 2;">
<span>

<u>Predmet</u>   | Profesor
---------------- | ---------
Seminar I        | J. Moder
Analiza III      | B. Novak
Računalništvo II | K. Perko
Fizika           | M. Jazbec

</span>
<span>

<u>Predmet</u> $\to$ | <u>Smer</u>
-------------------- | -----------
Seminar I            | Pedagoška
Analiza III          | Teoretična
Analiza III          | Uporabna
Računalništvo II     | Uporabna
Fizika               | Pedagoška
Fizika               | Uporabna
Fizika               | Teoretična

</span>
</span>

---

# Druga normalna oblika (2NF)

* Tabela je v drugi normalni obliki, če je v prvi normalni obliki in nima netrivialnih funkcijskih odvisnosti od prave podmnožice kakšnega kandidata za ključ.
* Primer:

  <span class="small">

  <u>Predmet</u>       | <u>Profesor</u> | Dan        | Ura   | Kabinet
  -------------------- | --------------- | ---------- | ----- | -------
  Seminar I            | J. Moder        | Sreda      | 10:00 | 23
  Analiza III          | B. Novak        | Četrtek    | 12:00 | 34
  Računalništvo II     | K. Perko        | Sreda      |  9:00 | 12
  Uvod v programiranje | K. Perko        | Ponedeljek | 11:00 | 12
  Fizika               | M. Jazbec       | Torek      | 14:00 | 17

  - Glavni ključ: *Predmet*, *Profesor*
  - Atribut *Kabinet* je odvisen le od atributa *Profesor* - tabela ni v drugi normalni obliki!

  </span>

---

# Dekompozicija

* Do težave pride, če npr. profesor zamenja kabinet - moramo popraviti povsod!

  <span class="columns small" style="grid-template-columns: 1.5fr 0.5fr">
  <span>

  <u>Predmet</u>       | <u>Profesor</u> $\to$ | Dan        | Ura
  -------------------- | --------------------- | ---------- | -----
  Seminar I            | J. Moder              | Sreda      | 10:00
  Analiza III          | B. Novak              | Četrtek    | 12:00
  Računalništvo II     | K. Perko              | Sreda      |  9:00
  Uvod v programiranje | K. Perko              | Ponedeljek | 11:00
  Fizika               | M. Jazbec             | Torek      | 14:00

  </span>
  <span>

  <u>Profesor</u> | Kabinet
  --------------- | -------
  J. Moder        | 23
  B. Novak        | 34
  K. Perko        | 12
  M. Jazbec       | 17

  </span>
  </span>

* V praksi je pogosto en sam kandidat za ključ, ta pa sestoji iz enega stolpca - taka tabela je že v drugi normalni obliki.

---

# Tretja normalna oblika (3NF)

* Tabela je v tretji normalni obliki, če je v drugi normalni obliki in nima tranzitivnih funkcijskih odvisnosti od kakšnega kandidata za ključ.
* Primer:

  <span class="small">

  <u>Predmet</u>       | Profesor  | Dan        | Ura   | Kabinet
  -------------------- | --------- | ---------- | ----- | -------
  Seminar I            | J. Moder  | Sreda      | 10:00 | 23
  Analiza III          | B. Novak  | Četrtek    | 12:00 | 34
  Računalništvo II     | K. Perko  | Sreda      |  9:00 | 12
  Uvod v programiranje | K. Perko  | Ponedeljek | 11:00 | 12
  Fizika               | M. Jazbec | Torek      | 14:00 | 17

  - Glavni ključ: *Predmet*
  - Atribut *Kabinet* je odvisen od atributa *Profesor*, ta pa od atributa *Predmet* - tabela ni v tretji normalni obliki!

  </span>

---

# Dekompozicija

* Spet bodo težave, če profesor zamenja kabinet.

  <span class="columns small" style="grid-template-columns: 1.5fr 0.5fr">
  <span>

  <u>Predmet</u>       | Profesor $\to$ | Dan        | Ura
  -------------------- | -------------- | ---------- | -----
  Seminar I            | J. Moder       | Sreda      | 10:00
  Analiza III          | B. Novak       | Četrtek    | 12:00
  Računalništvo II     | K. Perko       | Sreda      |  9:00
  Uvod v programiranje | K. Perko       | Ponedeljek | 11:00
  Fizika               | M. Jazbec      | Torek      | 14:00

  </span>
  <span>

  <u>Profesor</u> | Kabinet
  --------------- | -------
  J. Moder        | 23
  B. Novak        | 34
  K. Perko        | 12
  M. Jazbec       | 17

  </span>
  </span>

* Običajno normaliziramo (vsaj) do tretje normalne oblike.
  - Obstajajo tudi višje normalne oblike, npr. Boyce-Coddova normalna oblika.

---

# Primer ustvarjanja baze

* Narediti želimo bazo, ki bo hranila podatke o kinu.
* Grobe zahteve: vedeti moramo, kateri filmi se trenutno vrtijo, v katerih dvoranah se vrtijo in kako velike so dvorane.

---

# Konceptualni model

<span class="columns small" style="grid-template-columns: 0.58fr 0.5fr">
<span>

* ER diagram:
  
  ![](slike/er-kino.png)

</span>
<span>

* Tri tabele:
  - Film
  - Dvorana
  - Spored

* Dodatne omejitve:
  - Naslov in leto enolično določata film.
  - Ob enem terminu se v posamezni dvorani lahko predvaja le en film.
  - Leto mora biti po 1900.
  - Dolžina filma in kapaciteta dvorane morata biti pozitivni.
  - Vsi atributi so obvezni.

</span>
</span>

---

# Logični model (SQLite)

<span class="small">

```sql
CREATE TABLE film (
  id         integer  PRIMARY KEY AUTOINCREMENT,
  naslov     text     NOT NULL,
  leto       integer  NOT NULL CHECK (leto > 1900),
  dolzina    integer  NOT NULL CHECK (dolzina > 0),
  UNIQUE (naslov, leto)
);

CREATE TABLE dvorana (
  id         integer  PRIMARY KEY AUTOINCREMENT,
  kapaciteta integer  NOT NULL CHECK (kapaciteta > 0) 
);

CREATE TABLE spored (
  id         integer  PRIMARY KEY AUTOINCREMENT,
  film       integer  NOT NULL REFERENCES film(id),
  dvorana    integer  NOT NULL REFERENCES dvorana(id),
  termin     datetime NOT NULL,
  UNIQUE (dvorana, termin)
);
```

</span>
