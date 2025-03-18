---
marp: true
style: "@import url('style.css')"
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
* Pogosto so podatki kriptografsko podpisani, tako da uporabnik ne more spreminjati piškotka.
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

<span class="small">

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

</span>

---

# Predloge

<span class="small">

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

</span>

---

# Predloge (2)

<span class="small">

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

</span>

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

# Dekorator `view`

* Namesto uporabe funkcije `template` lahko uporabimo dekorator `view`, ki mu podamo ime predloge in privzete vrednosti spremenljivk.
  ```python
  @bottle.get('/pozdravi/<ime>/')
  @bottle.view('pozdravi.html')
  def pozdravi(ime):
      return dict(ime=ime)
  ```
* Dekorirana funkcija vrača slovar z vrednostmi spremenljivk.
  - Če funkcija ne vrne slovarja, se parametri dekoratorja `view` ignorirajo.
* Tak način je uporaben v kombinaciji z drugimi dekoratorji (npr. za preverjanje prijave).

---

# Funkcija `rebase`

<span class="small">

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

</span>

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

---

# Funkcije v predlogah

<span class="small">

* Poleg funkcije `rebase` so v predlogah na voljo še sledeče funkcije:
  - `include(predloga, ...)` - vključi navedeno predlogo
  - `defined(spremenljivka)` - pove, ali je spremenljivka (podana kot niz) definirana
  - `get(spremenljivka, privzeto=None)` - vrne vrednost spremenljivke oziroma privzeto vrednost
  - `setdefault(spremenljivka, privzeto)` - če spremenljivka ni definirana, jo nastavi na podano privzeto vrednost
* Lastne funkcije lahko dodajamo v slovar `BaseTemplate.defaults`.
  ```python
  bottle.BaseTemplate.defaults['povecaj'] = lambda x: x+1
  ```
  ```html
  {{povecaj(42)}}
  ```

</span>

---

# Prijava

* V bazi lahko hranimo podatke o uporabnikih aplikacije.
  - Uporabniška imena, gesla, ...
* Kako varno hraniti gesla?
  - Čistopis? Upravnik baze lahko vidi gesla uporabnikov - težave z zaupanjem!
  - Zgoščevalne funkcije? Gesla so zakrita, a lahko vsaj pogostejša gesla razkrijemo s pomočjo [mavričnih tabel](https://en.wikipedia.org/wiki/Rainbow_table).
* Rešitev: hranimo še naključno vrednost (*sol*), ki jo zgostimo skupaj z geslom.
  - Za delo z gesli so na voljo knjižnice, kot npr. `bcrypt`.
