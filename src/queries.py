import sqlite3
from pathlib import Path
import pandas as pd

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

cursor.execute("""
    SELECT
        produtos.id,
        produtos.nome,
        AVG(vendas.quantidade) as media_quantidade_vendida,
        AVG(produtos.valor * vendas.quantidade) as media_faturamento
    FROM produtos
        INNER JOIN vendas
                ON produtos.id = vendas.produto_id
            GROUP BY produtos.id,produtos.nome
            ORDER BY media_faturamento DESC
""")

media_vendas = cursor.fetchall()
print("media de vendas:")
print(media_vendas)

cursor.execute("""
    SELECT 
        AVG(quantidade) AS media_quantidade_vendida
    FROM vendas;
""")
meida_quantidade_vendida = cursor.fetchall()
print("meida quantidade vendida:")
print(meida_quantidade_vendida)

cursor.execute("""
    SELECT
        clientes.id,
        clientes.nome
        FROM clientes
        LEFT JOIN vendas
            ON clientes.id = vendas.cliente_id
        WHERE vendas.cliente_id IS NULL
""")

sem_vendas = cursor.fetchall()

print("clientes sem vendas:")
print(sem_vendas)


faturamento_mes = pd.read_sql_query("""
    SELECT
        strftime('%Y-%m', vendas.data_venda) AS mes,
        SUM(produtos.valor * vendas.quantidade) as faturamento
    FROM produtos
    INNER JOIN vendas
        ON produtos.id = produto_id
    GROUP BY strftime('%Y-%m', vendas.data_venda)
    ORDER BY mes

""", connection)

print("faturamento por mes")
print(faturamento_mes)