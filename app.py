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
            flash('Você precisa estar logado para acessar esta página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ========== ROTAS PÚBLICAS ==========

@app.route('/')
def splash():
    """Tela inicial (splash screen)"""
    if 'user_id' in session:
        return redirect(url_for('home'))
    return render_template('splash.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Tela e lógica de login"""
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        usuario = db.verificar_login(email, senha)
        
        if usuario:
            session['user_id'] = usuario['id']
            session['user_nome'] = usuario['nome']
            return redirect(url_for('home'))
        else:
            flash('Email ou senha inválidos.', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    """Tela e lógica de cadastro"""
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        cpf = request.form.get('cpf', '').replace('.', '').replace('-', '')
        senha = request.form.get('senha')
        confirma_senha = request.form.get('confirma_senha')
        
        if not all([nome, email, cpf, senha, confirma_senha]):
            flash('Por favor, preencha todos os campos.', 'warning')
            return redirect(url_for('cadastro'))
        
        if senha != confirma_senha:
            flash('As senhas não coincidem.', 'danger')
            return redirect(url_for('cadastro'))
            
        if len(cpf) != 11:
            flash('CPF inválido. Deve conter 11 dígitos.', 'danger')
            return redirect(url_for('cadastro'))

        if db.criar_usuario(nome, email, cpf, senha):
            flash('Cadastro realizado com sucesso! Faça o login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Este email ou CPF já está cadastrado.', 'danger')
            return redirect(url_for('cadastro'))
    
    return render_template('cadastro.html')

@app.route('/logout')
def logout():
    """Faz logout do usuário"""
    session.clear()
    return redirect(url_for('splash'))

# ========== ROTAS PROTEGIDAS ==========

@app.route('/home')
@login_required
def home():
    """Dashboard principal"""
    usuario = db.get_usuario(session['user_id'])
    return render_template('home.html', 
                           nome=usuario['nome'].split()[0],
                           pontos=usuario['pontos'])

@app.route('/perfil')
@login_required
def perfil():
    """Exibe o perfil do usuário"""
    usuario = db.get_usuario(session['user_id'])
    return render_template('perfil.html', usuario=usuario)

@app.route('/registrar-viagem', methods=['GET', 'POST'])
@login_required
def registrar_viagem():
    """Tela e lógica para registrar viagem"""
    if request.method == 'POST':
        modal = request.form.get('modal')
        # Lógica para registrar e dar pontos...
        pontos_ganhos = db.registrar_viagem(session['user_id'], modal)
        flash(f'Viagem registrada! Você ganhou {pontos_ganhos} pontos! 🎉', 'success')
        return redirect(url_for('home'))
    
    return render_template('registrar_viagem.html')

# --- NOVAS ROTAS PARA FEEDBACK E RECOMPENSAS ---

@app.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    """Tela para reportar lotação"""
    user_id = session['user_id']
    
    if request.method == 'POST':
        linha = request.form.get('linha')
        lotacao = request.form.get('lotacao')
        
        if not linha or not lotacao:
            flash('Por favor, selecione a linha e a lotação.', 'warning')
        else:
            db.registrar_feedback(user_id, linha, lotacao)
            # A mensagem de sucesso é mostrada pelo JavaScript no front-end.
            # O redirect aqui serve caso o JS falhe.
            flash('Feedback enviado com sucesso! Obrigado por contribuir.', 'success')
        return redirect(url_for('feedback'))

    # GET - Exibe a página com as estatísticas
    total_feedbacks = db.get_total_feedbacks(user_id)
    feedbacks_semana = db.get_feedbacks_semana(user_id)
    
    return render_template('feedback.html', 
                           total_feedbacks=total_feedbacks, 
                           feedbacks_semana=feedbacks_semana)

@app.route('/recompensas') # Alterado para /recompensas para melhor semântica
@login_required
def recompensas():
    """Tela para resgatar pontos"""
    user_id = session['user_id']
    usuario = db.get_usuario(user_id)
    historico_resgates = db.get_historico_resgates(user_id)
    
    return render_template('resgatar.html', 
                           pontos=usuario['pontos'], 
                           resgates=historico_resgates)

# ========== ROTAS DE API ==========

@app.route('/api/resgatar', methods=['POST'])
@login_required
def api_resgatar():
    """Processa o resgate de um benefício"""
    data = request.get_json()
    user_id = session['user_id']
    
    beneficio = data.get('beneficio')
    pontos_custo = data.get('pontos')
    
    # Chama a função do banco que faz a lógica de resgate
    resultado = db.resgatar_beneficio(user_id, beneficio, pontos_custo)
    
    return resultado # Retorna o JSON de sucesso ou erro para o front-end

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