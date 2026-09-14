from .frete import calcular_frete


def total_pedido(itens):
    subtotal = round(sum(i["preco"] * i["qtd"] for i in itens), 2)
    frete = calcular_frete(subtotal)
    return {"subtotal": subtotal, "frete": frete, "total": round(subtotal + frete, 2)}
