from config import get_connection

class ROIService:
    def calcular_roi(self, produto_id, recomendado_id):
        conn = None  # Inicializa a variável como None
        try:
            conn = get_connection()  # Tenta criar a conexão
            cursor = conn.cursor()

            # Consulta que ignora a relação com produto_id na tabela ProdutoRecomendado
            cursor.execute("""
                SELECT p.custoMensal, pr.custoEstimado
                FROM Produto p, ProdutoRecomendado pr
                WHERE p.id = ? AND pr.id = ?
            """, (produto_id, recomendado_id))

            result = cursor.fetchone()

            if not result:
                raise ValueError("Produto ou Produto Recomendado não encontrados.")

            # Extrair os custos do resultado da consulta
            custoMensal, custoEstimado = result

            # Calcular economia mensal e tempo de retorno do investimento (ROI)
            economiaMensal = custoMensal - custoEstimado
            if economiaMensal <= 0:
                raise ValueError("A economia mensal deve ser maior que 0 para calcular o ROI.")

            investimentoTotal = 1000  # Valor fixo de investimento total (pode ser ajustado)
            tempoRetorno = investimentoTotal / economiaMensal

            return {
                "economiaMensal": round(economiaMensal, 2),
                "investimentoTotal": investimentoTotal,
                "tempoRetorno": round(tempoRetorno, 2)
            }

        except Exception as e:
            print(f"Erro ao calcular ROI: {e}")  # Log do erro
            raise e  # Relevantar o erro para tratamento no app.py

        finally:
            if conn:  # Fecha a conexão apenas se ela foi criada
                conn.close()
