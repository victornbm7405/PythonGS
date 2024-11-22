import sqlite3

def testar_conexao():
    try:
        # Caminho do banco de dados - atualize se necessário
        caminho_banco = r"C:\Users\Modesto\OneDrive\Área de Trabalho\renovatec\src\main\resources\database\sqlite-tools-win-x64-3470000\meu_banco.db"
        conn = sqlite3.connect(caminho_banco)
        print("Conexão bem-sucedida com o banco de dados!")
        conn.close()
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")

if __name__ == "__main__":
    testar_conexao()
