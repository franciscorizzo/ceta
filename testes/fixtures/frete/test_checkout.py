from app.checkout import total_pedido


def test_frete_gratis_a_partir_de_200():
    r = total_pedido([{"preco": 100.00, "qtd": 2}])
    assert r["frete"] == 0.0


def test_frete_cobrado_abaixo_do_limite():
    r = total_pedido([{"preco": 50.00, "qtd": 2}])
    assert r["frete"] == 19.90
