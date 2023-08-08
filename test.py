import tkinter as tk
from tkinter import ttk


class TriView(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Tri View")
        self.geometry("500x300")
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)

        self.page1 = tk.Frame(self.notebook, bg='red')
        tk.Label(self.page1, text="View 1", font=("Arial", 20)).pack(padx=20, pady=20)
        self.page2 = tk.Frame(self.notebook, bg='green')
        tk.Label(self.page2, text="View 2", font=("Arial", 20)).pack(padx=20, pady=20)
        self.page3 = tk.Frame(self.notebook, bg='blue')
        tk.Label(self.page3, text="View 3", font=("Arial", 20)).pack(padx=20, pady=20)

        self.notebook.add(self.page1, text='View 1')
        self.notebook.add(self.page2, text='View 2')
        self.notebook.add(self.page3, text='View 3')


# Exemplo de uso
if __name__ == "__main__":
    tri_view = TriView()
    tri_view.mainloop()
