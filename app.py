from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_connection():
    conn = sqlite3.connect(r"meu_banco.db")
    return conn

def inicializar_banco():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Produto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        tipo TEXT NOT NULL,
        consumoEnergetico REAL NOT NULL,
        custoMensal REAL NOT NULL
    )
    """)
    conn.commit()
    conn.close()

inicializar_banco()

@app.route("/")
def index():
    return jsonify({"message": "API funcionando corretamente!"}), 200

@app.route("/produtos", methods=["POST"])
def cadastrar_produto():
    try:
        data = request.json
        if not data.get("nome") or not data.get("tipo"):
            return jsonify({"error": "O nome e o tipo são obrigatórios."}), 400
        if not isinstance(data.get("consumoEnergetico"), (float, int)) or not isinstance(data.get("custoMensal"), (float, int)):
            return jsonify({"error": "Os valores de consumo e custo devem ser numéricos."}), 400
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO Produto (nome, tipo, consumoEnergetico, custoMensal)
        VALUES (?, ?, ?, ?)
        """, (data["nome"], data["tipo"], data["consumoEnergetico"], data["custoMensal"]))
        conn.commit()
        return jsonify({"message": "Produto cadastrado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'conn' in locals() and conn:
            conn.close()

@app.route("/produtos", methods=["GET"])
def consultar_produtos():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Produto")
        produtos = [{"id": row[0], "nome": row[1], "tipo": row[2], "consumoEnergetico": row[3], "custoMensal": row[4]} for row in cursor.fetchall()]
        return jsonify(produtos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'conn' in locals() and conn:
            conn.close()

@app.route("/produtos/<int:produto_id>", methods=["PUT"])
def atualizar_produto(produto_id):
    try:
        data = request.json
        if not data.get("nome") or not data.get("tipo"):
            return jsonify({"error": "O nome e o tipo são obrigatórios."}), 400
        if not isinstance(data.get("consumoEnergetico"), (float, int)) or not isinstance(data.get("custoMensal"), (float, int)):
            return jsonify({"error": "Os valores de consumo e custo devem ser numéricos."}), 400
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE Produto
        SET nome = ?, tipo = ?, consumoEnergetico = ?, custoMensal = ?
        WHERE id = ?
        """, (data["nome"], data["tipo"], data["consumoEnergetico"], data["custoMensal"], produto_id))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Produto não encontrado."}), 404
        return jsonify({"message": "Produto atualizado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'conn' in locals() and conn:
            conn.close()

@app.route("/produtos/<int:produto_id>", methods=["DELETE"])
def excluir_produto(produto_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Produto WHERE id = ?", (produto_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Produto não encontrado."}), 404
        return jsonify({"message": "Produto excluído com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    app.run(debug=True)
