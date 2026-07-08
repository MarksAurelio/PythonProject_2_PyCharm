from flask import Flask, jsonify, request
from models import db, Tarefas, Alunos
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
#'sqlite:///tarefas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# 1) Criar rotas GET para alunos
@app.route('/alunos', methods=['GET'])
def listar_alunos():
    consulta = db.select(Alunos).order_by(Alunos.id)
    resultado = db.session.execute(consulta)
    alunos = resultado.scalars().all()
    lista_alunos = []

    for aluno in alunos:
        lista_alunos.append(aluno.to_dict())

    return jsonify(lista_alunos), 200

# 2) Criar rotas GET para alunos específico (por ID)
@app.route('/alunos/int:id_aluno', methods=['GET'])
def localizar_aluno_id(id_aluno):
    aluno = db.session.get(Alunos, id_aluno)

    if aluno is None:
        return jsonify({"erro":"Aluno não encontrado"}), 404
    return jsonify(aluno.to_dict()), 200

# 3) Criar rota POST para alunos
@app.route('/alunos', methods=['POST'])
def criar_aluno():
    dados = request.get_json()

    if not dados:
        return jsonify({'erro': 'Dados imcompletos'}), 400

    novo_aluno = Alunos(
        nome=dados['nome'],
        email=dados['email'],
        telefone=dados['telefone']
    )
    db.session.add(novo_aluno)
    db.session.commit()

    return jsonify(novo_aluno.to_dict()), 201

# 4) Criar rota PUT para alunos
@app.route('/alunos/<int:id_aluno>', methods=['PUT'])
def atualizar_aluno(id_aluno):
    aluno = db.session.get(Alunos, id_aluno)
    if aluno is None:
        return jsonify({"erro":"Aluno não encontrado"}), 404

    dados = request.get_json()
    aluno.nome = dados['nome']
    aluno.email = dados['email']
    aluno.telefone = dados['telefone']

    db.session.commit()

    return jsonify(aluno.to_dict()), 200

# 5) Criar rota PATH para alunos
@app.route('/alunos/<int:id_aluno>', methods=['PATCH'])
def atualizar_parcial_aluno(id_aluno):
    aluno = db.session.get(Alunos, id_aluno)

    if aluno is None:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    dados = request.get_json()

    if 'nome' in dados:
        aluno.nome = dados['nome']

    if 'email' in dados:
        aluno.email = dados['email']

    if 'telefone' in dados:
        aluno.telefone = dados['telefone']

    db.session.commit()

    return jsonify(aluno.to_dict()), 200

# 6) Criar rota DELETE para alunos
@app.route('/alunos/<int:id_aluno>', methods=['DELETE'])
def deletar_aluno(id_aluno):
    aluno = db.session.get(Alunos, id_aluno)

    if aluno is None:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    db.session.delete(aluno)

    db.session.commit()

    return jsonify({"mensagem":"Aluno deletado com sucesso"}), 200

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

@app.route('/tarefas/int:id_tarefa', methods=['GET'])
def atualizar_tarefas_id():
    id = request.args.get('id')


@app.route('/tarefas/<int:id_tarefa>', methods=['PUT'])
def atualizar_tarefas(id_tarefa):
    dados = request.get_json()

    if not dados:
        return jsonify({'erro': 'Nenhum dados foi enviado'}), 400

    campos_obrigatorios = ["titulo", "descricao", "concluida"]
    for campo in campos_obrigatorios:
        if campo not in dados:
            return jsonify({'erro':f'Campo{campo} é obrigatorio'}), 400

    tarefa = db.session.get(Tarefas, id_tarefa)

    if tarefa is None:
        return jsonify({'erro': 'Tarefa não encontrada'}), 404

    tarefa.titulo = dados['titulo']
    tarefa.descricao = dados['descricao']
    tarefa.concluida = dados['concluida']

    db.session.commit()

    return jsonify(tarefa.to_dict()), 201

@app.route('/tarefas/<int:id_tarefa>', methods=['PATCH'])
def alterar_tarefas(id_tarefa):
    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'Nenhum dados foi enviado'}), 400

    tarefa = db.session.get(Tarefas, id_tarefa)

    if tarefa is None:
        return jsonify({'erro':'Tarefa não encontrada'}), 404

    if 'titulo' in dados:
        tarefa.titulo = dados['titulo']
    if 'descricao' in dados:
        tarefa.descricao = dados['descricao']
    if 'concluida' in dados:
        tarefa.concluida = dados['concluida']

    db.session.commit()
    return jsonify(tarefa.to_dict()), 200

if __name__ == '__main__':
    app.run(debug=True)