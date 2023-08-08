import tkinter as tk
from tkinter import ttk
import sqlite3


class ProductListWidget(ttk.Treeview):
    def __init__(self, master, products):
        super().__init__(master, columns=("Nome do Produto", "Status", "Portador"), show="headings")
        self.heading("#1", text="Nome do Produto")
        self.heading("#2", text="Status")
        self.heading("#3", text="Portador")
        self.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for product in products:
            self.insert("", "end", values=(product["nome"], product["status"], product["alocado"]))


def show_product_list(products):
    window = tk.Toplevel()
    window.title("Lista de Produtos")
    window.geometry("600x400")

    ProductListWidget(window, products)


if __name__ == "__main__":
    # Simulando os dados do banco de dados
    produtos_cadastrados = [
        {"nome": "Parafusadeira", "status": "Disponível", "alocado": "Almoxafirado"},
        {"nome": "Lixadeira", "status": "Indisponível", "alocado": "Henrique"},
        {"nome": "Martelete", "status": "Disponível", "alocado": "Almoxarifado"},
        {"nome": "Serra Circular", "status": "Indisponível", "alocado": "Dailson"},
        {"nome": "Carrinho", "status": "Disponível", "alocado": "Almoxarifado"},
    ]

    root = tk.Tk()
    root.title("Exemplo de Listagem de Produtos")
    root.geometry("300x150")

    style = ttk.Style()
    style.theme_use("clam")

    btn_show_list = ttk.Button(root, text="Mostrar Lista", command=lambda: show_product_list(produtos_cadastrados))
    btn_show_list.pack(pady=20)

    root.mainloop()
