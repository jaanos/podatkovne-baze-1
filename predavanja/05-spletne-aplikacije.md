---
marp: true
style: "@import url('style.css')"
---

# Kako deluje internet

* Internet je v osnovi ogromno omrežje, v katerega so povezani računalniki (in ostale naprave).
* Lahko si ga predstavljamo kot graf.
  - Posamezni računalniki so listi tega grafa.
  - Vmesna vozlišča so usmerjevalniki.
* Če se želita dva računalnika pogovarjati, je potrebno poiskati pot v tem grafu.
  - Za iskanje učinkovitih poti skrbijo usmerjevalniki.
* Vsaka naprava na internetu ima svoj naslov.
  ```
  $ host www.google.com
  www.google.com has address 142.250.186.68
  www.google.com has IPv6 address 2a00:1450:400d:80e::2004
  ```
  - Vsaka naprava lahko uporablja naslova 127.0.0.1 (IPv4) ali ::1 (IPv6) za sklicevanje nase.

---

# DNS - *Domain Name System*

* Za lažjo uporabo napravam v omrežju dodelimo hierarhično organizirana imena.
* Primer: `www.google.com`
  - Vrhnja domena: `com` (ali `net`, `org`, ..., ter državne domene, kot `si`, ...)
  - Organizacija (znotraj `com`): `google`
  - Naprava (znotraj `google.com`): `www`
* Naslove, ki ustrezajo imenom, hranijo hierarhično organizirani imenski strežniki.
* Ko se želimo povezavi na `www.google.com`, pošljemo poizvedbo imenskemu strežniku internetnega ponudnika.
  - Če odgovora ne pozna, povpraša vrhnji strežnik, nato strežnik za `com`, nazadnje še strežnik za `google.com`.
* Ime `localhost` ustreza naslovoma 127.0.0.1 in ::1.

---

# Protokoli in vrata

* Za pošiljanje podatkov med računalniki se uporabljata omrežna protokola IPv4 in IPv6 (*Internet Protocol*, različici 4 in 6).
* Na posamezni napravi lahko teče več aplikacij, vsaka uporablja določena *vrata* pri enem od transportnih protokolov.
  - UDP (*User Datagram Protocol*) - za DNS, IPTV, IP telefonijo, ...
  - TCP (*Transmission Control Protocol*) - za večino storitev
* Številke vrat so večinoma standardizirane:
  - 53/UDP: DNS
  - 80/TCP: HTTP (*Hypertext Transfer Protocol*)
  - 443/TCP: HTTPS (HTTP preko SSL/TLS - šifrirana povezava)

---

# Kaj se zgodi, ko v brskalnik vtipkamo `https://www.google.com/`

* Operacijski sistem pošlje zahtevo imenskemu strežniku po protokolu DNS za IP naslov, ki ustreza imenu `www.google.com`.
  - Odgovor si zapomni, da ni potrebno vsakič spraševati.
* Z računalnikom na dobljenem naslovu poskusi vzpostaviti sejo TCP na vratih 443.
  - Seja TCP skrbi za zanesljiv prenos podatkov.
* Po vzpostavljeni seji se vzpostavi šifriran kanal po protokolu SSL/TLS.
* Brskalnik ima sedaj na voljo povezavo s spletnim strežnikom, s katerim se pogovarja po protokolu HTTP.

---

# Protokol HTTP

* Odjemalec (brskalnik) pošlje zahtevek, ki sestoji iz:
  - metode (`GET`, `POST`, ...)
  - naslova (znotraj strežnika - npr. `/index.html`)
  - glav zahtevka (npr. želeno kodiranje znakov, piškotki, ...)
* Strežnik odgovori z:
  - glavami odgovora
  - vsebino
* Za prikaz posamezne spletne strani je običajno potrebnih več zahtevkov!
  - Posebej se prenesejo slike, skripte, stili, ...

---

# Metoda `GET`

* Metoda `GET` se uporablja za pridobivanje podatkov iz spletnega strežnika.
  - Najpogosteje uporabljena metoda - uporabi se, če vnesemo spletni naslov ali kliknemo na povezavo.
