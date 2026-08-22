import sqlite3
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "data" / "database.db"

connection = sqlite3.connect(DATABASE_PATH)
connection.execute("PRAGMA foreign_keys = ON")

maiscompra = pd.read_sql_query("""
    SELECT clientes.id, clientes.nome, SUM(vendas.quantidade) AS quantidade_comprada
    FROM clientes
    INNER JOIN vendas ON clientes.id = vendas.cliente_id
    GROUP BY clientes.id, clientes.nome
    ORDER BY quantidade_comprada DESC
""", connection)
print("Clientes que mais compram:\n", maiscompra)

maiorfaturamento = pd.read_sql_query("""
    SELECT produtos.id, produtos.nome,
           SUM(vendas.quantidade) AS quantidade_vendida,
           SUM(produtos.valor * vendas.quantidade) AS faturamento
    FROM produtos
    INNER JOIN vendas ON produtos.id = vendas.produto_id
    GROUP BY produtos.id, produtos.nome
    ORDER BY faturamento DESC
""", connection)
print("Produtos com maior faturamento:\n", maiorfaturamento)

media_vendas = pd.read_sql_query("""
    SELECT produtos.id, produtos.nome,
           AVG(vendas.quantidade) AS media_quantidade_vendida,
           AVG(produtos.valor * vendas.quantidade) AS media_faturamento
    FROM produtos
    INNER JOIN vendas ON produtos.id = vendas.produto_id
    GROUP BY produtos.id, produtos.nome
    ORDER BY media_faturamento DESC
""", connection)
print("Média de vendas:\n", media_vendas)

media_quantidade_vendida = pd.read_sql_query("""
    SELECT AVG(quantidade) AS media_quantidade_vendida FROM vendas
""", connection)
print("Média quantidade vendida:\n", media_quantidade_vendida)

sem_vendas = pd.read_sql_query("""
    SELECT clientes.id, clientes.nome
    FROM clientes
    LEFT JOIN vendas ON clientes.id = vendas.cliente_id
    WHERE vendas.cliente_id IS NULL
""", connection)
print("Clientes sem vendas:\n", sem_vendas)

faturamento_mes = pd.read_sql_query("""
    SELECT strftime('%Y-%m', vendas.data_venda) AS mes,
           SUM(produtos.valor * vendas.quantidade) AS faturamento
    FROM produtos
    INNER JOIN vendas ON produtos.id = vendas.produto_id
    GROUP BY mes
    ORDER BY mes
""", connection)
print("Faturamento por mês:\n", faturamento_mes)

connection.close()