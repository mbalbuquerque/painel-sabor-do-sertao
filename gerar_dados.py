import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
n = 5000

cidades = [
    "Recife",
    "Olinda",
    "Caruaru",
    "Petrolina",
    "Garanhuns"
]

produtos = {
    "Bebidas": [
        ("Café", 8.0),
        ("Suco de caju", 8.0),
        ("Caldo de cana", 7.0)
    ],
    "Salgados": [
        ("Coxinha", 7.5),
        ("Pastel", 8.0),
        ("Tapioca", 12.0)
    ],
    "Doces": [
        ("Bolo de rolo", 9.0),
        ("Cartola", 14.0),
        ("Cocada", 5.0)
    ],
    "Pratos": [
        ("Cuscuz com carne de sol", 22.0),
        ("Baião de dois", 28.0),
        ("Macaxeira com charque", 25.0)
    ]
}

items = [
    (categoria, produto, preco)
    for categoria, lista in produtos.items()
    for produto, preco in lista
]

idx = rng.integers(0, len(items), n)

datas = pd.to_datetime("2025-01-01") + pd.to_timedelta(
    rng.integers(0, 365, n),
    unit="D"
)

df = pd.DataFrame({
    "data": datas,
    "hora": rng.integers(7, 22, n),
    "cidade": rng.choice(
        cidades,
        n,
        p=[0.35, 0.15, 0.20, 0.20, 0.10]
    ),
    "categoria": [items[i][0] for i in idx],
    "produto": [items[i][1] for i in idx],
    "preco_unitario": [items[i][2] for i in idx],
    "quantidade": rng.integers(1, 6, n),
    "pagamento": rng.choice(
        ["PIX", "Crédito", "Débito", "Dinheiro"],
        n,
        p=[0.45, 0.25, 0.20, 0.10]
    ),
    "avaliacao": rng.integers(1, 6, n).astype(float)
})

df["total"] = (
    df["preco_unitario"] * df["quantidade"]
).round(2)

# Cria alguns valores ausentes em avaliação
df.loc[
    rng.choice(n, 60, replace=False),
    "avaliacao"
] = np.nan

df.sort_values(
    ["data", "hora"]
).to_csv(
    "vendas_sabor_do_sertao.csv",
    index=False
)

print(
    "Arquivo gerado:",
    len(df),
    "linhas"
)