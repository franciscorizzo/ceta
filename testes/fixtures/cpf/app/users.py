from .validators import validar_cpf

_db = []


def criar_usuario(payload):
    nome = payload.get("nome")
    cpf = validar_cpf(payload.get("cpf"))
    _db.append({"nome": nome, "cpf": cpf})
    return {"status": 201, "id": len(_db)}


def post_users(payload):
    try:
        return criar_usuario(payload)
    except Exception as e:
        return {"status": 500, "erro": str(e)}
