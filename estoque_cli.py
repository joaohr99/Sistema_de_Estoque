import database

def menu():

    database.criar_tabela()

    while True:
        print('\n--- Sistema de Gestão de Estoque ---')
        print('1. Adicionar Produto.')
        print('2. Visualizar Estoque.')
        print('3. Atualizar Produto (Quantidade/Preço)')
        print('4. Deletar Produto')
        print('5. Limpar TODO o Estoque (Atenção!)')
        print('6. Sair')
        print('------------------------------------------')

        escolha = input('Escolha uma opção [1-6]: ')

        if escolha == '1':
            print('\n--- Adicionar Produto ---')
            nome = input('Nome do Produto: ')

            try:
                quantidade = int(input("Quantidade: "))
                preco = float(input("Preço (ex: 150.50):"))

                database.adicionar_produto(nome, quantidade, preco)
            except ValueError:
                print("Erro: Quantidade deve ser um número inteiro e Preço deve ser um número decimal.")

        elif escolha == '2':
            database.visualizar_produtos()

        elif escolha == '3':
            print()