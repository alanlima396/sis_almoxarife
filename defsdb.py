import sqlite3
import os
from utilitarios import *


class BancoDados:
    def __init__(self, nome_banco='almoxarifado.db'):
        self.nome_banco = nome_banco
        self.conexao = None

    def conectar(self):
        # Conectar ao banco de dados (criará o arquivo se não existir)
        self.conexao = sqlite3.connect(self.nome_banco)

    def desconectar(self):
        if self.conexao:
            self.conexao.close()

    def criar_tabelas(self):
        if not self.conexao:
            raise ValueError("A conexão com o banco de dados não foi estabelecida.")

        try:
            # Cria um cursor para execute comandos SQL
            cursor = self.conexao.cursor()

            # Cria a tabela usuarios
            cursor.execute('''
                        CREATE TABLE IF NOT EXISTS usuarios (
                            id INTEGER PRIMARY KEY,
                            nome TEXT UNIQUE,
                            email TEXT,
                            senha TEXT
                        )
                    ''')

            # Insere o usuário supervisor
            cursor.execute('''
                        INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)
                    ''', ("SUPERVISOR", "nzservices396@gmail.com", "Sis@369"))

            # Cria a tabela itens
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS itens (
                    id INTEGER PRIMARY KEY,
                    nome TEXT,
                    estoque INTEGER,
                    portador text,
                    status TEXT
                )
            ''')

            # Cria a tabela funcionarios
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS funcionarios (
                    id INTEGER PRIMARY KEY,
                    nome TEXT,
                    cargo TEXT
                )
            ''')

            # Cria a tabela alocacoes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS alocacoes (
                    id INTEGER PRIMARY KEY,
                    funcionario_id INTEGER,
                    item_id INTEGER,
                    data_alocacao TEXT,
                    data_devolucao TEXT,
                    quantidade_alocada INTEGER,
                    FOREIGN KEY (funcionario_id) REFERENCES funcionarios (id),
                    FOREIGN KEY (item_id) REFERENCES itens (id)
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS status_itens (
                    id INTEGER PRIMARY KEY,
                    nome TEXT NOT NULL
                )
            ''')

            # Dentro da função criar_tabelas da classe BancoDados
            # Inserir os status iniciais
            cursor.execute('''
                INSERT INTO status_itens (nome) VALUES ('Disponível')
            ''')
            cursor.execute('''
                INSERT INTO status_itens (nome) VALUES ('Indisponível')
            ''')

            # Salva as alterações
            self.conexao.commit()
        except sqlite3.Error as sqlite_error:
            notificacao(f'Erro ao interagir com o SQLite: {sqlite_error}', som=2)
        except Exception as general_error:
            print('Erro geral durante a criação do banco de dados:', general_error)
        else:
            print('Banco de dados conectado com sucesso!')

    def adicionar_usuario(self, nome, email, senha):
        cursor = self.conexao.cursor()

        try:
            cursor.execute('''
                INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)
            ''', (nome, email, senha))
            self.conexao.commit()
            print('Usuário registrado com sucesso!')
        except sqlite3.IntegrityError as e:
            print('Erro ao registrar usuário:', e)
            notificacao('Um usuário com o mesmo nome já existe.')
        except Exception as e:
            print('Erro ao registrar usuário:', e)

    def adicionar_funcioanrio(self, nome, cargo):
        cursor = self.conexao.cursor()
        cursor.execute('''
        INSERT INTO funcionarios (nome, cargo) VALUES (?, ?)
        ''', (nome, cargo))
        self.conexao.commit()

    def obter_nomes_funcionarios(self):
        cursor = self.conexao.cursor()
        cursor.execute('SELECT nome FROM funcionarios')
        nomes = [row[0] for row in cursor.fetchall()]
        return nomes

    def excluir_funcionario_por_nome(self, nome):
        cursor = self.conexao.cursor()

        try:
            cursor.execute('DELETE FROM funcionarios WHERE nome = ?', (nome,))
            if cursor.rowcount > 0:
                self.conexao.commit()
                notificacao('Funcionário excluído com sucesso!')
            else:
                notificacao(f'Funcionário "{nome}" não encontrado.')
        except sqlite3.Error as e:
            print('Erro ao excluir funcionário:', e)
        finally:
            cursor.close()  # Lembre-se de fechar o cursor

    def adicionar_produto(self, nome, status, quantia, portador):
        cursor = self.conexao.cursor()

        cursor.execute('''
            INSERT INTO itens (nome,  status, estoque, portador) VALUES (?, ?, ?, ?)
        ''', (nome, status, quantia, portador))

        self.conexao.commit()
        notificacao('Produto Registrado com Sucesso!')

    def adicionar_status(self, nome_status):
        cursor = self.conexao.cursor()

        # Verifica se o status já existe no banco de dados
        cursor.execute('SELECT nome FROM status_itens WHERE nome = ?', (nome_status,))
        existing_status = cursor.fetchone()

        if existing_status:
            notificacao(f"O status '{nome_status}' já está cadastrado.")

        else:
            cursor.execute('''
                INSERT INTO status_itens (nome) VALUES (?)
            ''', (nome_status,))
            print('Status adicionado com sucesso!')

        self.conexao.commit()

    def obter_dados(self, table, colun='nome'):
        cursor = self.conexao.cursor()

        cursor.execute(f'''
            SELECT {colun} FROM {table}
        ''')

        status = [row[0] for row in cursor.fetchall()]
        return status

    def obter_funcionarios(self):
        cursor = self.conexao.cursor()

        cursor.execute('''
              SELECT id, nome, cargo FROM funcionarios
          ''')

        funcionarios = []
        for row in cursor.fetchall():
            funcionario = {
                "id": row[0],
                "nome": row[1],
                "cargo": row[2]
            }
            funcionarios.append(funcionario)

        return funcionarios

    def carregar_produtos(self, classe):
        self.conectar()
        cursor = self.conexao.cursor()
        cursor.execute("SELECT nome, status, estoque, portador FROM itens")
        dados = cursor.fetchall()

        produtos = []

        for dado in dados:
            produtos.append(classe(*dado))

        cursor.close()
        return produtos

    def setup(self):
        if not os.path.exists(self.nome_banco):
            notificacao('Banco de dados não encontrado, o Sistema criará um.')
            self.criar_tabelas()
        self.conectar()
        self.desconectar()


#
if __name__ == '__main__':
    bd = BancoDados()
    bd.setup()
