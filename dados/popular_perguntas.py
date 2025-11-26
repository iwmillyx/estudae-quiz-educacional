import sqlite3
from pathlib import Path
from banco_dadosUsuarios import conectar, importar_perguntas

def criar_niveis_e_popular():
    """Cria níveis e importa perguntas"""
    conn = conectar()
    cursor = conn.cursor()
    
    # 1. Cria os níveis
    print("📝 Criando níveis...")
    cursor.execute("SELECT id_materia, nome FROM materia")
    materias = cursor.fetchall()
    
    for id_materia, nome_materia in materias:
        for nivel in ['Fácil', 'Médio', 'Difícil']:
            try:
                cursor.execute("INSERT INTO nivel (nome, id_materia) VALUES (?, ?)", (nivel, id_materia))
                print(f"✅ {nome_materia} - {nivel}")
            except:
                pass
    
    conn.commit()
    conn.close()
    
    # 2. Importa perguntas
    print("\n📥 Importando perguntas...")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id_nivel, nome FROM nivel")
    niveis = cursor.fetchall()
    conn.close()
    
    for id_nivel, nivel_nome in niveis:
        print(f"   Importando {nivel_nome}...")
        importar_perguntas(nivel_nome, id_nivel)
    
    print("\n✅ Concluído!")

if __name__ == "__main__":
    criar_niveis_e_popular()