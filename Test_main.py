from tkinter import ttk
from defsdb import BancoDados
from utilitarios import *
from PIL import Image, ImageTk
from ttkthemes import ThemedStyle
from tkinter import messagebox


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


def destroy_win(window):
    window.destroy()


def mostrar_funcionarios(local, funcionarios):
    # Aqui você pode criar uma nova janela ou um frame para mostrar a lista de funcionários
    # Por exemplo, você pode usar uma Treeview para exibir os funcionários em uma tabela
    # Certifique-se de configurar as colunas adequadamente
    frame_tree = tk.Frame(local, width=700, height=300)
    frame_tree.place(x=140, y=0)

    tree = ttk.Treeview(frame_tree, columns=("ID", "Nome", "Cargo"), show="headings")

    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.heading("Cargo", text="Cargo")
    tree.pack()

    for funcionario in funcionarios:
        tree.insert("", "end", values=(funcionario["id"], funcionario["nome"], funcionario["cargo"]))

    btn_exit = tk.Button(frame_tree, text='Quit', command=frame_tree.destroy, width=10)
    btn_exit.place(x=520, y=200)


def alocar(master, banco):
    frame = tk.Frame(master, width=800, height=300)
    frame.place(x=200, y=30)

    nomes_itens = banco.obter_dados(table='itens')
    nomes_funcionarios = banco.obter_dados(table='funcionarios')

    entry_busca = ttk.Entry(frame, width=20)
    entry_busca.place(x=25, y=30)

    entry_nomes = ttk.Entry(frame)
    entry_nomes.place(x=175, y=30)

    lista_resultados = tk.Listbox(frame)
    lista_resultados.place(x=25, y=50)

    def atualizar_lista(event):
        termo_busca = entry_busca.get().strip().lower()
        lista_resultados.delete(0, tk.END)

        if termo_busca:
            resultados = [item for item in nomes_itens if termo_busca in item.lower()]
            for resultado in resultados:
                lista_resultados.insert(tk.END, resultado)

        else:
            # Se o campo de busca estiver vazio, mostrar todos os itens
            for item in nomes_itens:
                lista_resultados.insert(tk.END, item)

    def vincular_nome(event):
        selected_item = lista_resultados.get(tk.ACTIVE)  # Obtém o item selecionado
        entry_busca.delete(0, tk.END)  # Limpa  Entry
        entry_busca.insert(0, selected_item)  # Insere o nome selecionado na Entry

    entry_busca.bind("<KeyRelease>", atualizar_lista)
    lista_resultados.bind("<Button-1>", vincular_nome)  # Vincula o evento de clique

    btn_sair = tk.Button(frame, text='Sair', command=frame.destroy)
    btn_sair.place(x=15, y=220)


