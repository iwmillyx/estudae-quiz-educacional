import sqlite3
from pathlib import Path

# Ajuste o caminho do banco
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "estudae.db"

# Coloca o DB na raiz do projeto (dois níveis acima deste arquivo: <projeto>/estudae.db)
# Assim todos os scripts que importarem este módulo vão apontar para o mesmo DB.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

def conectar():
    # Garante que a pasta existe
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    # DEBUG: imprime caminho absoluto do DB (verifique ao rodar quiz e popular_perguntas)
    print(f"[DEBUG] conectar() -> usando DB em: {DB_PATH}")
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def inicializar_niveis():
    """
    Cria os níveis automaticamente se não existirem.
    Chame isso quando o app iniciar.
    """
    conn = conectar()
    cursor = conn.cursor()
    
    # Verifica se já existem níveis
    cursor.execute("SELECT COUNT(*) FROM nivel")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return  # Já existem níveis, não faz nada
    
    print("📝 Criando níveis automaticamente...")
    
    # Cria os níveis para cada matéria
    cursor.execute("SELECT id_materia, nome FROM materia")
    materias = cursor.fetchall()
    
    for id_materia, nome_materia in materias:
        for nivel_nome in ['Fácil', 'Médio', 'Difícil']:
            cursor.execute("""
                INSERT OR IGNORE INTO nivel (nome, id_materia) 
                VALUES (?, ?)
            """, (nivel_nome, id_materia))
            print(f"  ✅ {nome_materia} - {nivel_nome}")
    
    conn.commit()
    conn.close()
    print("✅ Níveis criados automaticamente!")

# --- Funções básicas (mantidas como estavam) ---

def criar_usuario(nome_completo, email, senha_hash, data_nasc, estado):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO usuarios (nome_completo, email, senha_hash, data_nasc, estado) 
        VALUES (?, ?, ?, ?, ?)
    """, (nome_completo, email, senha_hash, data_nasc, estado))
    conn.commit()
    conn.close()

def verificar_login(email):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id_usuario, nome_completo, senha_hash FROM usuarios WHERE email=?", (email,))
    usuario = cursor.fetchone()
    conn.close()
    return usuario

def email_existente(email):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM usuarios WHERE email=?", (email,))
    existe = cursor.fetchone() is not None
    conn.close()
    return existe

def verificar_usuario_para_senha(email):
    """
    Retorna o usuário se o email existir, caso contrário None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id_usuario, nome_completo FROM usuarios WHERE email=?",
        (email,)
    )
    usuario = cursor.fetchone()
    conn.close()
    return usuario

def atualizar_senha(id_usuario, nova_senha_hash):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE usuarios SET senha_hash=? WHERE id_usuario=?",
        (nova_senha_hash, id_usuario)
    )
    conn.commit()
    conn.close()

