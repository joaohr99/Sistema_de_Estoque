import sqlite3

DB_NAME = 'estoque.db'

def conectar_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    return conn, cursor

def criar_tabela():
    conn, cursor = conectar_db()
    try:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco REAL NOT NULL
            )        
        ''')

        conn.commit()
        print("Tabela 'produtos' criada ou já existente.")
    finally:
        conn.close()

if __name__ == '__main__':
    criar_tabela()

def adicionar_produto(nome, quantidade, preco):
    conn, cursor = conectar_db()
    try:
        cursor.execute('''
            INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)
        ''', (nome, quantidade, preco))

        conn.commit()
        print(f"Produto '{nome}' adicionado com sucesso!")
    except sqlite3.Error as e:
        print(f'Erro ao adicionar o produto: {e}')
    finally:
        conn.close()

if __name__ == '__main__':
    criar_tabela()
    adicionar_produto('Notebook Dell', 10, 3500.00)
    adicionar_produto('Mouse sem fio', 50, 85.50)

def visualizar_produtos():

    conn, cursor = conectar_db()
    try:
        cursor.execute('SELECT * FROM produtos')
        produtos = cursor.fetchall()

        if not produtos:
            print('O estoque está vazio.')
            return

        print('\n --- Produtos em Estoque ---')
        for produto in produtos:
            print(f'ID: {produto[0]}, Nome: {produto[1]}, Quantidade: {produto[2]}, Preço: R$ {produto[3]:.2f}')
        print("-------------------------\n")

    except sqlite3.Error as e:
        print(f"Erro ao visualizar os produtos: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    criar_tabela()

    adicionar_produto('Notebook Dell', 10, 3500.00)
    adicionar_produto('Mouse Sem Fio', 50, 85.50)

    visualizar_produtos()

def atualizar_produto(produto_id, nova_quantidade, novo_preco):

    conn, cursor = conectar_db()
    try:
        cursor.execute("""
        UPDATE produtos SET quantidade = ?, preco = ? WHERE id = ?
        """, (nova_quantidade, novo_preco, produto_id))

        if cursor.rowcount > 0:
            conn.commit()
            print(f'Produto de ID {produto_id} atualizado com sucesso!')
        else:
            print(f'Produto de ID {produto_id} não encontrado.')
    except sqlite3.Error as e:
        print(f"Erro ao atualizar o produto: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    criar_tabela()

    adicionar_produto('Notebook Dell', 10, 3500.00)
    adicionar_produto('Mouse Sem Fio', 50, 85.50)
    visualizar_produtos()

    atualizar_produto(1, 8, 3200.00)
    atualizar_produto(2, 60, 75.00)
    visualizar_produtos()