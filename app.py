from flask import Flask , request , jsonify
from flask_cors import CORS
import _sqlite3

app = Flask(__name__)
CORS(app)

with _sqlite3.connect('database.db') as conn:
    cursor = conn.cursor()

    create_table_query = '''
        CREATE TABLE IF NOT EXISTS pacientes (
            cpf TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            nascimento TEXT NOT NULL,
            cep TEXT NOT NULL
        )     
    '''

    cursor.execute(create_table_query)
    conn.commit()

    print("tabela pacientes criada com sucesso")

@app.route('/')
def home():
    return 'API is working'

@app.route('/pacientes', methods=['GET'])
def listar_pacientes():
    try:
        with _sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT cpf, nome, nascimento, cep FROM pacientes')
            rows = cursor.fetchall()

            pacientes = []
            for row in rows:
                paciente = {
                    'cpf': row[0],
                    'nome': row[1],
                    'nascimento': row[2],
                    'cep': row[3]
                }
                pacientes.append(paciente)

            return jsonify(pacientes)
        
    except Exception as err:
        return jsonify({"err": str(err)}), 500  
    
@app.route('/paciente', methods=['POST'])
def cadastrar_paciente():
    try:
        dados = request.json
        cpf = dados.get('cpf')
        nome = dados.get('nome')
        nascimento = dados.get('nascimento')
        cep = dados.get('cep')

        if not cpf or not nome or not nascimento or not cep:
            return jsonify({'erro': 'Todos os campos são obrigatórios'}), 400
        
        with _sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pacientes WHERE cpf = ?", (cpf,))
            
            if cursor.fetchone():
                return jsonify({'mensagem': 'paciente já cadastrado.'}), 400

            cursor.execute("""
                INSERT INTO pacientes (cpf, nome, nascimento, cep) VALUES (?, ?, ?, ?)
                           """, (cpf, nome, nascimento, cep))

            conn.commit()

        return jsonify({'message': f'paciente {nome} cadastrado com sucesso'}), 201

    except Exception as err:
        return jsonify({"err": str(err)}), 500  

if __name__ == '__main__':
    app.run(debug=True)