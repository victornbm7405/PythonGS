from flask import Flask, request, jsonify
from services.produto_service import ProdutoService
from services.roi_service import ROIService
from config import get_connection
import json
import pandas as pd

app = Flask(__name__)

# Instâncias dos serviços
produto_service = ProdutoService()
roi_service = ROIService()

# Endpoint inicial para verificar se a API está funcionando
@app.route("/")
def index():
    return jsonify({"message": "API funcionando corretamente!"}), 200

# Endpoint para cadastrar um produto
@app.route("/produto", methods=["POST"])
def cadastrar_produto():
    try:
        data = request.json
        # Validações
        if not data.get("nome") or not data.get("tipo"):
            return jsonify({"error": "O nome e o tipo são obrigatórios."}), 400
        if not isinstance(data.get("consumoEnergetico"), (float, int)) or not isinstance(data.get("custoMensal"), (float, int)):
            return jsonify({"error": "Os valores de consumo e custo devem ser numéricos."}), 400

        produto_service.cadastrar_produto(data)
        return jsonify({"message": "Produto cadastrado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint para calcular ROI entre produto principal e recomendado
@app.route("/roi", methods=["POST"])
def calcular_roi():
    try:
        data = request.json
        produto_id = data.get("produto_id")
        recomendado_id = data.get("recomendado_id")

        if not produto_id or not recomendado_id:
            return jsonify({"error": "Os campos 'produto_id' e 'recomendado_id' são obrigatórios!"}), 400

        resultado = roi_service.calcular_roi(produto_id, recomendado_id)
        return jsonify(resultado), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint para consultar produtos
@app.route("/produtos", methods=["GET"])
def consultar_produtos():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Produto")
        produtos = [
            {"id": row[0], "nome": row[1], "tipo": row[2], "consumoEnergetico": row[3], "custoMensal": row[4]}
            for row in cursor.fetchall()
        ]
        return jsonify(produtos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

# Endpoint para consultar produtos com filtro
@app.route("/consulta", methods=["GET"])
def consulta_com_filtro():
    try:
        filtro = request.args.get("filtro")
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM Produto"
        params = {}
        if filtro:
            query += " WHERE nome LIKE ?"
            params = (f"%{filtro}%",)
        cursor.execute(query, params)
        produtos = [
            {"id": row[0], "nome": row[1], "tipo": row[2], "consumoEnergetico": row[3], "custoMensal": row[4]}
            for row in cursor.fetchall()
        ]
        return jsonify(produtos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

# Endpoint para exportar produtos para JSON
@app.route("/exportar", methods=["GET"])
def exportar_dados():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Produto")
        produtos = [
            {"id": row[0], "nome": row[1], "tipo": row[2], "consumoEnergetico": row[3], "custoMensal": row[4]}
            for row in cursor.fetchall()
        ]

        with open("produtos_exportados.json", "w") as f:
            json.dump(produtos, f, indent=4)

        return jsonify({"message": "Dados exportados para produtos_exportados.json"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

# Endpoint para exportar produtos para Excel
@app.route("/exportar_excel", methods=["GET"])
def exportar_dados_excel():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Produto")
        colunas = [desc[0] for desc in cursor.description]
        dados = cursor.fetchall()

        df = pd.DataFrame(dados, columns=colunas)
        df.to_excel("produtos_exportados.xlsx", index=False)

        return jsonify({"message": "Dados exportados para produtos_exportados.xlsx"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

# Executar a aplicação
if __name__ == "__main__":
    app.run(debug=True)
