import sys
from pathlib import Path
import random

BASE = Path(__file__).parent
sys.path.insert(0, str(BASE.parent))

from banco_dadosUsuarios import conectar, criar_usuario, atualizar_pontuacao, obter_id_materia_por_nome
import hashlib

def criar_senha_hash(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def popular_usuarios_teste():
    """
    Cria vários usuários de teste com pontuações aleatórias
    Usuários diferentes para ENEM e Militar
    """
    
    print("\n" + "="*60)
    print("👥 CRIANDO USUÁRIOS DE TESTE PARA O RANKING")
    print("="*60 + "\n")
    
    # Usuários focados no ENEM (mais XP no ENEM)
    usuarios_enem = [
        ("Ana Silva", "ana.silva@email.com", "2005-03-15", "SP"),
        ("Bruno Santos", "bruno.santos@email.com", "2004-07-22", "RJ"),
        ("Carla Oliveira", "carla.oliveira@email.com", "2005-11-08", "MG"),
        ("Daniel Costa", "daniel.costa@email.com", "2004-01-30", "RS"),
        ("Eduarda Lima", "eduarda.lima@email.com", "2005-09-12", "BA"),
        ("Felipe Souza", "felipe.souza@email.com", "2004-05-25", "PR"),
        ("Gabriela Alves", "gabriela.alves@email.com", "2005-02-18", "SC"),
        ("Helena Rocha", "helena.rocha@email.com", "2004-12-03", "PE"),
        ("Igor Martins", "igor.martins@email.com", "2005-06-27", "CE"),
        ("Julia Ferreira", "julia.ferreira@email.com", "2004-10-14", "GO"),
        ("Lucas Pereira", "lucas.pereira@email.com", "2005-04-20", "DF"),
        ("Mariana Gomes", "mariana.gomes@email.com", "2004-08-15", "ES"),
    ]
    
    # Usuários focados no MILITAR (mais XP no Militar)
    usuarios_militar = [
        ("Rafael Cardoso", "rafael.cardoso@email.com", "2004-02-10", "RJ"),
        ("Sofia Mendes", "sofia.mendes@email.com", "2005-06-18", "SP"),
        ("Thiago Ribeiro", "thiago.ribeiro@email.com", "2004-11-25", "RS"),
        ("Valentina Castro", "valentina.castro@email.com", "2005-01-08", "MG"),
        ("William Dias", "william.dias@email.com", "2004-09-30", "PR"),
        ("Yasmin Correia", "yasmin.correia@email.com", "2005-07-12", "BA"),
        ("Arthur Moreira", "arthur.moreira@email.com", "2004-03-22", "SC"),
        ("Beatriz Nunes", "beatriz.nunes@email.com", "2005-10-05", "PE"),
        ("Caio Barbosa", "caio.barbosa@email.com", "2004-04-17", "CE"),
        ("Davi Rodrigues", "davi.rodrigues@email.com", "2005-12-28", "GO"),
    ]
    
    # Usuários que estudam AMBOS (XP equilibrado)
    usuarios_ambos = [
        ("Enzo Fernandes", "enzo.fernandes@email.com", "2004-06-09", "DF"),
        ("Fernanda Teixeira", "fernanda.teixeira@email.com", "2005-05-14", "ES"),
        ("Giovanni Sousa", "giovanni.sousa@email.com", "2004-08-21", "RJ"),
        ("Isabela Cunha", "isabela.cunha@email.com", "2005-03-03", "SP"),
        ("João Azevedo", "joao.azevedo@email.com", "2004-07-19", "MG"),
    ]
    
    conn = conectar()
    cursor = conn.cursor()
    
    # Matérias
    materias_enem = [
        "Física", "Química", "Biologia",
        "História", "Geografia", "Filosofia", "Sociologia",
        "Português", "Literatura", "Inglês", "Matemática"
    ]
    
    materias_militar = [
        "Português (Exército)", "Matemática (Exército)", "Física (Exército)",
        "Português (Marinha)", "Matemática (Marinha)",
        "Português (Aeronáutica)", "Matemática (Aeronáutica)"
    ]
    
    usuarios_criados = 0
    
    # CRIAR USUÁRIOS FOCADOS NO ENEM
    print("📚 Criando usuários focados no ENEM...\n")
    for nome, email, data_nasc, estado in usuarios_enem:
        if criar_e_pontuar_usuario(cursor, nome, email, data_nasc, estado, 
                                   materias_enem, materias_militar, 
                                   tipo="ENEM"):
            usuarios_criados += 1
    
    # CRIAR USUÁRIOS FOCADOS NO MILITAR
    print("\n🎖️  Criando usuários focados no MILITAR...\n")
    for nome, email, data_nasc, estado in usuarios_militar:
        if criar_e_pontuar_usuario(cursor, nome, email, data_nasc, estado, 
                                   materias_enem, materias_militar, 
                                   tipo="MILITAR"):
            usuarios_criados += 1
    
    # CRIAR USUÁRIOS QUE ESTUDAM AMBOS
    print("\n⚖️  Criando usuários que estudam AMBOS...\n")
    for nome, email, data_nasc, estado in usuarios_ambos:
        if criar_e_pontuar_usuario(cursor, nome, email, data_nasc, estado, 
                                   materias_enem, materias_militar, 
                                   tipo="AMBOS"):
            usuarios_criados += 1
    
    conn.close()
    
    print("\n" + "="*60)
    print(f"✅ {usuarios_criados} USUÁRIOS CRIADOS COM SUCESSO!")
    print("="*60)
    print("\n📊 DISTRIBUIÇÃO:")
    print(f"   📚 ENEM: {len(usuarios_enem)} usuários")
    print(f"   🎖️  MILITAR: {len(usuarios_militar)} usuários")
    print(f"   ⚖️  AMBOS: {len(usuarios_ambos)} usuários")
    print("\n📝 CREDENCIAIS DE LOGIN:")
    print("   Email: qualquer um da lista acima")
    print("   Senha: senha123 (para todos)")
    print("\n🎮 Agora o ranking está populado e diversificado!")
    print("="*60 + "\n")

def criar_e_pontuar_usuario(cursor, nome, email, data_nasc, estado, 
                            materias_enem, materias_militar, tipo):
    """
    Cria um usuário e adiciona pontuações de acordo com seu foco
    tipo: "ENEM", "MILITAR" ou "AMBOS"
    """
    
    # Verifica se já existe
    cursor.execute("SELECT id_usuario FROM usuarios WHERE email = ?", (email,))
    if cursor.fetchone():
        print(f"⏭️  {nome} já existe, pulando...")
        return False
    
    # Cria usuário
    senha_hash = criar_senha_hash("senha123")
    
    try:
        criar_usuario(nome, email, senha_hash, data_nasc, estado)
        print(f"✅ {nome} criado!", end=" ")
        
        # Busca o ID do usuário criado
        cursor.execute("SELECT id_usuario FROM usuarios WHERE email = ?", (email,))
        id_usuario = cursor.fetchone()[0]
        
        total_xp = 0
        
        if tipo == "ENEM":
            # MUITO XP no ENEM, POUCO no Militar
            for materia in materias_enem:
                id_materia = obter_id_materia_por_nome(materia)
                if id_materia:
                    xp = random.randint(200, 500)  # ALTO
                    atualizar_pontuacao(id_usuario, id_materia, xp)
                    total_xp += xp
            
            for materia in materias_militar:
                id_materia = obter_id_materia_por_nome(materia)
                if id_materia:
                    xp = random.randint(10, 80)  # BAIXO
                    atualizar_pontuacao(id_usuario, id_materia, xp)
                    total_xp += xp
        
        elif tipo == "MILITAR":
            # POUCO XP no ENEM, MUITO no Militar
            for materia in materias_enem:
                id_materia = obter_id_materia_por_nome(materia)
                if id_materia:
                    xp = random.randint(10, 80)  # BAIXO
                    atualizar_pontuacao(id_usuario, id_materia, xp)
                    total_xp += xp
            
            for materia in materias_militar:
                id_materia = obter_id_materia_por_nome(materia)
                if id_materia:
                    xp = random.randint(200, 500)  # ALTO
                    atualizar_pontuacao(id_usuario, id_materia, xp)
                    total_xp += xp
        
        else:  # AMBOS
            # XP EQUILIBRADO em ambos
            for materia in materias_enem:
                id_materia = obter_id_materia_por_nome(materia)
                if id_materia:
                    xp = random.randint(100, 300)  # MÉDIO
                    atualizar_pontuacao(id_usuario, id_materia, xp)
                    total_xp += xp
            
            for materia in materias_militar:
                id_materia = obter_id_materia_por_nome(materia)
                if id_materia:
                    xp = random.randint(100, 300)  # MÉDIO
                    atualizar_pontuacao(id_usuario, id_materia, xp)
                    total_xp += xp
        
        print(f"💎 {total_xp} XP")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar {nome}: {e}")
        return False

if __name__ == "__main__":
    popular_usuarios_teste()