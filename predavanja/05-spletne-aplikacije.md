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
  - `<meta />` - metapodatki (kodiranje znakov, način prikaza, ...)
  - `<script>` - skripta v jeziku JavaScript
  - `<style>` - deklaracija stilov v obliki CSS
  - `<link />` - zunanja datoteka (stili v CSS, ikone, ...)
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

---

# Oblikovanje spletnih strani

* Izgled posameznih elementov določamo s stili, opisanimi v jeziku CSS (*Cascading Style Sheets*).
* Stile navajamo z značko `<style>` ali v posebni datoteki s končnico `.css`, ki jo vključimo z `<link rel="stylesheet" href="stil.css" type="text/css">`.
* Osnovna sintaksa:
  ```css
  selektor {
    lastnost1: vrednost1;
    lastnost2: vrednost2;
    ...
  }
  ```
  - Lastnosti (kar je znotraj `{}`) lahko navedemo tudi v atributu `style` pri posamezni znački.

---

# Selektorji v CSS

* `značka`: element tipa `<značka>`
* `.razred`: element z atributom `class="razred"`
  - Element ima lahko tudi več razredov (ločeni s presledki).
* `#oznaka`: element z atributom `id="oznaka"`
* Selektorje lahko tudi kombiniramo:
  - `značka.razred#oznaka`: element `<značka class="razred" id="oznaka">`
* Če selektorje ločimo s presledki, se to razume kot gnezdene elemente:
  - `značka .razred`: element z atributom `class="razred"` znotraj elementa `<značka>`

---

# Knjižnica `bottle`

* Za Python je na voljo knjižnica `bottle`, ki ponuja funkcionalnost spletnega strežnika, do katerega lahko dostopamo lokalno.
* Knjižnico lahko namestimo v sistem, npr.
  ```bash
  pip install bottle
  ```
