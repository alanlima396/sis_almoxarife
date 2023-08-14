import tkinter as tk
from tkinter import ttk
from defsdb import BancoDados
from utilitarios import *


class Produto:
    def __init__(self, nome, status, quantia, portador, data_registro):
        self.nome = nome
        self.status = status
        self.quantia = quantia
        self.portador = portador
        self.data_registro = data_registro


class Funcionario:
    def __init__(self, nome, email):
        self.nome = nome
        self.email = email


class Sistema:
    def __init__(self, raiz):
        self.root = raiz
        self.root.title("Exemplo de Listagem de Produtos")
        self.root.geometry("1080x720")
        self.style = ttk.Style()
        self.style.theme_use("winnative")

        self.banco = BancoDados()
        self.banco.conectar()

        self.produtos_cadastrados = [
            Produto("Parafusadeira", "Disponível", 5, "Almoxarifado", "2023-08-10"),
            Produto("Lixadeira", "Indisponível", 3, "Henrique", "2023-08-09"),
            # Adicione outros produtos aqui
        ]

        btn_cadastrar_funcionario = ttk.Button(self.root, text="Cadastrar Funcionário",
                                               command=self.cadastrar_funcionario)
        btn_cadastrar_funcionario.pack(padx=30, pady=20)

        btn_cadastrar_produto = ttk.Button(self.root, text="Cadastrar Produto", command=self.cadastrar_produto)
        btn_cadastrar_produto.pack(pady=20)

        btn_cadastrar_status = ttk.Button(self.root, text='Cadastrar Status', command=self.new_status)
        btn_cadastrar_status.pack()

    def destroy_win(self, window):
        self.banco.desconectar()
        window.destroy()

    def cadastrar_funcionario(self):
        win = tk.Toplevel()
        win.title("Cadastrar Funcionário")
        win.geometry("600x400")

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

            if nome and cargo == '':
                notificacao('Os Dados não podem ser vazios!')

            else:
                self.banco.adicionar_funcioanrio(nome, cargo)
                entry_nome.delete(0, tk.END)
                entry_cargo.delete(0, tk.END)

        btn_register = tk.Button(win, text="Salvar", command=lambda: salvar_funcionario(), width=10)
        btn_register.place(x=275, y=110)

        btn_sair = tk.Button(win, text="Sair", command=lambda: self.destroy_win(window=win), width=10)
        btn_sair.place(x=275, y=150)

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
        combox_status = ttk.Combobox(win, values=self.banco.obter_status())
        combox_status.pack()

        label_quantia = tk.Label(win, text="Quantia")
        label_quantia.pack()
        entry_quantia = tk.Entry(win, width=50)
        entry_quantia.pack()

        label_portador = tk.Label(win, text="Portador")
        label_portador.pack()
        entry_portador = tk.Entry(win, width=50)
        entry_portador.pack()

        def salvar_produto():
            nome = entry_nome.get()
            status = combox_status.get()
            quantia = int(entry_quantia.get())
            portador = entry_portador.get()
            data_registro = data_now()

            novo_produto = Produto(nome, status, quantia, portador, data_registro)
            self.produtos_cadastrados.append(novo_produto)

            self.banco.adicionar_produto(nome, status, quantia, portador, data_registro)

            entry_nome.delete(0, tk.END)
            combox_status.delete(0, tk.END)
            entry_quantia.delete(0, tk.END)
            entry_portador.delete(0, tk.END)

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
            tree.insert("", "end", values=(produto.nome, produto.status, produto.portador))

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
