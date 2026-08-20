import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "data" / "database.db"

connection = sqlite3.connect(DATABASE_PATH)
connection.execute("PRAGMA foreign_keys = ON")

cursor = connection.cursor()

cursor.execute(""" 
SELECT 
    clientes.id,
    clientes.nome,
    SUM(vendas.quantidade) as quantidade_comprada
FROM clientes
    INNER JOIN vendas
        ON clientes.id = vendas.cliente_id
    GROUP BY clientes.id,clientes.nome
    ORDER BY quantidade_comprada DESC
""")

maiscompra = cursor.fetchall()

print("Clientes que mais compram:")
print(maiscompra)

cursor.execute("""
    SELECT
        produtos.id,
        produtos.nome,
        SUM(vendas.quantidade) as quantidade_vendida,
        SUM(produtos.valor * vendas.quantidade) as faturamento
    FROM produtos
        INNER JOIN vendas
            ON produtos.id = vendas.produto_id
        GROUP BY produtos.id,produtos.nome
        ORDER BY faturamento DESC

""")

maiorfaturamento = cursor.fetchall()
print("produtos com maior faturamento:")
print(maiorfaturamento)