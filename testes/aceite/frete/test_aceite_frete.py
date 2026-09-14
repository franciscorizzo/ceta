from app.frete import calcular_frete


def test_200_exatos_paga_frete():
    assert calcular_frete(200.00) == 19.90


def test_acima_de_200_frete_gratis():
    assert calcular_frete(200.01) == 0.0
