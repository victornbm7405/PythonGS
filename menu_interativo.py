import requests

BASE_URL = "http://127.0.0.1:5000"

def menu():
    while True:
        print("\n=== MENU DE API ===")
        print("1. Inserir Produto")
        print("2. Consultar Todos os Produtos")
        print("3. Atualizar Produto")
        print("4. Excluir Produto")
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
        elif opcao == "0":
            break

def inserir_produto():
    try:
        nome = input("Nome: ")
        tipo = input("Tipo: ")
        consumo_energetico = float(input("Consumo Energético (kWh): "))
        custo_mensal = float(input("Custo Mensal (R$): "))
        produto = {"nome": nome, "tipo": tipo, "consumoEnergetico": consumo_energetico, "custoMensal": custo_mensal}
        response = requests.post(f"{BASE_URL}/produtos", json=produto)
        if response.status_code == 201:
            print("Produto inserido com sucesso!")
        else:
            print(response.json())
    except Exception as e:
        print(e)

def consultar_produtos():
    try:
        response = requests.get(f"{BASE_URL}/produtos")
        if response.status_code == 200:
            for produto in response.json():
                print(f"ID: {produto['id']}, Nome: {produto['nome']}, Tipo: {produto['tipo']}, Consumo: {produto['consumoEnergetico']} kWh, Custo: R$ {produto['custoMensal']}")
        else:
            print(response.json())
    except Exception as e:
        print(e)

def atualizar_produto():
    try:
        produto_id = input("ID do Produto: ")
        nome = input("Novo Nome: ")
        tipo = input("Novo Tipo: ")
        consumo_energetico = float(input("Novo Consumo Energético (kWh): "))
        custo_mensal = float(input("Novo Custo Mensal (R$): "))
        produto = {"nome": nome, "tipo": tipo, "consumoEnergetico": consumo_energetico, "custoMensal": custo_mensal}
        response = requests.put(f"{BASE_URL}/produtos/{produto_id}", json=produto)
        if response.status_code == 200:
            print("Produto atualizado com sucesso!")
        else:
            print(response.json())
    except Exception as e:
        print(e)

def excluir_produto():
    try:
        produto_id = input("ID do Produto: ")
        response = requests.delete(f"{BASE_URL}/produtos/{produto_id}")
        if response.status_code == 200:
            print("Produto excluído com sucesso!")
        else:
            print(response.json())
    except Exception as e:
        print(e)

if __name__ == "__main__":
    menu()