def obter_dados_usuario(id_usuario):
    """
    Retorna um dicionário com todos os dados do usuário prontos para a tela Home.
    """
    conn = conectar()
    cursor = conn.cursor()

    # Nome
    cursor.execute("SELECT nome_completo FROM usuarios WHERE id_usuario=?", (id_usuario,))
    nome = cursor.fetchone()
    nome = nome[0] if nome else "Aluno(a)"

    # XP total
    cursor.execute("SELECT SUM(pontuacao) FROM pontuacao WHERE id_usuario=?", (id_usuario,))
    xp_total = cursor.fetchone()[0] or 0

    # XP ENEM (id_quiz=1)
    cursor.execute("""
        SELECT SUM(p.pontuacao)
        FROM pontuacao p
        JOIN materia m ON p.id_materia = m.id_materia
        JOIN categoria c ON m.id_categoria = c.id_categoria
        WHERE p.id_usuario=? AND c.id_quiz=1
    """, (id_usuario,))
    xp_enem = cursor.fetchone()[0] or 0

    # XP Militar (id_quiz=2)
    cursor.execute("""
        SELECT SUM(p.pontuacao)
        FROM pontuacao p
        JOIN materia m ON p.id_materia = m.id_materia
        JOIN categoria c ON m.id_categoria = c.id_categoria
        WHERE p.id_usuario=? AND c.id_quiz=2
    """, (id_usuario,))
    xp_militar = cursor.fetchone()[0] or 0

    # Progresso
    progresso_enem = min(int(xp_enem / 500 * 100), 100) if xp_enem > 0 else 0
    progresso_militar = min(int(xp_militar / 500 * 100), 100) if xp_militar > 0 else 0
    progresso_geral = min(int(xp_total / 1000 * 100), 100) if xp_total > 0 else 0

    # Nível geral (1 nível a cada 100 XP)
    nivel_geral = xp_total // 100 + 1

    # Ranking geral
    cursor.execute("""
       SELECT id_usuario
       FROM pontuacao
       GROUP BY id_usuario
       ORDER BY SUM(pontuacao) DESC
    """)
    usuarios_ordenados = [row[0] for row in cursor.fetchall()]
    ranking_posicao = usuarios_ordenados.index(id_usuario) + 1 if id_usuario in usuarios_ordenados else 0
 
    # Ranking ENEM
    cursor.execute("""
        SELECT p.id_usuario
        FROM pontuacao p
        JOIN materia m ON p.id_materia = m.id_materia
        JOIN categoria c ON m.id_categoria = c.id_categoria
        WHERE c.id_quiz = 1
        GROUP BY p.id_usuario
        ORDER BY SUM(p.pontuacao) DESC
    """)
    usuarios_enem = [row[0] for row in cursor.fetchall()]
    ranking_enem = usuarios_enem.index(id_usuario) + 1 if id_usuario in usuarios_enem else 0

    # Ranking Militar
    cursor.execute("""
        SELECT p.id_usuario
        FROM pontuacao p
        JOIN materia m ON p.id_materia = m.id_materia
        JOIN categoria c ON m.id_categoria = c.id_categoria
        WHERE c.id_quiz = 2
        GROUP BY p.id_usuario
        ORDER BY SUM(p.pontuacao) DESC
    """)
    usuarios_militar = [row[0] for row in cursor.fetchall()]
    ranking_militar = usuarios_militar.index(id_usuario) + 1 if id_usuario in usuarios_militar else 0

    # Streak (dias consecutivos logados, exemplo 0)
    streak_dias = 0

    conn.close()
 
    return {
        'nome': nome,
        'xp_total': xp_total,
        'nivel_geral': nivel_geral,
        'ranking_posicao': ranking_posicao,
        'ranking_enem': ranking_enem,
        'ranking_militar': ranking_militar,
        'streak_dias': streak_dias,
        'progresso_geral': progresso_geral,
        'xp_enem': xp_enem,
        'progresso_enem': progresso_enem,
        'xp_militar': xp_militar,
        'progresso_militar': progresso_militar
    }

def ranking_materia(id_usuario, id_materia):
    """
    Retorna a posição do usuário no ranking da matéria específica
    e a lista completa do ranking.
    """
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id_usuario, pontuacao
        FROM pontuacao
        WHERE id_materia=?
        ORDER BY pontuacao DESC
    """, (id_materia,))
    
    ranking = cursor.fetchall()
    
    posicao = 0
    for i, (uid, _) in enumerate(ranking, start=1):
        if uid == id_usuario:
            posicao = i
            break
    
    conn.close()
    return posicao, ranking

def obter_xp_materias_quiz(id_usuario, id_quiz):
    """
    Retorna um dicionário com XP por matéria de um quiz específico.
    Ex: {'Física': 120, 'Química': 80, ...}
    """
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT m.nome, SUM(p.pontuacao)
        FROM pontuacao p
        JOIN materia m ON p.id_materia = m.id_materia
        JOIN categoria c ON m.id_categoria = c.id_categoria
        WHERE p.id_usuario=? AND c.id_quiz=?
        GROUP BY m.id_materia
    """, (id_usuario, id_quiz))
    
    resultado = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()
    return resultado


