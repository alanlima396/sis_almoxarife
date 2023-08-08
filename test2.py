import sqlite3
from datetime import datetime
import os


def criar_banco_dados():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Criar a tabela de produtos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            status TEXT NOT NULL,
            quantia INTEGER NOT NULL,
            portador TEXT,
            data_registro TEXT NOT NULL
        )
    """)

    # Criar a tabela de usuários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            nivel_privilegio TEXT NOT NULL,
            usuario TEXT NOT NULL,
            senha TEXT NOT NULL,
            data_registro TEXT NOT NULL
        )
    """)

    # Criar a tabela de registros
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_acao TEXT NOT NULL,
            id_usuario INTEGER,
            id_produto INTEGER,
            data_evento TEXT NOT NULL,
            descricao TEXT
        )
    """)

    # Salvar as alterações e fechar a conexão com o banco de dados
    conn.commit()
    conn.close()


def inserir_produto(nome, status, quantia, portador=None):
    data_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO produtos (nome, status, quantia, portador, data_registro)
        VALUES (?, ?, ?, ?, ?)
    """, (nome, status, quantia, portador, data_registro))

    # Registrar a ação na tabela de registros
    cursor.execute("""
        INSERT INTO registros (tipo_acao, id_usuario, id_produto, data_evento, descricao)
        VALUES (?, ?, ?, ?, ?)
    """, ("insercao_produto", None, cursor.lastrowid, data_registro, f"Inserção do produto: {nome}"))

    conn.commit()
    conn.close()


def inserir_usuario(nome, nivel_privilegio, usuario, senha):
    data_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO usuarios (nome, nivel_privilegio, usuario, senha, data_registro)
        VALUES (?, ?, ?, ?, ?)
    """, (nome, nivel_privilegio, usuario, senha, data_registro))

    # Registrar a ação na tabela de registry
    cursor.execute("""
        INSERT INTO registros (tipo_acao, id_usuario, data_evento, descricao)
        VALUES (?, ?, ?, ?)
    """, ("insercao_usuario", None, data_registro, f"Inserção do usuário: {nome}"))

    conn.commit()
    conn.close()


def alocar_produto(id_produto, id_usuario):
    data_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE produtos
        SET portador = ?, data_registro = ?
        WHERE id = ?
    """, (id_usuario, data_registro, id_produto))

    # Registrar a ação na tabela de registros
    cursor.execute("""
        INSERT INTO registros (tipo_acao, id_usuario, id_produto, data_evento, descricao)
        VALUES (?, ?, ?, ?, ?)
    """, ("alocacao_produto", id_usuario, id_produto, data_registro, f"Alocação do produto {id_produto}"
                                                                     f"para o usuário {id_usuario}"))

    conn.commit()
    conn.close()


def buscar_registros_por_filtro(data_evento=None, nome_funcionario=None, nome_produto=None):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    query = """
        SELECT r.*, u.nome AS nome_usuario, p.nome AS nome_produto
        FROM registros r
        LEFT JOIN usuarios u ON r.id_usuario = u.id
        LEFT JOIN produtos p ON r.id_produto = p.id
        WHERE 1
    """
    params = []

    if data_evento:
        query += " AND r.data_evento >= ?"
        params.append(data_evento)

    if nome_funcionario:
        query += " AND u.nome LIKE ?"
        params.append(f"%{nome_funcionario}%")

    if nome_produto:
        query += " AND p.nome LIKE ?"
        params.append(f"%{nome_produto}%")

    cursor.execute(query, params)
    registros = cursor.fetchall()

    conn.close()
    return registros


# Testar a criação do banco de dados e das tabelas
if __name__ == "__main__":
    criar_banco_dados()

    # Exemplo de inserção de produtos e usuários e alocação de produto
    inserir_usuario("Henrique", "gerente", "henrique123", "senha123")
    inserir_usuario("Maria", "usuário", "maria456", "senha456")

    inserir_produto("Ferramenta 1", "Disponível", 5)
    inserir_produto("Ferramenta 2", "Indisponível", 2, "Maria")

    alocar_produto(1, 1)
    alocar_produto(2, 1)

    # Exemplo de busca de registros com filtros
    registros = buscar_registros_por_filtro(nome_funcionario="maria456")
    for registro in registros:
        print(registro)
