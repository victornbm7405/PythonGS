import sqlite3

def get_connection():
    try:
        conn = sqlite3.connect(r"C:\Users\Modesto\OneDrive\Área de Trabalho\renovatec\src\main\resources\database\sqlite-tools-win-x64-3470000\meu_banco.db")
        print("Conexão com o banco criada com sucesso!")
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        raise e
