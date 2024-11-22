import requests
import json

BASE_URL = "http://127.0.0.1:5000"  # Atualize se necessário

def menu():
    while True:
        print("\n=== MENU INTERATIVO ===")
        print("1. Inserir Produto")
        print("2. Consultar Produtos")
        print("3. Atualizar Produto")
        print("4. Excluir Produto")
        print("5. Consultar Produtos com Filtro")
        print("6. Exportar Produtos para JSON")
        print("7. Exportar Produtos para Excel")
        print("0. Sair")

        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            inserir_produto()
        elif opcao == "2":
            consultar_produtos()
        elif opcao == "3":
            atualizar_produto()
        elif opcao == "4":
            excluir_produto()
        elif opcao == "5":
            consulta_com_filtro()
        elif opcao == "6":
            exportar_json()
        elif opcao == "7":
            exportar_excel()
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida! Tente novamente.")

def inserir_produto():
    print("\n=== Inserir Produto ===")
    nome = input("Nome: ")
    tipo = input("Tipo: ")
    consumo_energetico = float(input("Consumo Energético: "))
    custo_mensal = float(input("Custo Mensal: "))

    dados = {
        "nome": nome,
        "tipo": tipo,
        "consumoEnergetico": consumo_energetico,
        "custoMensal": custo_mensal
    }
    response = requests.post(f"{BASE_URL}/produto", json=dados)
    print(response.json())

def consultar_produtos():
    print("\n=== Consultar Produtos ===")
    response = requests.get(f"{BASE_URL}/produtos")
    produtos = response.json()
    for produto in produtos:
        print(produto)

def atualizar_produto():
    print("\n=== Atualizar Produto ===")
    produto_id = int(input("ID do Produto: "))
    nome = input("Novo Nome: ")
    tipo = input("Novo Tipo: ")
    consumo_energetico = float(input("Novo Consumo Energético: "))
    custo_mensal = float(input("Novo Custo Mensal: "))

    dados = {
        "nome": nome,
        "tipo": tipo,
        "consumoEnergetico": consumo_energetico,
        "custoMensal": custo_mensal
    }
    response = requests.put(f"{BASE_URL}/produto/{produto_id}", json=dados)
    print(response.json())

def excluir_produto():
    print("\n=== Excluir Produto ===")
    produto_id = int(input("ID do Produto: "))
    response = requests.delete(f"{BASE_URL}/produto/{produto_id}")
    print(response.json())

def consulta_com_filtro():
    print("\n=== Consultar com Filtro ===")
    filtro = input("Digite o filtro (ex.: nome do produto): ")
    response = requests.get(f"{BASE_URL}/consulta", params={"filtro": filtro})
    produtos = response.json()
    for produto in produtos:
        print(produto)

def exportar_json():
    print("\n=== Exportar para JSON ===")
    response = requests.get(f"{BASE_URL}/exportar")
    print(response.json())

def exportar_excel():
    print("\n=== Exportar para Excel ===")
    response = requests.get(f"{BASE_URL}/exportar_excel")
    print(response.json())

if __name__ == "__main__":
    menu()
