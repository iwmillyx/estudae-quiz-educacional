import json
import sys
from pathlib import Path

# Importa a função conectar do mesmo arquivo que o app usa
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE.parent))  # Adiciona a pasta raiz ao path

from banco_dadosUsuarios import conectar

def popular_niveis():
    """
    Popula a tabela de níveis para todas as matérias
    """
    conn = conectar()
    cur = conn.cursor()
    
    # Buscar todas as matérias cadastradas
    cur.execute("SELECT id_materia, nome FROM materia")
    materias = cur.fetchall()
    
    if not materias:
        print("❌ Nenhuma matéria encontrada no banco!")
        conn.close()
        return False
    
    print(f"📚 Encontradas {len(materias)} matérias no banco")
    
    # Níveis de dificuldade
    niveis = ["Fácil", "Médio", "Difícil"]
    
    total_inseridos = 0
    
    for id_materia, nome_materia in materias:
        for nivel in niveis:
            # Verificar se já existe
            cur.execute("""
                SELECT id_nivel FROM nivel 
                WHERE id_materia = ? AND nome = ?
            """, (id_materia, nivel))
            
            if not cur.fetchone():
                # Inserir novo nível
                cur.execute("""
                    INSERT INTO nivel (nome, id_materia)
                    VALUES (?, ?)
                """, (nivel, id_materia))
                total_inseridos += 1
    
    conn.commit()
    conn.close()
    
    if total_inseridos > 0:
        print(f"✅ {total_inseridos} níveis inseridos\n")
    else:
        print(f"✅ Todos os níveis já estavam cadastrados\n")
    
    return True

def carregar_json(nome_arquivo):
    caminho = BASE / nome_arquivo
    if not caminho.exists():
        print(f"❌ Arquivo não encontrado: {nome_arquivo}")
        return []
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

def obter_id_nivel(materia, nivel):
    conn = conectar()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT n.id_nivel 
        FROM nivel n
        JOIN materia m ON m.id_materia = n.id_materia
        WHERE m.nome = ? AND n.nome = ?
    """, (materia, nivel))
    
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def inserir_pergunta(materia, nivel, q):
    id_nivel = obter_id_nivel(materia, nivel)

    if not id_nivel:
        print(f"⚠ Não encontrei nível para {materia} - {nivel}")
        return 0

    conn = conectar()
    cur = conn.cursor()

    # Verifica se a pergunta já existe (evita duplicação)
    cur.execute("""
        SELECT id_pergunta FROM pergunta 
        WHERE enunciado = ? AND id_nivel = ?
    """, (q["enunciado"], id_nivel))
    
    if cur.fetchone():
        conn.close()
        return 0  # Pergunta já existe, pula

    cur.execute("""
        INSERT INTO pergunta 
        (enunciado, alternativa_a, alternativa_b, alternativa_c, 
        alternativa_d, alternativa_correta, id_nivel)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        q["enunciado"],
        q["A"], q["B"], q["C"], q["D"],
        q["correta"],
        id_nivel
    ))

    conn.commit()
    conn.close()
    return 1


def importar_arquivo(nome, titulo):
    print(f"\n📁 Importando → {titulo}")

    perguntas = carregar_json(nome)
    if not perguntas:
        print("⚠ Nenhuma pergunta encontrada.")
        return 0

    total = 0

    for q in perguntas:
        materia = q["materia"]
        nivel = q["nivel"]
        total += inserir_pergunta(materia, nivel, q)

    print(f"   ✔ {total} perguntas inseridas de {titulo}")
    return total


def main():
    print("🚀 INICIANDO IMPORTAÇÃO...\n")
    
    # PASSO 1: Popular níveis primeiro
    print("=" * 50)
    print("PASSO 1: POPULANDO NÍVEIS DE DIFICULDADE")
    print("=" * 50)
    
    if not popular_niveis():
        print("\n❌ Erro ao popular níveis. Abortando...")
        return
    
    # PASSO 2: Importar perguntas
    print("=" * 50)
    print("PASSO 2: IMPORTANDO PERGUNTAS")
    print("=" * 50)

    total = 0

    # ENEM
    total += importar_arquivo("questoes_enem_natureza.json",   "ENEM - Natureza")
    total += importar_arquivo("questoes_enem_humanas.json",    "ENEM - Humanas")
    total += importar_arquivo("questoes_enem_linguagens.json", "ENEM - Linguagens")
    total += importar_arquivo("questoes_enem_matematica.json", "ENEM - Matemática")

    # MILITAR
    total += importar_arquivo("questoes_exercito.json" "quest",        "Exército")
    total += importar_arquivo("questoes_marinha.json",         "Marinha")
    total += importar_arquivo("questoes_aeronautica.json",     "Aeronáutica")

    print(f"\n{'=' * 50}")
    print(f"🎯 FINALIZADO! Total inserido: {total} perguntas.")
    print("=" * 50)


if __name__ == "__main__":
    main()
