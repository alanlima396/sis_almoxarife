import datetime
import winsound
import win32api
import win32con
import customtkinter as ctk

# Agora você pode usar as funções e constantes dos módulos win32api e win32con


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
    root = ctk.CTk()
    root.iconbitmap('notify.ico')
    root.title("Notificação")
    root.resizable(False, False)

    label = ctk.CTkLabel(root, text=mensagem, font=("Arial", 20), width=30, height=5)
    label.pack(padx=10, pady=10)

    button = ctk.CTkButton(root, text="Fechar", width=40, height=35, corner_radius=10, command=root.destroy,
                           fg_color='#F5FF00', text_color='#000000', hover_color='#FFAA00')
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
