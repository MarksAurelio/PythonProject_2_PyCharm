from flask import Flask, jsonify, request
from models import db, Tarefas

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarefas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def home():
    return jsonify({'mensagem': 'API com Bando de Dados funcionando'}), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

@app.route('/tarefas', methods=['POST'])
def criar_tarefas():
    data = request.get_json()

    if not data:
        return jsonify({
            "erro": "Nenhum dado foi enviado"
        }), 400

    campos_obrigatorios = ["titulo", "descricao"]

    for campo in campos_obrigatorios:
        if campo not in data:
            return jsonify({
                "erro": f"O campo {campo} é obrigatorio"
            })

    nova_tarefa = Tarefas(
        titulo=data['titulo'],
        descricao=data['descricao'],
        concluida=data.get('concluida', False))

    db.session.add(nova_tarefa)
    db.session.commit()

    return jsonify(nova_tarefa.to_dict()), 200

@app.route('/tarefas', methods=['GET'])
def listar_tarefas():
    # Criar a consulta:
    consulta = db.select(Tarefas).order_by(Tarefas.id)

    # Executar a cosulta e salvar na variável 'resultado':
    resultado = db.session.execute(consulta)

    # Salvar os resultados na variável tarefas
    tarefas = resultado.scalars().all()

    # outra forma:
    #tarefas = Tarefas.query.order_by(Tarefas.id).all()

    lita_tarefas = []

    for tarefa in tarefas:
        lita_tarefas.append(tarefa.to_dict())

    return jsonify(lita_tarefas), 200


if __name__ == '__main__':
    app.run(debug=True)