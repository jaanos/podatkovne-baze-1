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
    for film, tip_vloge in igralec.poisci_vloge():
        vloga = VLOGE[tip_vloge]
        print(f'- {film.naslov} ({film.leto}, {vloga})')


def vnesi_izbiro(moznosti, izpis=lambda x: x):
    """
    Prikaži možne izbire in vrni izbrano.

    POZOR: brez kontrole pravilnosti!!!  TODO
    """
    for i, moznost in enumerate(moznosti, 1):
        print(f'{i}) {izpis(moznost)}')
    while True:
        vnos = input('> ')
        try:
            if vnos == '':
                raise KeyboardInterrupt
            izbira = int(vnos) - 1
            if izbira < 0:
                raise IndexError
            return moznosti[izbira]
        except (ValueError, IndexError):
            print("Napačna izbira, poskusi znova!")


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
    film = vnesi_izbiro(filmi, lambda film: f'{film.naslov} ({film.ocena}/10)')
    print(film)


def glavni_meni():
    print('Pozdravljen v bazi filmov!')
    while True:
        print('Kaj bi rad delal?')
        try:
            izbira = vnesi_izbiro(MOZNOSTI)
        except KeyboardInterrupt:
            izbira = SEL_DOMOV
        if izbira == ISKAL_OSEBO:
            try:
                oseba = poisci_osebo()
                izpisi_vloge(oseba)
            except KeyboardInterrupt:
                continue
        elif izbira == POGLEDAL_DOBRE_FILME:
            najboljsi_filmi()
        elif izbira == SEL_DOMOV:
            print('Adijo!')
            return


if __name__ == '__main__':
    glavni_meni()
