import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import database


class EstoqueApp:
    def __init__(self, master):
        self.master = master
        master.title("Gestão de Estoque (GUI)")
        master.geometry("650x450")

        database.criar_tabela()

        self.nome_var = tk.StringVar(master, value="")
        self.quantidade_var = tk.IntVar(master, value=0)
        self.preco_var = tk.DoubleVar(master, value=0.0)

        input_frame = tk.Frame(master)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Nome:").grid(row=0, column=0, padx=5, sticky="w")
        tk.Entry(input_frame, textvariable=self.nome_var).grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Quantidade:").grid(row=0, column=2, padx=5, sticky="w")
        tk.Entry(input_frame, textvariable=self.quantidade_var, width=10).grid(row=0, column=3, padx=5)

        tk.Label(input_frame, text="Preço:").grid(row=0, column=4, padx=5, sticky="w")
        tk.Entry(input_frame, textvariable=self.preco_var, width=10).grid(row=0, column=5, padx=5)

        tk.Button(master,
                  text="Adicionar Produto",
                  command=self.adicionar_produto_gui
                  ).pack(pady=5)


        colunas = ('id', 'nome', 'quantidade', 'preco')
        self.tabela_estoque = ttk.Treeview(master, columns=colunas, show='headings')

        self.tabela_estoque.heading('id', text='ID')
        self.tabela_estoque.heading('nome', text='Nome do Produto')
        self.tabela_estoque.heading('quantidade', text='Qtd.')
        self.tabela_estoque.heading('preco', text='Preço (R$)')

        self.tabela_estoque.column('id', width=40, anchor='center')
        self.tabela_estoque.column('nome', width=250)
        self.tabela_estoque.column('quantidade', width=80, anchor='center')
        self.tabela_estoque.column('preco', width=100, anchor='e')

        self.tabela_estoque.pack(pady=10, padx=10, fill='both', expand=True)

        tk.Button(master,
                  text="Visualizar Estoque",
                  command=self.atualizar_tabela
                  ).pack(pady=5)

        self.atualizar_tabela()

    def adicionar_produto_gui(self):
        try:
            nome = self.nome_var.get()
            quantidade = self.quantidade_var.get()
            preco = self.preco_var.get()

            if not nome or quantidade < 0 or preco < 0:
                messagebox.showerror("Erro de Validação", "Preencha o nome e use valores positivos.")
                return

            if database.adicionar_produto(nome, quantidade, preco):
                messagebox.showinfo("Sucesso", f"Produto '{nome}' adicionado com sucesso!")

                self.atualizar_tabela()

                self.nome_var.set("")
                self.quantidade_var.set(0)
                self.preco_var.set(0.0)

        except tk.TclError:
            messagebox.showerror("Erro de Dados", "Quantidade e Preço devem ser números válidos.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}")

    def atualizar_tabela(self):
        for item in self.tabela_estoque.get_children():
            self.tabela_estoque.delete(item)

        produtos = database.visualizar_produtos()

        for produto in produtos:
            produto_formatado = (produto[0], produto[1], produto[2], f"{produto[3]:.2f}")
            self.tabela_estoque.insert('', 'end', values=produto_formatado)


if __name__ == '__main__':
    root = tk.Tk()
    app = EstoqueApp(root)
    root.mainloop()
