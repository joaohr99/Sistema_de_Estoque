from sys import excepthook

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
            print('\n--- Atualizar Produto ---')
            try:
                produto_id = int(input('ID do produto a atualizar: '))
                nova_quantidade = int(input('Nova quantidade: '))
                novo_preco = float(input('Novo preço (ex:150.50): '))

                database.atualizar_produto(produto_id, nova_quantidade, novo_preco)
            except ValueError:
                print('Erro: ID, Quantidade e Preço devem ser números.')

        elif escolha == '4':
            print('\n--- Deletar Produto ---')
            try:
                produto_id = int(input('ID do produto a deletar: '))
                database.deletar_produto(produto_id)
            except ValueError:
                print('Erro: O ID deve ser um número inteiro.')

        elif escolha == '5':
            confirmacao = input("TEM CERTEZA? Isso deletará TUDO. Digite 'SIM' para continuar!")
            if confirmacao == 'SIM':
                database.limpar_tabela()
            else:
                print('Operação cancelada.')

        elif escolha == '6':
            print('Saindo do sistema. Obrigado!')
            break

        else:
            print('Opção inválidade. Por favor, escolha um número entre 1 e 6')

if __name__ == '__main__':
    menu()