import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "data" / "database.db"

connection = sqlite3.connect(DATABASE_PATH)
connection.execute("PRAGMA foreign_keys = ON")

cursor = connection.cursor()

# Clientes
clientes = [
    ("Hugo",),
    ("Ana",),
    ("Carlos",),
    ("Mariana",),
    ("Pedro",),
]

cursor.executemany(
    "INSERT INTO clientes (nome) VALUES (?)",
    clientes
)

# Produtos
produtos = [
    ("Lapis", 1.00),
    ("Caderno", 15.00),
    ("Caneta", 3.50),
    ("Mochila", 120.00),
    ("Fone de ouvido", 80.00),
]

cursor.executemany(
    "INSERT INTO produtos (nome, valor) VALUES (?, ?)",
    produtos
)

# Vendas
vendas = [
    (1, 1, "2026-06-05", 10),
    (2, 2, "2026-06-07", 3),
    (1, 4, "2026-06-15", 1),
    (3, 3, "2026-06-20", 8),
    (2, 5, "2026-07-02", 2),
    (4, 2, "2026-07-10", 5),
    (1, 3, "2026-07-18", 10),
    (3, 4, "2026-07-25", 2),
    (4, 5, "2026-08-03", 1),
    (2, 1, "2026-08-12", 20),
]

cursor.executemany(
    """
    INSERT INTO vendas (
        cliente_id,
        produto_id,
        data_venda,
        quantidade
    )
    VALUES (?, ?, ?, ?)
    """,
    vendas
)

connection.commit()
connection.close()