FRETE_PADRAO = 19.90
LIMITE_FRETE_GRATIS = 200.00


def calcular_frete(subtotal):
    if subtotal > LIMITE_FRETE_GRATIS:
        return 0.0
    return FRETE_PADRAO
