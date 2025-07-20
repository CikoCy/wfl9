import random

def calcola_pesi_adattivi(successi, errori, base=1.0):
    """
    Calcola un dizionario di pesi combinando successi ed errori.
    Pesi più alti ai numeri con più successi e meno errori.
    """
    pesi = {}

    for n in range(1, 21):
        s = successi.get(n, 0)
        e = errori.get(n, 0)

        # Formula: base + (successi * 2) - (errori * 1.5)
        peso = base + (s * 2) - (e * 1.5)
        peso = max(peso, 0.1)  # evita peso 0 o negativo
        pesi[n] = peso

    return pesi


def genera_previsione_con_pesi(pesi, k=10):
    """
    Genera k numeri univoci da 1 a 20 in base ai pesi forniti.
    """
    numeri = list(pesi.keys())
    probabilita = [pesi[n] for n in numeri]

    predetti = set()
    while len(predetti) < k:
        scelto = random.choices(numeri, weights=probabilita, k=1)[0]
        predetti.add(scelto)

    return list(predetti)
