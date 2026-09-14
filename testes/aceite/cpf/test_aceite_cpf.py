from app import users


def test_grava_cpf_so_com_digitos():
    r = users.post_users({"nome": "Ana", "cpf": "529.982.247-25"})
    assert r["status"] == 201
    assert users._db[-1]["cpf"] == "52998224725"
