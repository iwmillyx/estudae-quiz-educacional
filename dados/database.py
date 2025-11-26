import sqlite3
from pathlib import Path

# Caminho do banco de dados (mesmo para todos os arquivos)
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "estudae.db"

def conectar():
    """Cria conexão com o banco de dados"""
    return sqlite3.connect(DB_PATH)

def inicializar_banco():
    """
    Cria TODAS as tabelas do sistema.
    Execute apenas UMA VEZ ou quando quiser resetar o banco.
    """
    conn = conectar()
    cursor = conn.cursor()
    
    print("🔧 Inicializando banco de dados...")
    
    # Cria tabelas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz (
        id_quiz INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_completo TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha_hash TEXT NOT NULL,
        data_nasc TEXT,
        estado TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categoria (
        id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        id_quiz INTEGER NOT NULL,
        FOREIGN KEY (id_quiz) REFERENCES quiz(id_quiz)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS materia (
        id_materia INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        id_categoria INTEGER NOT NULL,
        FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nivel (
        id_nivel INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL CHECK (nome IN ('Fácil','Médio','Difícil')),
        id_materia INTEGER NOT NULL,
        FOREIGN KEY (id_materia) REFERENCES materia(id_materia)
    )
    """)

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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz_personalizado (
        id_quiz_personalizado INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario INTEGER NOT NULL,
        titulo TEXT NOT NULL,
        descricao TEXT,
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
    )
    """)

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
    
    conn.commit()
    conn.close()
    
    print("✅ Banco de dados 'estudae.db' inicializado com sucesso!")
    print("📊 Tabelas criadas: quiz, usuarios, categoria, materia, nivel, pergunta,")
    print("   quiz_personalizado, pergunta_personalizada, pontuacao")
    print(f"📁 Localização: {DB_PATH}")

def popular_dados_iniciais():
    """
    Popula o banco com dados básicos (quizzes, categorias, matérias)
    Execute DEPOIS de inicializar_banco()
    """
    conn = conectar()
    cursor = conn.cursor()
    
    print("📝 Populando dados iniciais...")
    
    # Insere quizzes
    cursor.execute("INSERT OR IGNORE INTO quiz (id_quiz, nome) VALUES (1, 'ENEM')")
    cursor.execute("INSERT OR IGNORE INTO quiz (id_quiz, nome) VALUES (2, 'MILITAR')")
    
    # Categorias ENEM
    categorias_enem = [
        (1, "Ciências da Natureza", 1),
        (2, "Ciências Humanas", 1),
        (3, "Linguagens e Códigos", 1),
        (4, "Matemática", 1)
    ]
    
    for id_cat, nome, id_quiz in categorias_enem:
        cursor.execute("""
            INSERT OR IGNORE INTO categoria (id_categoria, nome, id_quiz) 
            VALUES (?, ?, ?)
        """, (id_cat, nome, id_quiz))
    
    # Matérias ENEM por categoria
    materias_enem = [
        # Ciências da Natureza
        (1, "Física", 1),
        (2, "Química", 1),
        (3, "Biologia", 1),
        # Ciências Humanas
        (4, "História", 2),
        (5, "Geografia", 2),
        (6, "Filosofia", 2),
        (7, "Sociologia", 2),
        # Linguagens
        (8, "Português", 3),
        (9, "Literatura", 3),
        (10, "Inglês", 3),
        (11, "Espanhol", 3),
        (12, "Artes", 3),
        # Matemática
        (13, "Matemática", 4)
    ]
    
    for id_mat, nome, id_cat in materias_enem:
        cursor.execute("""
            INSERT OR IGNORE INTO materia (id_materia, nome, id_categoria) 
            VALUES (?, ?, ?)
        """, (id_mat, nome, id_cat))
    
    # Categorias MILITAR
    cursor.execute("""
        INSERT OR IGNORE INTO categoria (id_categoria, nome, id_quiz) 
        VALUES (5, 'Exatas', 2)
    """)
    
    cursor.execute("""
        INSERT OR IGNORE INTO categoria (id_categoria, nome, id_quiz) 
        VALUES (6, 'Humanas', 2)
    """)
    
    # Matérias MILITAR
    materias_militar = [
        (14, "Matemática", 5),
        (15, "Física", 5),
        (16, "Química", 5),
        (17, "Português", 6),
        (18, "Inglês", 6),
        (19, "História", 6),
        (20, "Geografia", 6),
    ]
    
    for id_mat, nome, id_cat in materias_militar:
        cursor.execute("""
            INSERT OR IGNORE INTO materia (id_materia, nome, id_categoria) 
            VALUES (?, ?, ?)
        """, (id_mat, nome, id_cat))
    
    conn.commit()
    conn.close()
    
    print("✅ Dados iniciais inseridos com sucesso!")

def resetar_banco():
    """
    CUIDADO: Deleta o banco e recria do zero!
    Use apenas para desenvolvimento/testes.
    """
    import os
    
    if DB_PATH.exists():
        os.remove(DB_PATH)
        print("🗑️ Banco de dados antigo removido")
    
    inicializar_banco()
    popular_dados_iniciais()

# Executa quando rodar: python database.py
if __name__ == "__main__":
    print("=" * 50)
    print("INICIALIZAÇÃO DO BANCO DE DADOS")
    print("=" * 50)
    
    resposta = input("\n⚠️  Deseja RESETAR o banco? (apaga tudo!) [s/N]: ")
    
    if resposta.lower() == 's':
        resetar_banco()
    else:
        inicializar_banco()
        popular_dados_iniciais()
    
    print("\n✅ Processo concluído!")