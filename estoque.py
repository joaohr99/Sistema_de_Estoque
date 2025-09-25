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
