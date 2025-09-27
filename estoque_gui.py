import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import database


class EstoqueApp:
    def __init__(self, master):
        self.master = master
        master.title("Gestão de Estoque (GUI)")
        master.geometry("750x550")  # Aumentei um pouco a largura para o novo botão

        database.criar_tabela()

        self.nome_var = tk.StringVar(master, value="")
        self.quantidade_var = tk.IntVar(master, value=0)
        self.preco_var = tk.DoubleVar(master, value=0.0)
        self.produto_selecionado_id = None

        input_frame = tk.Frame(master)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Nome:").grid(row=0, column=0, padx=5, sticky="w")
        self.entry_nome = tk.Entry(input_frame, textvariable=self.nome_var)
        self.entry_nome.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Quantidade:").grid(row=0, column=2, padx=5, sticky="w")
        self.entry_quantidade = tk.Entry(input_frame, textvariable=self.quantidade_var, width=10)
        self.entry_quantidade.grid(row=0, column=3, padx=5)

        tk.Label(input_frame, text="Preço:").grid(row=0, column=4, padx=5, sticky="w")
        self.entry_preco = tk.Entry(input_frame, textvariable=self.preco_var, width=10)
        self.entry_preco.grid(row=0, column=5, padx=5)

        button_frame = tk.Frame(master)
        button_frame.pack(pady=5)

        self.btn_adicionar = tk.Button(button_frame,
                                       text="Adicionar Novo",
                                       command=self.adicionar_produto_gui,
                                       width=15
                                       )
        self.btn_adicionar.pack(side=tk.LEFT, padx=10)

        tk.Button(button_frame,
                  text="Atualizar Item",
                  command=self.atualizar_produto_gui,
                  width=15
                  ).pack(side=tk.LEFT, padx=10)

        tk.Button(button_frame,
                  text="Deletar Item",
                  command=self.deletar_produto_gui,
                  width=15
                  ).pack(side=tk.LEFT, padx=10)

        # NOVO: Botão de Recarregar
        tk.Button(button_frame,
                  text="Recarregar Estoque",
                  command=self.atualizar_tabela,
                  width=18
                  ).pack(side=tk.LEFT, padx=10)

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

        self.tabela_estoque.bind('<<TreeviewSelect>>', self.selecionar_item)

        self.atualizar_tabela()

    def selecionar_item(self, event):
        try:
            item_selecionado = self.tabela_estoque.focus()
            if not item_selecionado:
                return

            valores = self.tabela_estoque.item(item_selecionado, 'values')

            self.produto_selecionado_id = int(valores[0])

            self.nome_var.set(valores[1])
            self.quantidade_var.set(int(valores[2]))

            preco_str = valores[3].replace('R$ ', '').replace(',', '.')
            self.preco_var.set(float(preco_str))

        except Exception as e:
            print(f"Erro ao selecionar item: {e}")
            self.limpar_campos()

    def limpar_campos(self):
        """Limpa as variáveis de controle e reseta o ID selecionado."""
        self.produto_selecionado_id = None
        self.nome_var.set("")
        self.quantidade_var.set(0)
        self.preco_var.set(0.0)

    def atualizar_produto_gui(self):
        """
        Lida com a lógica de atualização do produto.
        """
        if self.produto_selecionado_id is None:
            messagebox.showwarning("Atenção", "Selecione um produto na tabela para atualizar.")
            return

        try:
            nome = self.nome_var.get()
            quantidade = self.quantidade_var.get()
            preco = self.preco_var.get()

            if not nome or quantidade < 0 or preco < 0:
                messagebox.showerror("Erro de Validação", "Preencha todos os campos e use valores positivos.")
                return

            database.atualizar_produto(self.produto_selecionado_id, quantidade, preco)

            messagebox.showinfo("Sucesso", f"Produto ID {self.produto_selecionado_id} atualizado.")
            self.limpar_campos()
            self.atualizar_tabela()

        except tk.TclError:
            messagebox.showerror("Erro de Dados", "Quantidade e Preço devem ser números válidos.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}")

    def deletar_produto_gui(self):
        """
        Lida com a lógica de deleção do produto.
        """
        if self.produto_selecionado_id is None:
            messagebox.showwarning("Atenção", "Selecione um produto na tabela para deletar.")
            return

        nome_item = self.nome_var.get()
        confirmar = messagebox.askyesno(
            "Confirmar Deleção",
            f"Tem certeza que deseja deletar o produto '{nome_item}' (ID: {self.produto_selecionado_id})?"
        )

        if confirmar:
            database.deletar_produto(self.produto_selecionado_id)
            messagebox.showinfo("Sucesso", f"Produto '{nome_item}' deletado com sucesso.")

            self.limpar_campos()
            self.atualizar_tabela()
        else:
            messagebox.showinfo("Cancelado", "Deleção cancelada.")

    def adicionar_produto_gui(self):
        """
        Lida com a lógica de adicionar um produto.
        """
        if self.produto_selecionado_id is not None:
            self.limpar_campos()

        try:
            nome = self.nome_var.get()
            quantidade = self.quantidade_var.get()
            preco = self.preco_var.get()

            if not nome or quantidade < 0 or preco < 0:
                messagebox.showerror("Erro de Validação", "Preencha o nome e use valores positivos.")
                return

            if database.adicionar_produto(nome, quantidade, preco):
                messagebox.showinfo("Sucesso", f"Produto '{nome}' adicionado com sucesso!")
                self.limpar_campos()
                self.atualizar_tabela()

        except tk.TclError:
            messagebox.showerror("Erro de Dados", "Quantidade e Preço devem ser números válidos.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}")

    def atualizar_tabela(self):
        """
        Busca os dados no BD e os insere na tabela (Treeview).
        """
        for item in self.tabela_estoque.get_children():
            self.tabela_estoque.delete(item)

        produtos = database.visualizar_produtos()

        for produto in produtos:
            produto_formatado = (produto[0], produto[1], produto[2], f"R$ {produto[3]:.2f}")
            self.tabela_estoque.insert('', 'end', values=produto_formatado)


if __name__ == '__main__':
    root = tk.Tk()
    app = EstoqueApp(root)
    root.mainloop()