def obter_niveis_completados_materia(id_usuario, id_quiz):
    """
    Retorna um dicionário com as matérias e os níveis que o usuário completou.
    
    Exemplo de retorno:
    {
        "Matemática": [1, 2],
        "Português": [1],
        "Física": [1, 2, 3]
    }
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        # Busca todos os registros de quizzes completados pelo usuário
        query = """
            SELECT materia, nivel 
            FROM historico_quiz 
            WHERE id_usuario = ? AND id_quiz = ?
            ORDER BY materia, nivel
        """
        cursor.execute(query, (id_usuario, id_quiz))
        resultados = cursor.fetchall()
        
        # Organiza em um dicionário
        niveis_por_materia = {}
        for materia, nivel in resultados:
            if materia not in niveis_por_materia:
                niveis_por_materia[materia] = []
            
            # Converte nomes de nível para números
            nivel_numero = {"Fácil": 1, "Médio": 2, "Difícil": 3}.get(nivel, 1)
            
            if nivel_numero not in niveis_por_materia[materia]:
                niveis_por_materia[materia].append(nivel_numero)
        
        # Ordena os níveis de cada matéria
        for materia in niveis_por_materia:
            niveis_por_materia[materia].sort()
        
        conn.close()
        return niveis_por_materia
        
    except Exception as e:
        print(f"❌ Erro ao obter níveis completados: {e}")
        return {}

def criar_tabela_historico_quiz():
    """Cria a tabela de histórico de quizzes se não existir"""
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS historico_quiz (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_usuario INTEGER NOT NULL,
                id_quiz INTEGER NOT NULL,
                materia TEXT NOT NULL,
                nivel TEXT NOT NULL,
                acertos INTEGER DEFAULT 0,
                total_questoes INTEGER DEFAULT 0,
                xp_ganho INTEGER DEFAULT 0,
                data_conclusao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
            )
        """)
        
        conn.commit()
        conn.close()
        print("✅ Tabela historico_quiz criada/verificada com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao criar tabela historico_quiz: {e}")


def salvar_resultado_quiz(id_usuario, id_quiz, materia, nivel, acertos, total_questoes, xp_ganho):
    """Salva o resultado de um quiz no histórico"""
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO historico_quiz 
            (id_usuario, id_quiz, materia, nivel, acertos, total_questoes, xp_ganho)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (id_usuario, id_quiz, materia, nivel, acertos, total_questoes, xp_ganho))
        
        conn.commit()
        conn.close()
        print(f"✅ Resultado salvo: {materia} - {nivel} ({acertos}/{total_questoes}) +{xp_ganho} XP")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao salvar resultado do quiz: {e}")
        return False


def carregar_dados_ranking():
    """
    Retorna um dicionário com os rankings gerais:
    {'ENEM': [('Nome1', pontos1), ...], 'MILITAR': [('Nome2', pontos2), ...]}
    """
    conn = conectar()
    cursor = conn.cursor()
    categorias = {"ENEM": 1, "MILITAR": 2}
    resultado = {}

    for cat_nome, id_quiz in categorias.items():
        cursor.execute("""
            SELECT u.nome_completo, SUM(p.pontuacao) as total
            FROM pontuacao p
            JOIN usuarios u ON p.id_usuario = u.id_usuario
            JOIN materia m ON p.id_materia = m.id_materia
            JOIN categoria c ON m.id_categoria = c.id_categoria
            WHERE c.id_quiz = ?
            GROUP BY p.id_usuario
            ORDER BY total DESC
        """, (id_quiz,))
        resultado[cat_nome] = cursor.fetchall()

    conn.close()
    return resultado

def ranking_geral(dados, categoria):
    """Retorna a lista de ranking da categoria escolhida"""
    return dados.get(categoria, [])

def carregar_ranking_materias():
    """
    Retorna um dicionário com rankings por categoria e matéria:
    {
        'ENEM': {
            'Física': [('Aluno1', 120), ('Aluno2', 100), ...],
            'Química': [...],
            ...
        },
        'MILITAR': {
            'Matéria1': [...],
            ...
        }
    }
    """
    conn = conectar()
    cursor = conn.cursor()

    categorias = {"ENEM": 1, "MILITAR": 2}
    resultado = {}

    for cat_nome, id_quiz in categorias.items():
        cursor.execute("""
            SELECT m.id_materia, m.nome 
            FROM materia m
            JOIN categoria c ON m.id_categoria = c.id_categoria
            WHERE c.id_quiz=?
        """, (id_quiz,))
        materias = cursor.fetchall()

        resultado[cat_nome] = {}

        for id_materia, nome in materias:
            cursor.execute("""
                SELECT u.nome_completo, p.pontuacao
                FROM pontuacao p
                JOIN usuarios u ON p.id_usuario = u.id_usuario
                WHERE p.id_materia=?
                ORDER BY p.pontuacao DESC
            """, (id_materia,))
            ranking = cursor.fetchall()
            resultado[cat_nome][nome] = ranking

    conn.close()
    return resultado

