import tkinter as tk
from tkinter import ttk
from defsdb import BancoDados
from utilitarios import *
import customtkinter as ctk
from ttkthemes import ThemedStyle



class Produto:
    def __init__(self, nome, descricao, estoque, portador):
        self.nome = nome
        self.descricao = descricao
        self.estoque = estoque
        self.portador = portador



class Funcionario:
    def __init__(self, nome, email):
        self.nome = nome
        self.email = email


class Sistema:
    def __init__(self, raiz):
        self.root = raiz
        self.root.title("Exemplo de Listagem de Produtos")
        self.root.geometry("1080x720")
        self.style = ThemedStyle(self.root)
        self.style.theme_use("clam")
        self.root.protocol("WM_DELETE_WINDOW",self.fechar_janela)
        self.banco = BancoDados()
        self.banco.conectar()

        self.produtos_cadastrados = self.banco.carregar_produtos(Produto)

        btn_cadastrar_funcionario = ctk.CTkButton(self.root, text="Cadastrar Funcionário",
                                                  command=self.cadastrar_funcionario)
        btn_cadastrar_funcionario.pack(padx=30, pady=20)

        btn_cadastrar_produto = ctk.CTkButton(self.root, text="Cadastrar Produto", command=self.cadastrar_produto,
                                              height=60)
        btn_cadastrar_produto.pack(pady=20)

        btn_cadastrar_status = ctk.CTkButton(self.root, text='Cadastrar Status', command=self.new_status)
        btn_cadastrar_status.pack()



    def fechar_janela(self):
        self.banco.desconectar()  # Desconectar o banco antes de fechar
        self.root.destroy()  # Fechar a janela

    def destroy_win(self, window):
        window.destroy()

    def cadastrar_funcionario(self):
        win = tk.Toplevel()
        win.title("Cadastrar Funcionário")
        win.geometry("400x200")

        label_nome = tk.Label(win, text="Funcionário:")
        label_nome.pack()
        entry_nome = tk.Entry(win, width=50)
        entry_nome.pack()

        label_cargo = tk.Label(win, text="cargo")
        label_cargo.pack()
        entry_cargo = tk.Entry(win, width=50)
        entry_cargo.pack()

        def salvar_funcionario():
            nome = entry_nome.get().upper().strip()
            cargo = entry_cargo.get().lower().strip()

            if nome == '' or cargo == '':
                notificacao('Os Dados não podem ser vazios!')

            else:
                self.banco.adicionar_funcioanrio(nome, cargo)
                entry_nome.delete(0, tk.END)
                entry_cargo.delete(0, tk.END)

        btn_register = tk.Button(win, text="Salvar", command=lambda: salvar_funcionario(), width=10)
        btn_register.place(x=100, y=100)

        btn_sair = tk.Button(win, text="Sair", command=lambda: self.destroy_win(window=win), width=10)
        btn_sair.place(x=230, y=100)

    def cadastrar_produto(self):
        win = tk.Toplevel()
        win.title("Cadastrar Produto")
        win.geometry("500x300")

        label_nome = tk.Label(win, text="Nome do Produto:")
        label_nome.pack()
        entry_nome = tk.Entry(win, width=50)
        entry_nome.pack()

        label_status = tk.Label(win, text="Status")
        label_status.pack()
        combox_status = ttk.Combobox(win, values=self.banco.obter_dados('status_itens'))
        combox_status.pack()

        label_quantia = tk.Label(win, text="Quantia")
        label_quantia.pack()
        entry_quantia = tk.Spinbox(win, from_=0, to=10000)
        entry_quantia.pack()

        label_portador = tk.Label(win, text="Portador")
        label_portador.pack()
        combox_portador = ttk.Combobox(win, values=self.banco.obter_dados(table='funcionarios'))
        combox_portador.pack()

        def salvar_produto():
            nome = entry_nome.get().strip()
            status = combox_status.get().strip()
            quantia = entry_quantia.get()
            portador = combox_portador.get().strip()

            if nome == '' or status == '' or portador == '':
                notificacao("Os campos não podem ser vazios!")

            else:
                self.banco.adicionar_produto(nome, status, quantia, portador)

                entry_nome.delete(0, tk.END)
                combox_status.delete(0, tk.END)
                entry_quantia.delete(0, tk.END)
                combox_portador.delete(0, tk.END)

        btn_register = tk.Button(win, text="Salvar", command=lambda: salvar_produto(), width=10)
        btn_register.place(x=210, y=215)

        btn_sair = tk.Button(win, text='Sair', command=lambda: self.destroy_win(win), width=10)
        btn_sair.place(x=210, y=250)

    def show_product_list(self):
        window = tk.Toplevel()
        window.title("Lista de Produtos")
        window.geometry("600x400")

        tree = ttk.Treeview(window, columns=("Nome do Produto", "Status", "Portador"), show="headings")
        tree.heading("#1", text="Nome do Produto")
        tree.heading("#2", text="Status")
        tree.heading("#3", text="Portador")
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for produto in self.produtos_cadastrados:
            tree.insert("", "end", values=(produto.nome, produto.descricao, produto.portador))

    def new_status(self):
        win = tk.Toplevel()
        win.title("Cadastrar Status")
        win.geometry("400x200")

        lb_name = tk.Label(win, text='Novo Status:')
        lb_name.pack()

        et_status = tk.Entry(win)
        et_status.pack()

        def salvar_status():
            new = et_status.get().title()
            if new.strip() == '':
                notificacao('O Status não pode ser vazio!')

            else:
                self.banco.adicionar_status(new)
                et_status.delete(0, tk.END)

        btn_save_status = ttk.Button(win, text='Salvar', command=salvar_status)
        btn_save_status.place(x=160, y=75)

        btn_sair = ttk.Button(win, text='Sair', command=lambda: self.destroy_win(window=win))
        btn_sair.place(x=160, y=110)


if __name__ == "__main__":
    root = tk.Tk()
    sistema = Sistema(root)
    root.mainloop()
