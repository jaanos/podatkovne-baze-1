#
#   Tekstovni vmesnik 
#   za delo z bazo filmi.sqlite
#
#   J. Vidali, nov. 2024
#   Prirejeno po M. Pretnar, 2019, M. Lokar, dec. 2020
#

from enum import Enum
from model import Film, Oseba


class Meni(Enum):
    ISKAL_OSEBO = 'Iskal osebo'
    POGLEDAL_DOBRE_FILME = 'Pogledal dobre filme'
    SEL_DOMOV = 'Šel domov'


def vnesi_izbiro(moznosti, izpis=lambda x: x):
    """
    Prikaži možne izbire in vrni izbrano.

    POZOR: brez kontrole pravilnosti!!!  TODO
    """
    moznosti = list(moznosti)
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


def izpisi_vloge(igralec):
    """
    Izpiši ime igralca ter vse filme,
    pri katerih je imel vloge
    (kot režiser ali igralec).
    """
    print(igralec.ime)
    for vloga in igralec.poisci_vloge():
        print(f'- {vloga.film.naslov} ({vloga.film.leto}, {vloga.tip_vloge})')


def poisci_osebo():
    """
    Zahtevaj vnos (dela) imena
    in vrni ustrezno osebo.
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


def najboljsi_filmi():
    """
    Izpiši najboljše filme za vneseno leto.
    
    TODO: kontrola smiselnosti leta
        : izbira števila izpisanih filmov
        : izpis seznama igralcev in režiserjev
    """
    leto = input('Katero leto te zanima? ')
    filmi = list(Film.najboljsi_v_letu(leto))
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
            izbira = vnesi_izbiro(Meni, lambda x: x.value)
        except KeyboardInterrupt:
            izbira = Meni.SEL_DOMOV
        if izbira == Meni.ISKAL_OSEBO:
            try:
                oseba = poisci_osebo()
                izpisi_vloge(oseba)
            except KeyboardInterrupt:
                continue
        elif izbira == Meni.POGLEDAL_DOBRE_FILME:
            najboljsi_filmi()
        elif izbira == Meni.SEL_DOMOV:
            print('Adijo!')
            return


if __name__ == '__main__':
    glavni_meni()