* Pri uporabi metode `GET` naj se stanje na strežniku ne bi spremenilo.
  - Če dvakrat zapored izvedemo isti zahtevek (npr. pri osvežitvi strani) in se vmes ne zgodi nič drugega, naj bi dobili enak odgovor.
  - Iz baze lahko beremo, podatkov v njej pa naj ne bi spreminjali!

---

# Metoda `POST`

* Metoda `POST` se uporablja pri pošiljanju podatkov strežniku.
  - Obrazci, datoteke, ...
* Stanje na strežniku se lahko ob uporabi metode `POST` lahko spremeni.
  - Če spreminjamo podatke v bazi, uporabimo metodo `POST`!
* Dobra praksa: po uspešni izvedbi zahtevka z metodo `POST` izvedemo preusmeritev - naslednji zahtevek uporabi metodo `GET`.
  - Spremembe na bazi naj se izvedejo znotraj ene transakcije.
  - Če ob zahtevku z metodo `POST` dobimo vsebino (brez preusmeritve), brskalnik ob osvežitvi (po opozorilu) ponovno izvede enak zahtevek.
    + Možnost neželene ponovitve transakcije!

---

# Piškotki

* Piškotki so informacije, ki jih spletni strežnik pošlje odjemalcu, ta si jih pa nato shrani in pošlje nazaj strežniku pri naslednjem zahtevku.
* Uporabljajo se za hranjenje informacij o seji.
  - Podatki o prijavljenem uporabniku, vsebina košarice, obvestila, ...
* Pogosto so podatki šifrirani, tako da uporabnik nima vpogleda v vsebino piškotka in ga ne more spreminjati.
  - Uporabnik lahko še vedno pobriše piškotke!
* Strežnik naj bi spreminjal piškotke le ob uporabi metode `POST`.

---

# HTML

* Spletne strani so predstavljene v obliki HTML (*Hypertext Markup Language*).
* Dokumenti HTML so hierarhično organizirani z značkami.
  ```html
  <znacka>
    Vsebina značke
    <z atribut="vrednost" /> <!-- značka brez vsebine -->
  </znacka>
  ```
* Spletni brskalnik na podlagi drevesne strukture značk prikaže spletno stran.

---

# Značke HTML

* `<!DOCTYPE html>` - na vrhu dokumenta (brez zapiranja) določa obliko dokumenta
* `<html>` - vrhnja značka, ki vsebuje celotno spletno stran
* `<head>` - glava dokumenta
  - `<title>` - naslov dokumenta
  - `<meta>` - metapodatki (kodiranje znakov, način prikaza, ...)
  - `<script>` - skripta v jeziku JavaScript
  - `<style>` - deklaracija stilov v obliki CSS
  - `<link>` - zunanja datoteka (stili v CSS, ikone, ...)
* `<body>` - telo dokumenta

---

# Značke HTML (2)

* `<div>` - organizacijski blok (za potrebe postavitve)
* `<span>` - medvrstični blok (za potrebe oblikovanja)
* `<h1>`, `<h2>`, `<h3>` - naslovi
* `<p>` - odstavek
* `<br />` - prelom vrstice
* `<em>` - *poševno besedilo*; `<strong>` - **krepko besedilo**
* `<table>` - tabela
  - `<tr>` - vrstica tabele
  - `<th>` - celica glave tabele, `<td>` - celica telesa tabele
* `<ul>` - neoštevilčen seznam, `<ol>` - oštevilčen seznam
  - `<li>` - element seznama

---

# Značke HTML (3)

* `<a href="povezava">` - hiperpovezava na drugo stran
* `<img src="povezava" />` - slika
* `<form action="povezava" method="metoda">` - obrazec (`metoda` = `GET`/`POST`)
  - `<input type="tip" name="ime" value="vrednost" />` - vnosno polje, vrsta odvisna od `tip`:
    + `text` - besedilno polje
    + `password` - polje za geslo
    + `number` - številsko polje
    + `date` - polje za datum
    + `file` - nalaganje datoteke
    + `submit` - gumb za pošiljanje obrazca