def atualizar_pontuacao(id_usuario, id_materia, pontos):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO pontuacao (id_usuario, id_materia, pontuacao)
        VALUES (?, ?, ?)
        ON CONFLICT(id_usuario, id_materia)
        DO UPDATE SET pontuacao = pontuacao + excluded.pontuacao
    """, (id_usuario, id_materia, pontos))

    conn.commit()
    conn.close()

def criar_quiz_personalizado(id_usuario, titulo, descricao):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO quiz_personalizado (id_usuario, titulo, descricao)
        VALUES (?, ?, ?)
    """, (id_usuario, titulo, descricao))

    conn.commit()
    conn.close()

def adicionar_pergunta_quiz(id_quiz, enunciado, a, b, c, d, correta, nivel):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO pergunta_personalizada
        (id_quiz_personalizado, enunciado, alternativa_a, alternativa_b,
         alternativa_c, alternativa_d, alternativa_correta, nivel)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (id_quiz, enunciado, a, b, c, d, correta, nivel))

    conn.commit()
    conn.close()

def obter_quizzes_usuario(id_usuario):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_quiz_personalizado, titulo, descricao
        FROM quiz_personalizado
        WHERE id_usuario=?
    """, (id_usuario,))

    dados = cursor.fetchall()
    conn.close()
    return dados

def obter_perguntas_quiz(id_quiz):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM pergunta_personalizada
        WHERE id_quiz_personalizado=?
    """, (id_quiz,))

    dados = cursor.fetchall()
    conn.close()
    return dados

def obter_perguntas_por_nivel(id_nivel, limite=10):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_pergunta, enunciado, alternativa_a, alternativa_b,
               alternativa_c, alternativa_d, alternativa_correta
        FROM pergunta
        WHERE id_nivel=?
        ORDER BY RANDOM() LIMIT ?
    """, (id_nivel, limite))

    dados = cursor.fetchall()
    conn.close()
    return dados


def obter_id_nivel_por_materia(nome_materia, nivel_numero):
    """
    Retorna o id_nivel real do banco baseado no nome da matéria e número do nível.
    nivel_numero: 1 (Fácil), 2 (Médio), 3 (Difícil)
    """
    conn = conectar()
    cursor = conn.cursor()
    
    nivel_nome_map = {1: "Fácil", 2: "Médio", 3: "Difícil"}
    nivel_nome = nivel_nome_map.get(nivel_numero, "Fácil")
    
    cursor.execute("""
        SELECT n.id_nivel
        FROM nivel n
        JOIN materia m ON n.id_materia = m.id_materia
        WHERE m.nome = ? AND n.nome = ?
    """, (nome_materia, nivel_nome))
    
    resultado = cursor.fetchone()
    conn.close()
    
    return resultado[0] if resultado else None

def obter_id_materia_por_nome(nome_materia):
    """
    Retorna o id_materia baseado no nome da matéria
    """
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id_materia FROM materia WHERE nome = ?
    """, (nome_materia,))
    
    resultado = cursor.fetchone()
    conn.close()
    
    return resultado[0] if resultado else None

def verificar_nivel_completado(id_usuario, nome_materia, nome_nivel):
    """
    Verifica se um nível já foi completado pelo usuário.
    Retorna True se completado, False caso contrário.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT completado 
            FROM progresso_usuario 
            WHERE id_usuario = ?
            AND id_materia = (SELECT id_materia FROM materia WHERE nome = ?)
            AND id_nivel = (SELECT id_nivel FROM nivel WHERE nome = ?)
        """, (id_usuario, nome_materia, nome_nivel))
        
        resultado = cursor.fetchone()
        conn.close()
        
        return resultado[0] == 1 if resultado else False
    except Exception as e:
        print(f"Erro ao verificar nível completado: {e}")
        return False


