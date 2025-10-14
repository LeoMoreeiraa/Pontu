import sqlite3
import bcrypt
from datetime import datetime

class Database:
    def __init__(self, db_name='pontu.db'):
        self.db_name = db_name
        self.init_db()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def init_db(self):
        """Cria as tabelas se não existirem"""
        conn = self.get_connection()
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
                pontos_gastos INTEGER,
                codigo_resgate TEXT,
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
        conn.close()
    
    # ========== USUÁRIOS ==========
    
    def criar_usuario(self, nome, email, cpf, senha):
        """Cria um novo usuário com senha hash"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Hash da senha
            senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
            
            cursor.execute('''
                INSERT INTO usuarios (nome, email, cpf, senha)
                VALUES (?, ?, ?, ?)
            ''', (nome, email, cpf, senha_hash))
            
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            return None  # Email ou CPF já existe
    
    def verificar_login(self, email, senha):
        """Verifica credenciais e retorna dados do usuário"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
        usuario = cursor.fetchone()
        conn.close()
        
        if usuario and bcrypt.checkpw(senha.encode('utf-8'), usuario[4]):
            return {
                'id': usuario[0],
                'nome': usuario[1],
                'email': usuario[2],
                'cpf': usuario[3],
                'pontos': usuario[5]
            }
        return None
    
    def get_usuario(self, user_id):
        """Retorna dados de um usuário"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, nome, email, cpf, pontos FROM usuarios WHERE id = ?', (user_id,))
        usuario = cursor.fetchone()
        conn.close()
        
        if usuario:
            return {
                'id': usuario[0],
                'nome': usuario[1],
                'email': usuario[2],
                'cpf': usuario[3],
                'pontos': usuario[4]
            }
        return None
    
    def atualizar_pontos(self, user_id, pontos):
        """Adiciona ou remove pontos do usuário"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE usuarios 
            SET pontos = pontos + ?
            WHERE id = ?
        ''', (pontos, user_id))
        
        conn.commit()
        conn.close()
    
    # ========== VIAGENS ==========
    
    def registrar_viagem(self, usuario_id, modal, origem=None, destino=None):
        """Registra uma viagem e adiciona pontos"""
        # Calcula pontos baseado no modal
        pontos_modal = {
            'metro': 10,
            'trem': 10,
            'onibus': 12,
            'bike': 15,
            'patinete': 15
        }
        pontos = pontos_modal.get(modal.lower(), 10)
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO viagens (usuario_id, modal, origem, destino, pontos_ganhos)
            VALUES (?, ?, ?, ?, ?)
        ''', (usuario_id, modal, origem, destino, pontos))
        
        conn.commit()
        conn.close()
        
        # Atualiza saldo do usuário
        self.atualizar_pontos(usuario_id, pontos)
        
        return pontos
    
    def get_historico_viagens(self, usuario_id, limit=10):
        """Retorna histórico de viagens do usuário"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT modal, origem, destino, pontos_ganhos, data_viagem
            FROM viagens
            WHERE usuario_id = ?
            ORDER BY data_viagem DESC
            LIMIT ?
        ''', (usuario_id, limit))
        
        viagens = cursor.fetchall()
        conn.close()
        
        return [{
            'modal': v[0],
            'origem': v[1],
            'destino': v[2],
            'pontos': v[3],
            'data': v[4]
        } for v in viagens]
    
    # ========== RESGATES ==========
    
    def resgatar_beneficio(self, usuario_id, beneficio, pontos_gastos):
        """Realiza resgate de benefício"""
        import random
        import string
        
        # Verifica se usuário tem pontos suficientes
        usuario = self.get_usuario(usuario_id)
        if not usuario or usuario['pontos'] < pontos_gastos:
            return None
        
        # Gera código de resgate
        codigo = 'PONTU-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO resgates (usuario_id, beneficio, pontos_gastos, codigo_resgate)
            VALUES (?, ?, ?, ?)
        ''', (usuario_id, beneficio, pontos_gastos, codigo))
        
        conn.commit()
        conn.close()
        
        # Remove pontos do usuário
        self.atualizar_pontos(usuario_id, -pontos_gastos)
        
        return codigo
    
    def get_historico_resgates(self, usuario_id):
        """Retorna histórico de resgates"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT beneficio, pontos_gastos, codigo_resgate, data_resgate
            FROM resgates
            WHERE usuario_id = ?
            ORDER BY data_resgate DESC
        ''', (usuario_id,))
        
        resgates = cursor.fetchall()
        conn.close()
        
        return [{
            'beneficio': r[0],
            'pontos': r[1],
            'codigo': r[2],
            'data': r[3]
        } for r in resgates]
    
    # ========== FAVORITOS ==========
    
    def adicionar_favorito(self, usuario_id, nome_rota, origem, destino):
        """Adiciona rota aos favoritos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO favoritos (usuario_id, nome_rota, origem, destino)
            VALUES (?, ?, ?, ?)
        ''', (usuario_id, nome_rota, origem, destino))
        
        conn.commit()
        conn.close()
    
    def get_favoritos(self, usuario_id):
        """Retorna favoritos do usuário"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, nome_rota, origem, destino
            FROM favoritos
            WHERE usuario_id = ?
        ''', (usuario_id,))
        
        favoritos = cursor.fetchall()
        conn.close()
        
        return [{
            'id': f[0],
            'nome': f[1],
            'origem': f[2],
            'destino': f[3]
        } for f in favoritos]
    
    def remover_favorito(self, favorito_id):
        """Remove um favorito"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM favoritos WHERE id = ?', (favorito_id,))
        
        conn.commit()
        conn.close()
    
    # ========== FEEDBACK ==========
    
    def registrar_feedback_lotacao(self, usuario_id, linha, lotacao):
        """Registra feedback de lotação"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO feedbacks_lotacao (usuario_id, linha, lotacao)
            VALUES (?, ?, ?)
        ''', (usuario_id, linha, lotacao))
        
        conn.commit()
        conn.close()