class Sistema:
    def __init__(self, raiz):
        self.root = raiz
        self.root.title("NZservices")
        self.root.iconbitmap('ico_logo.ico')
        self.root.geometry("1100x600")
        self.root.resizable(False, False)
        self.style = ThemedStyle(self.root)
        self.style.theme_use("clam")
        self.root.protocol("WM_DELETE_WINDOW", self.fechar_janela)
        self.root.configure(bg="#00AAFF")
        self.banco = BancoDados()
        self.banco.setup()
        self.banco.conectar()
        self.produtos_cadastrados = self.banco.carregar_produtos(Produto)

        # Defer a criação da PhotoImage
        self.photo = None

        # carregar imagens:
        self.load_image()

        btn_funcionario = tk.Button(self.root, text="Funcionários", height=3, width=18,
                                    command=self.funcionarios)
        btn_funcionario.place(x=25, y=50)

        btn_cadastrar_produto = tk.Button(self.root, text="Produto", command=self.produtos,
                                          height=3, width=18)
        btn_cadastrar_produto.place(x=25, y=150)

        btn_cadastrar_status = tk.Button(self.root, text='Cadastrar Status', height=3, width=18, command=self.new_status
                                         )
        btn_cadastrar_status.place(x=25, y=250)

    # Defs Para Lidar com janela.
    def load_image(self):
        imagem = Image.open('background1.png')
        self.photo = ImageTk.PhotoImage(imagem)
        label_img = tk.Label(self.root, image=self.photo)
        label_img.place(x=50, y=36)

    def fechar_janela(self):
        self.banco.desconectar()  # Desconectar o banco antes de fechar
        self.root.destroy()  # Fechar a janela

    # Defs para lidar com funcionários
    def funcionarios(self):
        frame = tk.Frame(self.root, width=800, height=300)
        frame.place(x=200, y=30)

        background01 = tk.Label(frame, width=120, height=50, bg='#005AFF')
        background01.place(x=0, y=0)

        background02 = tk.Label(frame, width=16, height=16, bg='#0000FF')
        background02.place(x=0, y=0)

        btn_view = ttk.Button(frame, text='Visualizar', command=lambda: self.visualizar_funcionarios(frame))
        btn_view.place(x=10, y=20)

        btn_cadastrar = ttk.Button(frame, text='Cadastrar', command=self.cadastrar_funcionario)
        btn_cadastrar.place(x=10, y=60)

        btn_excluir_funcionario = ttk.Button(frame, text='Excluir', command=lambda: self.excluir_funcionario(frame))
        btn_excluir_funcionario.place(x=10, y=100)

        btn_voltar = tk.Button(frame, text='Voltar', width=12, command=lambda: frame.destroy())
        btn_voltar.place(x=10, y=210)

    def excluir_funcionario(self, master):
        def confirmar_exclusao():
            nome = combobox.get()
            if nome:
                resposta = messagebox.askyesno("Confirmar Exclusão",
                                               f"Tem certeza que deseja excluir o funcionário {nome}?")
                if resposta:
                    self.banco.excluir_funcionario_por_nome(nome)
                    frame_excluir.destroy()
            else:
                notificacao('Os campos não podem ser vazios!')

        frame_excluir = tk.Frame(master, width=200, height=150)
        frame_excluir.place(x=250, y=50)

        combobox = ttk.Combobox(frame_excluir, width=26, values=self.banco.obter_nomes_funcionarios())
        combobox.place(x=10, y=10)

        btn_excluir = ttk.Button(frame_excluir, text='Deletar Funcionário', command=lambda: confirmar_exclusao())
        btn_excluir.place(x=30, y=40)

        btn_cancelar = ttk.Button(frame_excluir, text='Cancelar', command=frame_excluir.destroy, width=17)
        btn_cancelar.place(x=30, y=90)

    def cadastrar_funcionario(self):
        win = tk.Toplevel()
        win.title("Cadastrar Funcionário")

        win.resizable(False, False)
        win.geometry('400x200')

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

        btn_sair = tk.Button(win, text="Sair", command=lambda: destroy_win(window=win), width=10)
        btn_sair.place(x=230, y=100)

    def visualizar_funcionarios(self, master):
        funcionarios = self.banco.obter_funcionarios()
        mostrar_funcionarios(master, funcionarios)

    # Defs para Lidar com produtos:

    def produtos(self):
        frame = tk.Frame(self.root, width=800, height=300)
        frame.place(x=200, y=30)

        bg = tk.Label(frame, width=120, height=20, bg='#00FF50')
        bg.place(x=0, y=0)

        background01 = tk.Label(frame, width=16, height=18, bg='#32CD32')
        background01.place(x=0, y=5)

        btn_listar = ttk.Button(frame, text='Listar Itens', command=lambda: self.show_product_list(frame))
        btn_listar.place(x=10, y=20)

        btn_alocar = ttk.Button(frame, text='Alocar', command=lambda: alocar(frame, self.banco))
        btn_alocar.place(x=10, y=60)

        btn_cadastrar = ttk.Button(frame, text='Cadastrar', command=self.cadastrar_produto)
        btn_cadastrar.place(x=10, y=100)

        btn_excluir = ttk.Button(frame, text='Excluir Itens')
        btn_excluir.place(x=10, y=140)

        btn_closer = tk.Button(frame, text='Close', width=13, command=frame.destroy)
        btn_closer.place(x=8, y=250)

    def cadastrar_produto(self):
        win = tk.Toplevel()
        win.title("Cadastrar Produto")
        win.geometry("500x300")
        win.resizable(False, False)

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
                try:
                    if status not in combox_status['values']:
                        notificacao(f"Status '{status}' inválido!")
                    elif portador not in combox_portador['values']:
                        notificacao(f"Portador '{portador}' inválido!")
                    else:
                        self.banco.adicionar_produto(nome, status, quantia, portador)
                        entry_nome.delete(0, tk.END)
                        combox_status.delete(0, tk.END)
                        entry_quantia.delete(0, tk.END)
                        combox_portador.delete(0, tk.END)
                except Exception as e:
                    notificacao(f"Erro: {str(e)}")

        btn_register = tk.Button(win, text="Salvar", command=salvar_produto, width=10)
        btn_register.place(x=210, y=215)

        btn_sair = tk.Button(win, text='Sair', command=win.destroy, width=10)
        btn_sair.place(x=210, y=250)

    def show_product_list(self, master):
        frame_show = tk.Frame(master, width=800, height=300)
        frame_show.place(x=150, y=0)

        self.produtos_cadastrados = self.banco.carregar_produtos(Produto)

        tree = ttk.Treeview(frame_show, columns=("Nome do Produto", "Status", "Portador"), show="headings")
        tree.heading("#1", text="Nome do Produto")
        tree.heading("#2", text="Status")
        tree.heading("#3", text="Portador")
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for produto in self.produtos_cadastrados:
            tree.insert("", "end", values=(produto.nome, produto.descricao, produto.portador))

        btn_quit = tk.Button(frame_show, text='Quit', command=frame_show.destroy)
        btn_quit.place(x=570, y=200)

    def new_status(self):
        win = tk.Toplevel()
        win.title("Cadastrar Status")
        win.geometry("400x200")
        win.resizable(False, False)

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

        btn_sair = ttk.Button(win, text='Sair', command=lambda: destroy_win(window=win))
        btn_sair.place(x=160, y=110)


if __name__ == "__main__":
    db = BancoDados()
    db.setup()
    root = tk.Tk()
    sistema = Sistema(root)
    root.mainloop()
