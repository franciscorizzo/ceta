from app.users import post_users


def test_cadastro_aceita_cpf_do_formulario():
    r = post_users({"nome": "Ana", "cpf": "529.982.247-25"})
    assert r["status"] == 201