def salvar_progresso_nivel(id_usuario, nome_materia, nome_nivel, xp_ganho, acertos, erros):
    """
    Salva ou atualiza o progresso de um nível específico.
    Marca como completado e registra os dados.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        # Busca os IDs
        cursor.execute("SELECT id_materia FROM materia WHERE nome = ?", (nome_materia,))
        id_materia = cursor.fetchone()[0]
        
        cursor.execute("SELECT id_nivel FROM nivel WHERE nome = ?", (nome_nivel,))
        id_nivel = cursor.fetchone()[0]
        
        # Insere ou atualiza o progresso
        cursor.execute("""
            INSERT INTO progresso_usuario 
            (id_usuario, id_materia, id_nivel, completado, xp_ganho, acertos, erros, data_conclusao)
            VALUES (?, ?, ?, 1, ?, ?, ?, datetime('now'))
            ON CONFLICT(id_usuario, id_materia, id_nivel) 
            DO UPDATE SET 
                completado = 1,
                xp_ganho = xp_ganho + ?,
                acertos = acertos + ?,
                erros = erros + ?,
                data_conclusao = datetime('now')
        """, (id_usuario, id_materia, id_nivel, xp_ganho, acertos, erros, xp_ganho, acertos, erros))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Erro ao salvar progresso: {e}")
        return False


def adicionar_xp_usuario(id_usuario, xp):
    """
    Adiciona XP ao usuário na tabela usuarios.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        # Verifica se existe coluna xp na tabela usuarios
        cursor.execute("PRAGMA table_info(usuarios)")
        colunas = [col[1] for col in cursor.fetchall()]
        
        if 'xp' not in colunas:
            # Adiciona a coluna xp se não existir
            cursor.execute("ALTER TABLE usuarios ADD COLUMN xp INTEGER DEFAULT 0")
        
        # Atualiza o XP
        cursor.execute("""
            UPDATE usuarios 
            SET xp = COALESCE(xp, 0) + ? 
            WHERE id_usuario = ?
        """, (xp, id_usuario))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Erro ao adicionar XP: {e}")
        return False


def obter_progresso_materia(id_usuario, nome_materia):
    """
    Retorna o progresso geral de uma matéria (quantos níveis foram completados).
    Retorna: (completados, total)
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        # Total de níveis da matéria
        cursor.execute("""
            SELECT COUNT(*) 
            FROM nivel 
            WHERE id_materia = (SELECT id_materia FROM materia WHERE nome = ?)
        """, (nome_materia,))
        total = cursor.fetchone()[0]
        
        # Níveis completados
        cursor.execute("""
            SELECT COUNT(*) 
            FROM progresso_usuario 
            WHERE id_usuario = ?
            AND id_materia = (SELECT id_materia FROM materia WHERE nome = ?)
            AND completado = 1
        """, (id_usuario, nome_materia))
        completados = cursor.fetchone()[0]
        
        conn.close()
        return (completados, total)
    except Exception as e:
        print(f"Erro ao obter progresso: {e}")
        return (0, 3)  # Default: 0 de 3 níveis
    
def importar_perguntas(nome_materia, nivel_numero, limite=10):
    """
    Importa perguntas de uma matéria e nível específicos.
    
    Args:
        nome_materia (str): Nome da matéria (ex: "Física", "Matemática")
        nivel_numero (int): Número do nível (1=Fácil, 2=Médio, 3=Difícil)
        limite (int): Quantidade máxima de perguntas a retornar
    
    Returns:
        list: Lista de tuplas com os dados das perguntas
    """
    id_nivel = obter_id_nivel_por_materia(nome_materia, nivel_numero)
    
    if not id_nivel:
        print(f"⚠ Nível não encontrado para {nome_materia} - Nível {nivel_numero}")
        return []
    
    return obter_perguntas_por_nivel(id_nivel, limite)