* Lahko pa si naložimo datoteko [`bottle.py`](https://github.com/bottlepy/bottle/raw/master/bottle.py) v mapo, kjer imamo svojo aplikacijo.

---

# Enostavna spletna aplikacija

Spletni vmesnik gradimo s funkcijami.

```python
import bottle

@bottle.get('/')
def pozdravi_svet():
    return 'Pozdravljen, svet!'

bottle.run()
```

* Funkcijama `bottle.get` in `bottle.post` podamo pot, vračata pa dekorator, ki registrira funkcijo za zahtevke `GET` oziroma `POST` na podani poti.
  - Ko strežnik dobi zahtevek za podano pot, se izvede ustrezna funkcija.

---

# Možnosti zaganjanja

```python
bottle.run(host='127.0.0.1', port=8080, reloader=False, debug=False)
```
* `host`: naslov, na katerem teče aplikacija
  - Privzeto je aplikacija dostopna samo lokalno.
  - Če navedemo `host='0.0.0.0'`, bo do aplikacije mogoče dostopati tudi z drugih računalnikov.
* `port`: številka vrat, na katerih teče aplikacija
  - Za vrata 80 običajno potrebujemo administratorske pravice.
* `reloader`: ali naj se aplikacija samodejno znova zažene ob spremembah kode.
* `debug`: ali naj se izpisujejo napake.
  - Med razvojem običajno nastavimo `reloader=True, debug=True`.

---

# Parametrizirane poti

* Poti lahko tudi parametriziramo.
* Imena parametrov morajo ustrezati imenom parametrov funkcije.
  ```python
  @bottle.get('/pozdravi/<ime>/')
  def pozdravi(ime):
      return f'Živjo, {ime}!'
  ```
* Privzeto funkcija dobi vrednost parametra kot niz. Lahko pa zahtevamo vnos celega števila.
  ```python
  @bottle.get('/kvadriraj/<n:int>')
  def kvadriraj(n):
      return f'{n}^2 = {n**2}'
  ```
  - Druge možnosti: `<x:float>` (decimalna števila), `<x:path>` (pot do datoteke - lahko vsebuje `/`), `<x:re:exp>` (niz, ki ustreza regularnemu izrazu `exp`).

---

# Predloge

* Funkcije vračajo vsebino strani v obliki HTML.
* Za vračanje vsebine predloge uporabljamo funkcijo `template`, ki ji kot poimenovane parametre podamo vrednosti spremenljivk.
  ```python
  @bottle.get('/pozdravi/<ime>/')
  def pozdravi(ime):
      return bottle.template('pozdravi.html', ime=ime)
  ```
* Predloge postavimo v mapo `views` (z malimi črkami).
  ```html
  <html>
    <head>
      <title>Pozdravna stran za {{ime}}</title>
    </head>
    <body>
      Živjo, <b>{{ime}}</b>!
    </body>
  </html>
  ```

---

# Predloge (2)

* V predlogah lahko med dvojnimi zavitimi oklepaji navajamo Pythonove izraze (običajno spremenljivke).
* Vrstice, ki se začnejo s `%`, se razumejo kot Pythonova koda.
  - Zamaknjene bloke (`if`, `for`, `with`, ...) moramo končati z `end`.
* Ostale vrstice gradijo izpis.
  ```html
  vrstica besedila
  %        if 3 < 7:
  %   a = 42
  % else:
  %        a = 100
  % end
  odgovor je {{a}}
  ```
  ```
  vrstica besedila
  odgovor je 42
  ```

---

# Primer

```html
<ul>
% for i in range(5):
    <li>{{i ** 2}}</li>
% end
</ul>
```

```html
<ul>
   <li>0</li>
   <li>1</li>
   <li>4</li>
   <li>9</li>
   <li>16</li>
</ul>
```

---

# Funkcija `rebase`

* Za skupne dele predlog lahko uporabljamo funkcijo `rebase`, ki ji podamo ime datoteke z osnovno predlogo.
* Tako kot funkciji `template` lahko tudi funkciji `rebase` kot poimenovane parametre podamo vrednosti spremenljivk.
* V osnovno predlogo vsebino strani podamo z `{{!base}}`.
  ```html
  <html>
    <head>
      <title>{{naslov}}</title>
    </head>
    <body>
      {{!base}}
    </body>
  </html>
  ```
  ```html
  % rebase('osnova.html', naslov=f'Pozdravna stran za {ime}')
  <h1>Živjo, <b>{{ime}}</b>!</h1>
  ```

---

# Statične datoteke

* S funkcijo `static_file` lahko ponujamo tudi statične datoteke (slike, stili CSS, skripte, ...)
* Statične datoteke običajno hranimo znotraj zanje predvidene mape (npr. `static`).
  ```python
  @bottle.get('/static/<datoteka:path>')
  def static(datoteka):
      return bottle.static_file(datoteka, root='static')
  ```

---

# Obrazci

* Podatke iz obrazcev, poslanih z metodo `GET`, preberemo iz objekta `request.query`.
  ```html
  <form action="/sestej/">
    a: <input type="text" name="a">
    b: <input type="text" name="b">
    <input type="submit" value="a + b">
  </form>
  ```
  ```python
  @bottle.get('/sestej/')
  def sestej():
      a = bottle.request.query.a
      b = bottle.request.query.b
      return f'{a} + {b} = {a + b}'
  ```
* Podatki so predstavljeni kot nizi!

---

# Metoda `POST` in preusmeritve

* Podatke iz obrazcev, poslanih z metodo `POST`, preberemo iz objekta `request.forms`.
* Preusmeritev izvedemo s funkcijo `redirect`.
  ```html
  <form action="/obrazec" method="POST">
      Uporabnik: <input type="text" name="uporabnik" />
      <input type="submit" value="Prijava" />
  </form>
  ```
  ```python
  @bottle.post('/obrazec')
  def obrazec_post():
      uporabnik = bottle.request.forms.uporabnik
      # zabeležimo prijavo
      bottle.redirect('/obrazec')
  ```

---

# Piškotki

* Piškotek nastavimo z metodo `response.set_cookie`.
  ```python
  bottle.response.set_cookie('uporabnik', uporabnik, secret=SKRIVNOST, path='/')
  ```
  - `SKRIVNOST` je vrednost, s katero podpisujemo piškotke in tako zagotovimo njihovo celovitost.
  - `path='/'` nam zagotavlja, da bomo lahko do piškotka dostopali iz celotne aplikacije.
* Piškotek preberemo z metodo `request.get_cookie`.
  ```python
  uporabnik = bottle.request.get_cookie('uporabnik', secret=SKRIVNOST)
  ```
* Piškotek pobrišemo z metodo `response.delete_cookie`.
  ```python
  bottle.response.delete_cookie('uporabnik', path='/')
  ```
