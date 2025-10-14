import sqlite3
import bcrypt
from datetime import datetime
import random
import string

class Database:
    def __init__(self, db_name='pontu.db'):
        self.db_name = db_name
        self.init_db()
    
    def get_connection(self):
        """Cria e retorna uma conexão com o banco de dados."""
        conn = sqlite3.connect(self.db_name)
        # Retorna linhas como dicionários (mais fácil de trabalhar no Flask)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Cria as tabelas se não existirem"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Tabela de usuários
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    cpf TEXT UNIQUE NOT NULL,
                    senha TEXT NOT NULL,
                    pontos INTEGER DEFAULT 0,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabela de viagens
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS viagens (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_id INTEGER NOT NULL,
                    modal TEXT NOT NULL,
                    origem TEXT,
                    destino TEXT,
                    pontos_ganhos INTEGER,
                    data_viagem TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
                )
            ''')
            
            # Tabela de resgates
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS resgates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_id INTEGER NOT NULL,
                    beneficio TEXT NOT NULL,
                    pontos_gastos INTEGER NOT NULL,
                    codigo_resgate TEXT NOT NULL,
                    data_resgate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
                )
            ''')
            
            # Tabela de favoritos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS favoritos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_id INTEGER NOT NULL,
                    nome_rota TEXT NOT NULL,
                    origem TEXT,
                    destino TEXT,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
                )
            ''')
            
            # Tabela de feedbacks de lotação
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS feedbacks_lotacao (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_id INTEGER NOT NULL,
                    linha TEXT NOT NULL,
                    lotacao TEXT NOT NULL,
                    data_feedback TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
                )
            ''')
            
            conn.commit()
    
    # ========== USUÁRIOS ==========
    
    def criar_usuario(self, nome, email, cpf, senha):
        """Cria um novo usuário com senha hash"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
                cursor.execute(
                    'INSERT INTO usuarios (nome, email, cpf, senha) VALUES (?, ?, ?, ?)',
                    (nome, email, cpf, senha_hash)
                )
                conn.commit()
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None  # Email ou CPF já existe
    
    def verificar_login(self, email, senha):
        """Verifica credenciais e retorna dados do usuário como dicionário"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
            usuario = cursor.fetchone()
        
        if usuario and bcrypt.checkpw(senha.encode('utf-8'), usuario['senha']):
            # Retorna um dicionário com os dados do usuário
            return dict(usuario)
        return None
    
    def get_usuario(self, user_id):
        """Retorna dados de um usuário como dicionário"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM usuarios WHERE id = ?', (user_id,))
            usuario = cursor.fetchone()
        
        if usuario:
            return dict(usuario)
        return None
    
    def atualizar_pontos(self, user_id, pontos):
        """Adiciona ou remove pontos do usuário"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE usuarios SET pontos = pontos + ? WHERE id = ?', (pontos, user_id))
            conn.commit()
    
    # ========== VIAGENS ==========
    
    def registrar_viagem(self, usuario_id, modal, origem=None, destino=None):
        """Registra uma viagem e adiciona pontos"""
        pontos_modal = {'metro': 10, 'trem': 10, 'onibus': 12, 'bike': 15, 'patinete': 15}
        pontos = pontos_modal.get(modal.lower(), 10)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO viagens (usuario_id, modal, origem, destino, pontos_ganhos) VALUES (?, ?, ?, ?, ?)',
                (usuario_id, modal, origem, destino, pontos)
            )
            conn.commit()
        
        self.atualizar_pontos(usuario_id, pontos)
        return pontos
    
    # ========== RESGATES ==========
    
    def resgatar_beneficio(self, user_id, beneficio, pontos_custo):
        """Realiza resgate de benefício e retorna um JSON de status"""
        usuario = self.get_usuario(user_id)
        
        if not usuario or usuario['pontos'] < pontos_custo:
            return {'success': False, 'mensagem': 'Você não tem pontos suficientes para este resgate.'}
            
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Gera código de resgate
                codigo = 'PONTU-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                
                # Insere o resgate
                cursor.execute(
                    'INSERT INTO resgates (usuario_id, beneficio, pontos_gastos, codigo_resgate) VALUES (?, ?, ?, ?)',
                    (user_id, beneficio, pontos_custo, codigo)
                )
                
                # Debita os pontos (operação segura)
                cursor.execute('UPDATE usuarios SET pontos = pontos - ? WHERE id = ?', (pontos_custo, user_id))
                
                conn.commit()
                
                return {
                    'success': True,
                    'mensagem': f'Benefício "{beneficio}" resgatado!',
                    'codigo': codigo
                }
        except Exception as e:
            # Em caso de erro, retorna falha
            print(f"Erro no resgate: {e}")
            return {'success': False, 'mensagem': 'Ocorreu um erro ao processar seu resgate.'}

    def get_historico_resgates(self, usuario_id):
        """Retorna histórico de resgates com data formatada"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT beneficio, pontos_gastos, codigo_resgate, data_resgate FROM resgates WHERE usuario_id = ? ORDER BY data_resgate DESC',
                (usuario_id,)
            )
            resgates = cursor.fetchall()
        
        # Formata a data para DD/MM/YYYY para exibição
        resgates_formatados = []
        for r in resgates:
            resgate_dict = dict(r)
            data_obj = datetime.strptime(resgate_dict['data_resgate'], '%Y-%m-%d %H:%M:%S')
            resgate_dict['data'] = data_obj.strftime('%d/%m/%Y')
            resgate_dict['pontos'] = resgate_dict.pop('pontos_gastos') # Renomeia para o template
            resgate_dict['codigo'] = resgate_dict.pop('codigo_resgate')
            resgates_formatados.append(resgate_dict)
            
        return resgates_formatados

    # ========== FEEDBACK ==========
    
    def registrar_feedback(self, usuario_id, linha, lotacao):
        """Registra um novo feedback de lotação no banco de dados."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO feedbacks_lotacao (usuario_id, linha, lotacao) VALUES (?, ?, ?)',
                (usuario_id, linha, lotacao)
            )
            conn.commit()

    def get_total_feedbacks(self, user_id):
        """Conta o total de feedbacks enviados por um usuário."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(id) FROM feedbacks_lotacao WHERE usuario_id = ?', (user_id,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else 0

    def get_feedbacks_semana(self, user_id):
        """Conta os feedbacks enviados por um usuário nos últimos 7 dias."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # A sintaxe de data é específica para SQLite
            cursor.execute(
                "SELECT COUNT(id) FROM feedbacks_lotacao WHERE usuario_id = ? AND data_feedback >= date('now', '-7 days')",
                (user_id,)
            )
            resultado = cursor.fetchone()
            return resultado[0] if resultado else 0