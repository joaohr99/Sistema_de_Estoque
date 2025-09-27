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


def visualizar_produtos():
    """Visualiza todos os produtos no estoque e retorna a lista."""
    conn, cursor = conectar_db()
    produtos = []
    try:
        cursor.execute('SELECT * FROM produtos')
        produtos = cursor.fetchall()

        # O retorno é a única ação de 'visualizar_produtos' agora
        return produtos

    except sqlite3.Error as e:
        print(f"Erro ao visualizar os produtos: {e}")
        return []
    finally:
        conn.close()

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

def deletar_produto(produto_id):

    conn, cursor = conectar_db()
    try:
        cursor.execute('DELETE FROM produtos WHERE id = ?', (produto_id,))

        if cursor.rowcount > 0:
            conn.commit()
            print(f'Produto de ID {produto_id} deletado com sucesso.')
        else:
            print(f'Produto de ID {produto_id} não encontrado para deleção.')

    except sqlite3.Error as e:
        print(f'Erro ao deletar produto: {e}')
    finally:
        conn.close()


def limpar_tabela():
    conn, cursor = conectar_db()
    try:
        cursor.execute('DELETE FROM produtos')
        conn.commit()
        print("Todos os dados da tabela 'produtos' foram limpos.")
    except sqlite3.Error as e:
        print(f'Erro ao limpar a tabela: {e}')
    finally:
        conn.close()
