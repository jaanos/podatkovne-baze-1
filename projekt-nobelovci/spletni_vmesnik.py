import bottle
import model

@bottle.get("/")
def zacetna_stran():
    return bottle.template('zacetek.html')

@bottle.get("/dodaj")
def dodaj():
    return bottle.template('dodaj.html')

@bottle.post("/dodaj")
def dodaj_post():
    leto = bottle.request.forms.getunicode("leto")
    tema = bottle.request.forms.getunicode("tema")
    zmagovalec = bottle.request.forms.getunicode("zmagovalec")
    model.Nobel(leto, tema, zmagovalec).dodaj_v_bazo()
    bottle.redirect("/")

@bottle.get("/izpis")
def izpis():
    od = bottle.request.query.get("od", 1901)
    do = bottle.request.query.get("do", 2008)
    return bottle.template('izpis.html', od=od, do=do, podatki=model.Nobel.poisci(od, do))

bottle.run(debug=True, reloader=True)
