import tkinter as tk
from tkinter import messagebox
import database

class EstoqueApp:
    def __init__(self, master):
        # Janela Principal GUI
        self.master = master
        master.title('Gestão de Estoque (GUI)')
        master.geometry('400x200')

        database.criar_tabela()

        self.nome_var = tk.StringVar()
        self.quantidade_var = tk.IntVar()
        self.preco_var = tk.DoubleVar()
        # campo nome
        tk.Label(master, text="Nome:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        tk.Entry(master, textvariable=self.nome_var).grid(row=0, column=1, padx=10, pady=5)
        # campo quantidade
        tk.Label(master, text="Quantidade:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        tk.Entry(master, textvariable=self.quantidade_var).grid(row=1, column=1, padx=10, pady=5)
        # campo preço
        tk.Label(master, text="Preço:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        tk.Entry(master, textvariable=self.preco_var).grid(row=2, column=1, padx=10, pady=5)

        tk.Button(master,
                  text='Adicionar Produto',
                  command=self.adicionar_produto_gui
                  ).grid(row=3, column=0, columnspan=2, pady=10)

        tk.Button(master,
                  text='Visualizar Estoque (Console)',
                  command=database.visualizar_produtos()
                  ).grid(row=4, column=0, columnspan=2, pady=5)

    def adicionar_produto_gui(self):
        try:
            nome = self.nome_var.get()
            quantidade = self.quantidade_var.get()
            preco = self.preco_var.get()

            if not nome or quantidade < 0 or preco < 0:
                messagebox.showerror("Erro de Validação", "Preencha todos os campos e use valores positivos.")
                return

            if database.adicionar_produto(nome, quantidade, preco):
                messagebox.showinfo('Sucesso', f"Produto '{nome}' adicionado com sucesso!")

            self.nome_var.set("")
            self.quantidade_var.set(0)
            self.preco_var.set(0.0)

        except tk.TclError:
            messagebox.showerror('Erro de Dados', 'Quantidade e Preço devem ser números válidos.')
        except Exception as e:
            messagebox.showerror('Erro', f'Ocorreu um erro inesperado: {e}')

if __name__ == '__main__':
    root = tk.Tk()
    app = EstoqueApp(root)
    root.mainloop()
