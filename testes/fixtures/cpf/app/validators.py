import re

CPF_RE = re.compile(r"^\d{11}$")


def validar_cpf(cpf):
    if not CPF_RE.match(cpf):
        raise ValueError(f"CPF invalido: {cpf}")
    return cpf
