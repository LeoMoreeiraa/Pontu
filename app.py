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

@app.route('/resgatar', methods=['GET'])
@login_required
def resgatar():
    """Tela de resgate de pontos"""
    usuario = db.get_usuario(session['user_id'])
    resgates = db.get_historico_resgates(session['user_id'])
    
    # Formata as datas
    for resgate in resgates:
        resgate['data'] = resgate['data'][:16].replace('T', ' às ')
    
    return render_template('resgatar.html', 
                         pontos=usuario['pontos'],
                         resgates=resgates)

@app.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    """Tela e lógica de feedback de lotação"""
    if request.method == 'POST':
        linha = request.form.get('linha')
        lotacao = request.form.get('lotacao')
        
        # Registra o feedback
        db.registrar_feedback_lotacao(session['user_id'], linha, lotacao)
        
        return redirect(url_for('feedback', success='true'))
    
    # GET - exibe formulário
    # Conta total de feedbacks do usuário
    import sqlite3
    conn = db.get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM feedbacks_lotacao WHERE usuario_id = ?', 
                   (session['user_id'],))
    total_feedbacks = cursor.fetchone()[0]
    
    # Feedbacks dos últimos 7 dias
    cursor.execute('''
        SELECT COUNT(*) FROM feedbacks_lotacao 
        WHERE usuario_id = ? 
        AND date(data_feedback) >= date('now', '-7 days')
    ''', (session['user_id'],))
    feedbacks_semana = cursor.fetchone()[0]
    
    conn.close()
    
    return render_template('feedback.html',
                         total_feedbacks=total_feedbacks,
                         feedbacks_semana=feedbacks_semana)

@app.route('/rotas')
@login_required
def rotas():
    """Tela de consultar rotas com mapa"""
    return render_template('rotas.html')

@app.route('/favoritos')
@login_required
def favoritos():
    """Tela de rotas favoritas"""
    favoritos_list = db.get_favoritos(session['user_id'])
    return render_template('favoritos.html', favoritos=favoritos_list)

@app.route('/historico')
@login_required
def historico():
    """Tela de histórico de viagens"""
    import calendar
    from datetime import datetime
    
    viagens = db.get_historico_viagens(session['user_id'], limit=100)
    
    # Formata as viagens
    icones_modais = {
        'metro': '🚇',
        'trem': '🚆',
        'onibus': '🚌',
        'bike': '🚴',
        'patinete': '🛴'
    }
    
    nomes_modais = {
        'metro': 'Metrô',
        'trem': 'Trem (CPTM)',
        'onibus': 'Ônibus',
        'bike': 'Bicicleta',
        'patinete': 'Patinete'
    }
    
    viagens_formatadas = []
    for v in viagens:
        # Formata data
        data_obj = datetime.strptime(v['data'], '%Y-%m-%d %H:%M:%S')
        mes_nome = calendar.month_name[data_obj.month]
        
        viagens_formatadas.append({
            'modal': v['modal'],
            'icone': icones_modais.get(v['modal'], '🚇'),
            'modal_nome': nomes_modais.get(v['modal'], v['modal']),
            'origem': v['origem'],
            'destino': v['destino'],
            'pontos': v['pontos'],
            'data': v['data'],
            'data_formatada': data_obj.strftime('%d/%m/%Y às %H:%M'),
            'mes_ano': f'{mes_nome} {data_obj.year}'
        })
    
    # Calcula estatísticas
    total_viagens = len(viagens)
    total_pontos_ganhos = sum(v['pontos'] for v in viagens)
    co2_economizado = round(total_viagens * 2.5, 1)  # Mock: 2.5kg por viagem
    
    # Dias ativos (distintos)
    datas_distintas = set(v['data'][:10] for v in viagens)
    dias_ativos = len(datas_distintas)
    
    return render_template('historico.html',
                         viagens=viagens_formatadas,
                         total_viagens=total_viagens,
                         total_pontos_ganhos=total_pontos_ganhos,
                         co2_economizado=co2_economizado,
                         dias_ativos=dias_ativos)

@app.route('/explorar')
@login_required
def explorar():
    """Tela de explorar transportes"""
    return render_template('explorar.html')

@app.route('/planejar')
@login_required
def planejar():
    """Tela de planejar rota"""
    return render_template('planejar.html')

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

@app.route('/api/resgatar', methods=['POST'])
@login_required
def api_resgatar():
    """API para resgatar benefícios"""
    data = request.get_json()
    beneficio = data.get('beneficio')
    pontos = data.get('pontos')
    
    # Tenta resgatar
    codigo = db.resgatar_beneficio(session['user_id'], beneficio, pontos)
    
    if codigo:
        return {
            'success': True,
            'codigo': codigo,
            'mensagem': f'{beneficio} resgatado com sucesso!'
        }
    else:
        return {
            'success': False,
            'mensagem': 'Pontos insuficientes ou erro ao resgatar.'
        }, 400

@app.route('/api/usuario')
@login_required
def api_usuario():
    """Retorna dados do usuário logado"""
    usuario = db.get_usuario(session['user_id'])
    return usuario

@app.route('/api/favoritar', methods=['POST'])
@login_required
def api_favoritar():
    """API para adicionar rota aos favoritos"""
    data = request.get_json()
    nome_rota = data.get('nome_rota')
    origem = data.get('origem')
    destino = data.get('destino')
    
    try:
        db.adicionar_favorito(session['user_id'], nome_rota, origem, destino)
        return {
            'success': True,
            'mensagem': 'Rota adicionada aos favoritos!'
        }
    except Exception as e:
        return {
            'success': False,
            'mensagem': 'Erro ao adicionar favorito.'
        }, 400

@app.route('/api/remover-favorito/<int:favorito_id>', methods=['DELETE'])
@login_required
def api_remover_favorito(favorito_id):
    """API para remover favorito"""
    try:
        db.remover_favorito(favorito_id)
        return {
            'success': True,
            'mensagem': 'Favorito removido com sucesso!'
        }
    except Exception as e:
        return {
            'success': False,
            'mensagem': 'Erro ao remover favorito.'
        }, 400

# ========== EXECUÇÃO ==========

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)