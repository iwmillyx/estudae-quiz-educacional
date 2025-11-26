import sqlite3
from pathlib import Path
import random
import requests
import urllib.parse

# Ajuste o caminho do banco
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "estudae.db"

def conectar():
    return sqlite3.connect(DB_PATH)

# --- Funções básicas ---

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

def importar_perguntas(nivel_nome, id_nivel):
    nivel_api = {"Fácil": "easy", "Médio": "medium", "Difícil": "hard"}[nivel_nome]
    url = f"https://opentdb.com/api.php?amount=20&type=multiple&difficulty={nivel_api}&encode=url3986"

    try:
        response = requests.get(url, timeout=10)
        dados = response.json()

        # Verifica se a API retornou sucesso
        if dados.get('response_code') != 0:
            print(f"⚠️ API não retornou perguntas (código: {dados.get('response_code')})")
            return 0
        
        resultados = dados['results']

        conn = conectar()
        cursor = conn.cursor()

        perguntas_inseridas = 0

        for item in resultados:
            try:
                enunciado = urllib.parse.unquote(item['question'])
                alternativas = [urllib.parse.unquote(a) for a in item['incorrect_answers']]
                correta_texto = urllib.parse.unquote(item["correct_answer"])

                alternativas.append(correta_texto)
                random.shuffle(alternativas)

                # Garante 4 alternativas
                while len(alternativas) < 4:
                    alternativas.append("Alternativa não disponível")
                alternativas = alternativas[:4]

                letra_correta = chr(65 + alternativas.index(correta_texto))

                cursor.execute("""
                    INSERT INTO pergunta (enunciado, alternativa_a, alternativa_b, alternativa_c, alternativa_d, alternativa_correta, id_nivel)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (enunciado, alternativas[0], alternativas[1], alternativas[2], alternativas[3], letra_correta, id_nivel))

                perguntas_inseridas += 1
            except Exception as e:
                print(f"⚠️ Erro ao inserir pergunta: {e}")
                continue

        conn.commit()
        conn.close()

        print(f"✅ {perguntas_inseridas} perguntas importadas!")
        return perguntas_inseridas
    
    except Exception as e:
        print(f"❌ Erro ao buscar da API: {e}")
        return 0
    
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