import os
import hashlib
import hmac


def zgosti(geslo, sol):
    """
    Vrne zgostitev gesla pri podani soli.

    Uporabi funkcijo PBKDF2_HMAC za izpeljavo ključa
    z zgoščevalno funkcijo SHA256 in 100000 ponovitvami.
    """
    return hashlib.pbkdf2_hmac('sha256', geslo.encode('utf-8'), sol, 100000)


def sifriraj_geslo(geslo):
    """
    Vrne zgoščeno geslo skupaj z uporabljeno soljo.
    """
    sol = os.urandom(32)
    zgostitev = zgosti(geslo, sol)
    return (zgostitev.hex(), sol.hex())


def preveri_geslo(geslo, zgostitev, sol):
    """
    Preveri, ali podano geslo ustreza podani zgostitvi in soli.
    """
    try:
        return hmac.compare_digest(bytes.fromhex(zgostitev),
                                   zgosti(geslo, bytes.fromhex(sol)))
    except ValueError:
        return False
