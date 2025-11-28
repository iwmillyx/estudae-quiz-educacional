import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "estudae.db"


def conectar():
    """Cria conexão com o banco de dados"""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


# ================================================================
#  CRIAÇÃO DO BANCO DE DADOS COMPLETO
# ================================================================
def inicializar_banco():
    conn = conectar()
    cursor = conn.cursor()

    print("🔧 Criando tabelas...")


    # ------------------- QUIZ ----------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz (
        id_quiz INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )
    """)

    # ------------------- USUÁRIOS ------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_completo TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha_hash TEXT NOT NULL,
        data_nasc TEXT,
        estado TEXT,
        xp INTEGER DEFAULT 0
    )
    """)

    # ------------------ CATEGORIA ------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categoria (
        id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        id_quiz INTEGER NOT NULL,
        FOREIGN KEY (id_quiz) REFERENCES quiz(id_quiz)
    )
    """)

    # ------------------ MATÉRIA --------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS materia (
        id_materia INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        id_categoria INTEGER NOT NULL,
        FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria)
    )
    """)

    # ------------------ NÍVEL ----------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nivel (
        id_nivel INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL CHECK (nome IN ('Fácil','Médio','Difícil')),
        id_materia INTEGER NOT NULL,
        FOREIGN KEY (id_materia) REFERENCES materia(id_materia)
    )
    """)

    # ------------------ PERGUNTA --------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pergunta (
        id_pergunta INTEGER PRIMARY KEY AUTOINCREMENT,
        enunciado TEXT NOT NULL,
        alternativa_a TEXT NOT NULL,
        alternativa_b TEXT NOT NULL,
        alternativa_c TEXT NOT NULL,
        alternativa_d TEXT NOT NULL,
        alternativa_correta TEXT NOT NULL CHECK(alternativa_correta IN ('A','B','C','D')),
        id_nivel INTEGER NOT NULL,
        FOREIGN KEY (id_nivel) REFERENCES nivel(id_nivel)
    )
    """)

    # ------------------ QUIZ PERSONALIZADO ----------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz_personalizado (
        id_quiz_personalizado INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario INTEGER NOT NULL,
        titulo TEXT NOT NULL,
        descricao TEXT,
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
    )
    """)

    # ------------------ PERGUNTA PERSONALIZADA ------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pergunta_personalizada (
        id_pergunta_personalizada INTEGER PRIMARY KEY AUTOINCREMENT,
        id_quiz_personalizado INTEGER NOT NULL,
        enunciado TEXT NOT NULL,
        alternativa_a TEXT NOT NULL,
        alternativa_b TEXT NOT NULL,
        alternativa_c TEXT NOT NULL,
        alternativa_d TEXT NOT NULL,
        alternativa_correta TEXT NOT NULL CHECK(alternativa_correta IN ('A','B','C','D')),
        nivel TEXT CHECK (nivel IN ('Fácil','Médio','Difícil')),
        FOREIGN KEY (id_quiz_personalizado) REFERENCES quiz_personalizado(id_quiz_personalizado)
    )
    """)

    # ------------------ PONTUAÇÃO --------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pontuacao (
        id_pontuacao INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario INTEGER NOT NULL,
        id_materia INTEGER NOT NULL,
        pontuacao INTEGER DEFAULT 0,
        data_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(id_usuario, id_materia),
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
        FOREIGN KEY (id_materia) REFERENCES materia(id_materia)
    )
    """)

    # ------------------ PROGRESSO --------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS progresso_usuario (
        id_progresso INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario INTEGER NOT NULL,
        id_materia INTEGER NOT NULL,
        id_nivel INTEGER NOT NULL,
        completado INTEGER DEFAULT 0,
        xp_ganho INTEGER DEFAULT 0,
        acertos INTEGER DEFAULT 0,
        erros INTEGER DEFAULT 0,
        data_conclusao TEXT,
        UNIQUE(id_usuario, id_materia, id_nivel),
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
        FOREIGN KEY (id_materia) REFERENCES materia(id_materia),
        FOREIGN KEY (id_nivel) REFERENCES nivel(id_nivel)
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Tabelas criadas com sucesso!\n")


# ================================================================
#  INSERIR DADOS INICIAIS (QUIZ, CATEGORIAS, MATÉRIAS)
# ================================================================
def popular_dados_iniciais():
    conn = conectar()
    cursor = conn.cursor()

    print("📝 Inserindo dados iniciais...")

    # === QUIZZES ===
    cursor.execute("INSERT OR IGNORE INTO quiz (id_quiz, nome) VALUES (1, 'ENEM')")
    cursor.execute("INSERT OR IGNORE INTO quiz (id_quiz, nome) VALUES (2, 'MILITAR')")

    # === CATEGORIAS ENEM ===
    categorias_enem = [
        (1, "Ciências da Natureza", 1),
        (2, "Ciências Humanas", 1),
        (3, "Linguagens e Códigos", 1),
        (4, "Matemática", 1),
    ]

    for c in categorias_enem:
        cursor.execute("INSERT OR IGNORE INTO categoria VALUES (?, ?, ?)", c)

    # === CATEGORIAS MILITARES DIVIDIDAS ===
    categorias_militares = [
        (5, "Exército", 2),
        (6, "Marinha", 2),
        (7, "Aeronáutica", 2),
    ]

    for c in categorias_militares:
        cursor.execute("INSERT OR IGNORE INTO categoria VALUES (?, ?, ?)", c)

    # === MATÉRIAS ENEM ===
    materias_enem = [
        (1, "Física", 1),
        (2, "Química", 1),
        (3, "Biologia", 1),

        (4, "História", 2),
        (5, "Geografia", 2),
        (6, "Filosofia", 2),
        (7, "Sociologia", 2),

        (8, "Português", 3),
        (9, "Literatura", 3),
        (10, "Inglês", 3),
        (11, "Espanhol", 3),
        (12, "Artes", 3),

        (13, "Matemática", 4),
    ]

    for m in materias_enem:
        cursor.execute("INSERT OR IGNORE INTO materia VALUES (?, ?, ?)", m)

    # === MATÉRIAS MILITAR ===
    # Exército
    materias_exercito = [
        ("Português (Exército)", 5),
        ("Matemática (Exército)", 5),
        ("História (Exército)", 5),
        ("Geografia (Exército)", 5),
        ("Inglês (Exército)", 5),
        ("Física (Exército)", 5),
        ("Química (Exército)", 5),
    ]

    # Marinha
    materias_marinha = [
        ("Português (Marinha)", 6),
        ("Matemática (Marinha)", 6),
        ("Física (Marinha)", 6),
        ("Química (Marinha)", 6),
        ("Inglês (Marinha)", 6),
    ]

    # Aeronáutica
    materias_aeronautica = [
        ("Português (Aeronáutica)", 7),
        ("Matemática (Aeronáutica)", 7),
        ("Inglês (Aeronáutica)", 7),
        ("Física (Aeronáutica)", 7),
    ]

    todas_militares = materias_exercito + materias_marinha + materias_aeronautica

    id_auto = 14
    for nome, id_categoria in todas_militares:
        cursor.execute("""
            INSERT OR IGNORE INTO materia (id_materia, nome, id_categoria)
            VALUES (?, ?, ?)
        """, (id_auto, nome, id_categoria))
        id_auto += 1

    conn.commit()
    conn.close()
    print("✅ Dados iniciais configurados!\n")


# ================================================================
#  RESETAR BANCO
# ================================================================
def resetar_banco():
    import os

    if DB_PATH.exists():
        print("🗑 Banco antigo removido!")
        os.remove(DB_PATH)

    inicializar_banco()
    popular_dados_iniciais()


# ================================================================
#  EXECUÇÃO DIRETA
# ================================================================
if __name__ == "__main__":
    print("==============================================")
    print("      INICIALIZAR / RESETAR BANCO")
    print("==============================================\n")

    resp = input("⚠️ Deseja RESETAR o banco? (S/N): ").lower()

    if resp == "s":
        resetar_banco()
    else:
        inicializar_banco()
        popular_dados_iniciais()

    print("\n✅ Finalizado!")
