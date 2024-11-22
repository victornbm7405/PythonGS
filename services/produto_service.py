from config import get_connection

class ProdutoService:
    def cadastrar_produto(self, data):
        conn = None  # Inicializa a variável como None
        try:
            conn = get_connection()  # Tenta criar a conexão
            cursor = conn.cursor()
            # Query para inserir o produto
            cursor.execute("""
                INSERT INTO Produto (nome, tipo, consumoEnergetico, custoMensal)
                VALUES (?, ?, ?, ?)
            """, (data["nome"], data["tipo"], data["consumoEnergetico"], data["custoMensal"]))
            conn.commit()
        except Exception as e:
            print(f"Erro ao cadastrar produto: {e}")  # Log do erro
            raise e
        finally:
            if conn:  # Fecha a conexão apenas se ela foi criada
                conn.close()
