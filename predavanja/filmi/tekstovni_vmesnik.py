#
#   Tekstovni vmesnik 
#   za delo z bazo filmi.sqlite
#
#   J. Vidali, dec. 2023
#   Prirejeno po M. Pretnar, 2019, M. Lokar, dec. 2020
#

from model import Film, Oseba


VLOGE = {'I': 'igralec', 'R': 'režiser'}
ISKAL_OSEBO = 'Iskal osebo'
POGLEDAL_DOBRE_FILME = 'Pogledal dobre filme'
SEL_DOMOV = 'Šel domov'
MOZNOSTI = [ISKAL_OSEBO, POGLEDAL_DOBRE_FILME, SEL_DOMOV]


def izpisi_vloge(igralec):
    """
    Izpiši ime igralca ter vse filme,
    pri katerih je imel vloge
    (kot režiser ali igralec).
    """
    print(igralec.ime)
    for naslov, leto, tip_vloge in igralec.poisci_vloge():
        vloga = VLOGE[tip_vloge]
        print(f'- {naslov} ({leto}, {vloga})')


def vnesi_izbiro(moznosti):
    """
    Prikaži možne izbire in vrni izbrano.

    POZOR: brez kontrole pravilnosti!!!  TODO
    """
    for i, moznost in enumerate(moznosti, 1):
        print(f'{i}) {moznost}')
    izbira = int(input('> ')) - 1
    return moznosti[izbira]


def poisci_osebo():
    """
    Zahtevaj vnos (dela) imena
    in vrni ustrezno osebo.
    """
    ime_igralca = input('Kdo te zanima? ')
    osebe = Oseba.poisci(ime_igralca)
    if len(osebe) == 1:
        return osebe[0]
    elif len(osebe) == 0:
        print('Te osebe ne najdem. Poskusi znova.')
        return poisci_osebo()
    else:
        print('Našel sem več igralcev, kateri od teh te zanima?')
        return vnesi_izbiro(osebe)


def najboljsi_filmi():
    """
    Izpiši najboljše filme za vneseno leto.
    
    TODO: kontrola smiselnosti leta
        : izbira števila izpisanih filmov
    """
    leto = input('Katero leto te zanima? ')
    filmi = Film.najboljsi_v_letu(leto)
    if filmi == []:
        print(f'Za leto {leto} ni podatkov o filmih')
        return
    for mesto, film in enumerate(filmi, 1):
        print(f'{mesto}) {film.naslov} ({film.ocena}/10)')


def glavni_meni():
    print('Pozdravljen v bazi filmov!')
    while True:
        print('Kaj bi rad delal?')
        izbira = vnesi_izbiro(MOZNOSTI)
        if izbira == ISKAL_OSEBO:
            oseba = poisci_osebo()
            izpisi_vloge(oseba)
        elif izbira == POGLEDAL_DOBRE_FILME:
            najboljsi_filmi()
        elif izbira == SEL_DOMOV:
            print('Adijo!')
            return


if __name__ == '__main__':
    glavni_meni()
