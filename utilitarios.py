import datetime
import winsound
import win32api
import win32con
import tkinter as tk
from tkinter import ttk


def data_now():
    data_atual = datetime.datetime.now()
    data_formatada = data_atual.strftime("%Y-%m-%d %H:%M:%S")
    return data_formatada


def notificacao(mensagem='Dados Inválidos', som=1):
    # Som da Notificação.
    if som == 1:
        win32api.MessageBeep(win32con.MB_ICONERROR)
    else:
        winsound.PlaySound("SystemExclamation", winsound.SND_ASYNC)
    # Janela da Notificação.
    root = tk.Tk()
    root.iconbitmap('notify.ico')
    root.title("Notificação")
    root.resizable(False, False)

    label = tk.Label(root, text=mensagem, font=("Arial", 12))
    label.pack(padx=10, pady=10)

    button = tk.Button(root, text="Fechar", width=10, command=root.destroy)
    button.pack(padx=5, pady=5)

    # Obter a largura e altura da janela
    window_width = root.winfo_width()
    window_height = root.winfo_height()

    # Obter a largura e altura da tela
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calcular as coordenadas x e y para centralizar a janela
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Definir a posição da janela
    root.geometry(f"+{x}+{y}")

    root.mainloop()


def centralizar_janela(janela):
    largura_janela = janela.winfo_reqwidth()  # Largura desejada da janela
    altura_janela = janela.winfo_reqheight()  # Altura desejada da janela

    # Obtém as dimensões da tela do monitor
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()

    # Calculi as coordenadas de posicionamento para centralizar a janela
    x = (largura_tela - largura_janela) // 2
    y = (altura_tela - altura_janela) // 2

    janela.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")


def atualizar_lista(entry, lista, nomes):
    termo_busca = entry.get().strip().lower()
    lista.delete(0, tk.END)

    if termo_busca:
        resultados = [item for item in nomes if termo_busca in item.lower()]
        for resultado in resultados:
            lista.insert(tk.END, resultado)
    else:
        # Se o campo de busca estiver vazio, mostrar todos os itens
        for item in nomes:
            lista.insert(tk.END, item)


def vincular_nome(listbox, entry):
    selected_item = listbox.get(tk.ACTIVE)  # Obtém o item selecionado
    entry.delete(0, tk.END)  # Limpa  Entry
    entry.insert(0, selected_item)  # Insere o nome selecionado na Entry


def alocar(master, banco):
    frame = tk.Frame(master, width=800, height=300)
    frame.place(x=200, y=30)

    nomes_itens = banco.obter_dados(table='itens')
    nomes_funcionarios = banco.obter_dados(table='funcionarios')

    entry_itens = ttk.Entry(frame, width=20)
    entry_itens.place(x=25, y=30)

    entry_nomes = ttk.Entry(frame)
    entry_nomes.place(x=175, y=30)

    listbox_itens = tk.Listbox(frame)
    listbox_itens.place(x=25, y=50)

    listbox_funcionarios = tk.Listbox(frame)
    listbox_funcionarios.place(x=175, y=50)

    entry_itens.bind("<KeyRelease>", lambda event: atualizar_lista(entry_itens, listbox_itens, nomes_itens))
    listbox_itens.bind("<Button-1>", lambda event: vincular_nome(listbox_itens, entry_itens))

    entry_nomes.bind("<KeyRelease>", lambda event: atualizar_lista(entry_nomes, listbox_funcionarios,
                                                                   nomes_funcionarios))
    listbox_funcionarios.bind("<KeyRelease>", lambda event: vincular_nome(listbox_funcionarios, entry_nomes))

    btn_sair = tk.Button(frame, text='Sair', command=frame.destroy)
    btn_sair.place(x=15, y=220)


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
