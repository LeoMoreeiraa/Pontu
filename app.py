from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import Database
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Gera chave secreta para sessões

# Inicializa o banco de dados
db = Database()

# ========== MIDDLEWARE DE AUTENTICAÇÃO ==========

def login_required(f):
    """Decorator para rotas que precisam de autenticação"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', error='required'))
        return f(*args, **kwargs)
    return decorated_function

# ========== ROTAS PÚBLICAS ==========

@app.route('/')
def splash():
    """Tela inicial (splash screen)"""
    # Se usuário já está logado, redireciona para home
    if 'user_id' in session:
        return redirect(url_for('home'))
    return render_template('splash.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Tela e lógica de login"""
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        # Valida credenciais
        usuario = db.verificar_login(email, senha)
        
        if usuario:
            # Armazena dados na sessão
            session['user_id'] = usuario['id']
            session['user_nome'] = usuario['nome']
            session['user_email'] = usuario['email']
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login', error='credentials'))
    
    # GET - exibe formulário
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    """Tela e lógica de cadastro"""
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        cpf = request.form.get('cpf').replace('.', '').replace('-', '')  # Remove formatação
        senha = request.form.get('senha')
        confirma_senha = request.form.get('confirma_senha')
        
        # Validações básicas
        if not all([nome, email, cpf, senha, confirma_senha]):
            return redirect(url_for('cadastro', error='missing'))
        
        if senha != confirma_senha:
            return redirect(url_for('cadastro', error='password_mismatch'))
        
        if len(cpf) != 11:
            return redirect(url_for('cadastro', error='cpf_invalid'))
        
        # Tenta criar usuário
        user_id = db.criar_usuario(nome, email, cpf, senha)
        
        if user_id:
            return redirect(url_for('cadastro', success='true'))
        else:
            return redirect(url_for('cadastro', error='exists'))
    
    # GET - exibe formulário
    return render_template('cadastro.html')

@app.route('/logout')
def logout():
    """Faz logout do usuário"""
    session.clear()
    return redirect(url_for('splash'))

# ========== ROTAS PROTEGIDAS (EXEMPLO - IMPLEMENTAR DEPOIS) ==========

@app.route('/home')
@login_required
def home():
    """Dashboard principal"""
    usuario = db.get_usuario(session['user_id'])
    return render_template('home.html', 
                         nome=usuario['nome'].split()[0],  # Apenas primeiro nome
                         pontos=usuario['pontos'])

@app.route('/perfil')
@login_required
def perfil():
    """Perfil do usuário (temporário)"""
    usuario = db.get_usuario(session['user_id'])
    return f"<h1>Perfil de {usuario['nome']}</h1><p>Email: {usuario['email']}</p>"

@app.route('/registrar-viagem', methods=['GET', 'POST'])
@login_required
def registrar_viagem():
    """Tela e lógica para registrar viagem"""
    if request.method == 'POST':
        modal = request.form.get('modal')
        origem = request.form.get('origem', '')
        destino = request.form.get('destino', '')
        
        # Registra a viagem e adiciona pontos
        pontos = db.registrar_viagem(session['user_id'], modal, origem, destino)
        
        return redirect(url_for('registrar_viagem', success='true', pontos=pontos))
    
    # GET - exibe formulário
    return render_template('registrar_viagem.html')

# ========== ROTAS DE API (para depois) ==========

@app.route('/api/registrar-viagem', methods=['POST'])
@login_required
def api_registrar_viagem():
    """Registra uma viagem e adiciona pontos"""
    data = request.get_json()
    modal = data.get('modal')
    origem = data.get('origem')
    destino = data.get('destino')
    
    pontos = db.registrar_viagem(session['user_id'], modal, origem, destino)
    
    return {
        'success': True,
        'pontos_ganhos': pontos,
        'mensagem': f'Viagem registrada! Você ganhou {pontos} pontos! 🎉'
    }

@app.route('/api/usuario')
@login_required
def api_usuario():
    """Retorna dados do usuário logado"""
    usuario = db.get_usuario(session['user_id'])
    return usuario

# ========== EXECUÇÃO ==========

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

'''from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/resgatar-pontos")
def resgatar_pontos():
    return jsonify({"message": "Você acessou a rota de Resgatar Pontos!"})

@app.route("/consultar-rotas")
def consultar_rotas():
    return jsonify({"message": "Consultando rotas..."})

@app.route("/planejar-rota")
def planejar_rota():
    return jsonify({"message": "Planejando rota..."})

@app.route("/salvar-trajeto")
def salvar_trajeto():
    return jsonify({"message": "Trajeto salvo com sucesso!"})

@app.route("/feedback")
def feedback():
    return jsonify({"message": "Envie seu feedback!"})

if __name__ == "__main__":
    app.run(debug=True)
'''