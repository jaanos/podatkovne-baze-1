from pomozne_funkcije import Meni, JaNe, prekinitev
from model import Film, Oseba


def vnesi_izbiro(moznosti):
    """
    Uporabniku da na izbiro podane možnosti.
    """
    moznosti = list(moznosti)
    for i, moznost in enumerate(moznosti, 1):
        print(f'{i}) {moznost}')
    izbira = None
    while True:
        try:
            izbira = int(input('> ')) - 1
            return moznosti[izbira]
        except (ValueError, IndexError):
            print("Napačna izbira!")


def izpisi_vloge(igralec):
    """
    Izpiše vse vloge podanega igralca.
    """
    print(igralec.ime)
    for naslov, leto, vloga in igralec.poisci_vloge():
        print(f'- {naslov} ({leto}, {vloga})')


def poisci_osebo():
    """
    Poišče osebo, ki jo vnese uporabnik.
    """
    while True:
        ime_igralca = input('Kdo te zanima? ')
        osebe = list(Oseba.poisci(ime_igralca))
        if len(osebe) == 1:
            return osebe[0]
        elif len(osebe) == 0:
            print('Te osebe ne najdem. Poskusi znova.')
        else:
            print('Našel sem več igralcev, kateri od teh te zanima?')
            return vnesi_izbiro(osebe)


@prekinitev
def iskanje_osebe():
    """
    Izpiše vloge za osebo, ki jo vnese uporabnik.
    """
    oseba = poisci_osebo()
    izpisi_vloge(oseba)


@prekinitev
def najboljsi_filmi():
    """
    Izpiše najboljših 10 filmov v letu, ki ga vnese uporabnik.
    """
    leto = input('Katero leto te zanima? ')
    filmi = Film.najboljsi_v_letu(leto)
    for mesto, film in enumerate(filmi, 1):
        print(f'{mesto}) {film.naslov} ({film.ocena}/10)')


@prekinitev
def dodajanje_osebe():
    """
    Doda osebo z imenom, ki ga vnese uporabnik.
    """
    ime = input('Napiši ime osebe, ki jo želiš dodati: ')
    oseba = Oseba(ime)
    oseba.dodaj_v_bazo()
    print(f'Oseba {ime} dodana z ID-jem {oseba.id}.')


@prekinitev
def dodajanje_filma():
    """
    Doda film s podatki, ki jih vnese uporabnik.
    """
    naslov = input("Napiši naslov filma: ")
    leto = None
    while leto is None:
        try:
            leto = int(input("Napiši leto: "))
        except ValueError:
            print("Leto mora biti celo število!")
    ocena = None
    while ocena is None:
        try:
            ocena = float(input("Napiši oceno: "))
        except ValueError:
            print("Ocena mora biti število!")
    reziserji = []
    while True:
        print("Ali želiš dodati režiserja?")
        dodaj = vnesi_izbiro(JaNe)
        if dodaj == JaNe.NE:
            break
        oseba = poisci_osebo()
        reziserji.append(oseba)
        print(f"Dodan režiser {oseba.ime}.")
    igralci = []
    while True:
        print("Ali želiš dodati igralca?")
        dodaj = vnesi_izbiro(JaNe)
        if dodaj == JaNe.NE:
            break
        oseba = poisci_osebo()
        igralci.append(oseba)
        print(f"Dodan igralec {oseba.ime}.")
    film = Film(naslov, leto, ocena)
    film.dodaj_v_bazo(reziserji, igralci)
    print(f'Film {naslov} ({leto}) dodan z ID-jem {film.id}.')


def domov():
    """
    Pozdravi pred izhodom.
    """
    print('Adijo!')


class GlavniMeni(Meni):
    """
    Izbire v glavnem meniju.
    """
    ISKAL_OSEBO = ('Iskal osebo', iskanje_osebe)
    POGLEDAL_DOBRE_FILME = ('Pogledal dobre filme', najboljsi_filmi)
    DODAL_OSEBO = ('Dodal osebo', dodajanje_osebe)
    DODAL_FILM = ('Dodal film', dodajanje_filma)
    SEL_DOMOV = ('Šel domov', domov)


@prekinitev
def glavni_meni():
    """
    Prikazuje glavni meni, dokler uporabnik ne izbere izhoda.
    """
    print('Pozdravljen v bazi filmov!')
    while True:
        print('Kaj bi rad delal?')
        izbira = vnesi_izbiro(GlavniMeni)
        izbira.funkcija()
        if izbira == GlavniMeni.SEL_DOMOV:
            return


glavni_meni()