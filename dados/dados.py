# ------------------------------------------------------------
# Este arquivo cuida dos DADOS do projeto.
# Aqui ficam:
#  - a estrutura base (categorias, matérias, lista de pontuações)
#  - funções para carregar/salvar o JSON
#  - funções para adicionar pontuação
#  - funções para calcular ranking geral e ranking por matéria
# ------------------------------------------------------------

import json  # biblioteca para ler/escrever JSON
# import os  # (não precisamos mais dele na opção 1)

ARQUIVO = "scores.json"  # Nome do arquivo .json com as pontuações

# Estrutura base com categorias, matérias e lista de pontuações
PADRAO = {
    "ENEM": {
        "materias": ["Matemática", "Linguagens", "Ciências Humanas", "Ciências da Natureza", "Redação"],
        "pontuacoes": []  # cada item: {"aluno": "...", "materia": "...", "pontos": 700}
    },
    "MILITAR": {
        "materias": ["Matemática", "Português", "Física", "Química", "História"],
        "pontuacoes": []
    }
}

def carregar_dados():
    """
    Sempre recria o arquivo com os dados definidos no código.
    1) Copia a estrutura base
    2) Preenche com exemplos
    3) Salva em scores.json
    4) Retorna o dicionário pronto
    """
    dados = PADRAO.copy()

    # Exemplos (pode editar/expandir à vontade)
    exemplos = [
        # ENEM
        ("ENEM", "Matemática", "Ana", 720),
        ("ENEM", "Linguagens", "Ana", 660),
        ("ENEM", "Ciências Humanas", "Ana", 710),

        ("ENEM", "Matemática", "Bruno", 680),
        ("ENEM", "Linguagens", "Bruno", 640),
        ("ENEM", "Ciências da Natureza", "Bruno", 690),

        ("ENEM", "Matemática", "Carla", 700),
        ("ENEM", "Linguagens", "Carla", 720),
        ("ENEM", "Redação", "Carla", 860),

        ("ENEM", "Matemática", "Diego", 650),
        ("ENEM", "Ciências Humanas", "Diego", 680),
        ("ENEM", "Ciências da Natureza", "Diego", 670),

        ("ENEM", "Matemática", "Eduarda", 760),
        ("ENEM", "Linguagens", "Eduarda", 700),
        ("ENEM", "Redação", "Eduarda", 850),

        ("ENEM", "Matemática", "Felipe", 720),
        ("ENEM", "Ciências Humanas", "Felipe", 705),

        ("ENEM", "Linguagens", "Giovana", 690),
        ("ENEM", "Redação", "Giovana", 840),

        ("ENEM", "Matemática", "Heitor", 730),
        ("ENEM", "Ciências da Natureza", "Heitor", 710),

        ("ENEM", "Matemática", "Isabela", 750),
        ("ENEM", "Linguagens", "Isabela", 620),
        ("ENEM", "Redação", "Isabela", 870),

        ("ENEM", "Matemática", "João", 700),
        ("ENEM", "Ciências Humanas", "João", 690),
        ("ENEM", "Redação", "João", 820),

        # MILITAR
        ("MILITAR", "Matemática", "Ana", 85),
        ("MILITAR", "Português", "Bruno", 78),
        ("MILITAR", "Física", "Carla", 92),
        ("MILITAR", "Química", "Diego", 88),
        ("MILITAR", "História", "Eduarda", 75),
        ("MILITAR", "Matemática", "Felipe", 89),
        ("MILITAR", "Português", "Giovana", 84),
        ("MILITAR", "Física", "Heitor", 95),
        ("MILITAR", "Química", "Isabela", 91),
        ("MILITAR", "História", "João", 88),
    ]

    # Preenche a lista de pontuações por categoria
    for cat, mat, aluno, pts in exemplos:
        dados[cat]["pontuacoes"].append({
            "aluno": aluno,
            "materia": mat,
            "pontos": int(pts)
        })

    # Salva no arquivo JSON (sempre sobrescreve)
    salvar_dados(dados)

    # Devolve os dados montados
    return dados

def salvar_dados(dados):
    """Grava o dicionário 'dados' no arquivo scores.json (com acentos e identado)."""
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

def adicionar_pontuacao(dados, aluno, categoria, materia, pontos):
    """Adiciona uma pontuação em memória; chame salvar_dados(dados) depois se quiser persistir."""
    if categoria not in dados:
        raise ValueError("Categoria inválida")
    if materia not in dados[categoria]["materias"]:
        raise ValueError("Matéria inválida para essa categoria")
    dados[categoria]["pontuacoes"].append({
        "aluno": aluno,
        "materia": materia,
        "pontos": int(pontos)
    })

def ranking_geral(dados, categoria):
    """Soma todas as matérias por aluno dentro da categoria e ordena do maior pro menor."""
    totais = {}
    for r in dados.get(categoria, {}).get("pontuacoes", []):
        aluno = r["aluno"]
        pts = int(r["pontos"])
        totais[aluno] = totais.get(aluno, 0) + pts
    lista = list(totais.items())
    lista.sort(key=lambda x: (-x[1], x[0]))
    return lista

def ranking_materia(dados, categoria, materia):
    """Soma apenas a matéria escolhida por aluno dentro da categoria e ordena."""
    totais = {}
    for r in dados.get(categoria, {}).get("pontuacoes", []):
        if r["materia"] == materia:
            aluno = r["aluno"]
            pts = int(r["pontos"])
            totais[aluno] = totais.get(aluno, 0) + pts
    lista = list(totais.items())
    lista.sort(key=lambda x: (-x[1], x[0]))
    return lista
