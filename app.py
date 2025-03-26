from flask import Flask, request, jsonify, render_template
import sqlite3
from flask_cors import CORS

app = Flask(__name__) 
CORS(app)

def init_db():
    with sqlite3.connect('database.db') as conn: #conecta ao banco de nome dataBase.db 
        conn.execute("""CREATE TABLE IF NOT EXISTS livros (
                     id integer primary key autoincrement,
                     categoria text not null,
                     titulo text not null,
                     autor text not null,
                     imagem_url text not null
                     ) """) #executa um script sql
        print("Banco de dados Criado !")

init_db()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/doar', methods=['POST'])
def doar():
    dados = request.get_json()
    titulo = dados.get('titulo')
    categoria = dados.get('categoria')
    autor = dados.get('autor')
    imagem_url = dados.get('imagem_url')
    if not all([titulo, categoria, autor, imagem_url]):
        return jsonify({"erro":"todos os campos são obrigatórios"}),400
    
    with sqlite3.connect('database.db') as conn:
        conn.execute(f""" INSERT INTO livros (categoria, titulo, autor, imagem_url) values ( ?, ?, ?, ? ) """,  (categoria, titulo, autor, imagem_url))
        conn.commit()
        return jsonify({ "mensagem":"Livro cadastrado com sucesso" }),201


@app.route('/livros', methods=['GET'])
def getLivros():
     with sqlite3.connect('database.db') as conn:
        livros =  conn.execute(""" SELECT * FROM LIVROS """).fetchall()
        livros_formatados= []
        for livro in livros:
            dicionario_livros = {
                "id": livro[0],
                "titulo": livro[1],
                "categoria": livro[2],
                "autor": livro[3],
                "imagem_url": livro[4]
            }
        livros_formatados.append(dicionario_livros)
        return jsonify(livros_formatados), 200


@app.route('/livros/<int:livro_id>', methods=['DELETE'])
def deletar_livro(livro_id):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM livros WHERE id = ?", (livro_id,))
        conn.commit()

    if cursor.rowcount == 0:
        return jsonify({"erro": "Livro não encontrado"}), 404

    return jsonify({"menssagem": "Livro excluido com sucesso"}), 200


if __name__ == '__main__':
    app.run(debug=True)#debug=True faz com que a cada save, ele atualize sozinho