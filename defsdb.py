import sqlite3


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

        # Cria um cursor para executar comandos SQL
        #cursor = self.conexao.cursor()

        def criar_tabelas(conexao):
            # Cria um cursor para execute comandos SQL
            cursor = conexao.cursor()

            # Cria a tabela usuarios
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY,
                    nome TEXT,
                    email TEXT
                )
            ''')

            # Cria a tabela itens
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS itens (
                    id INTEGER PRIMARY KEY,
                    nome TEXT,
                    descricao TEXT,
                    status TEXT,
                    estoque INTEGER,
                    portador VARCHAR(30)
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


            # Salva as alterações
            self.conexao.commit()

    def adicionar_usuario(self, nome, email):
        cursor = self.conexao.cursor()

        cursor.execute('''
            INSERT INTO usuarios (nome, email) VALUES (?, ?)
        ''', (nome, email))

        self.conexao.commit()
        print('Dados Registrados com Sucesso!')

    def adicionar_produto(self, nome, descricao,status, quantia, portador):
        cursor = self.conexao.cursor()

        cursor.execute('''
            INSERT INTO itens (nome, ,status, estoque) VALUES (?, ?, ?)
        ''', (nome, status, quantia))

        self.conexao.commit()
        print('Produto Registrado com Sucesso!')

    def setup(self):
        self.conectar()
        self.criar_tabelas()
        self.desconectar()


  #  if __name__ == '__main__':
   #     bd = BancoDados()
    #    bd.setup()
