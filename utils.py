# utils.py
"""
Funções utilitárias para design responsivo no EstudAe
"""

def get_dimensoes(root):
    """Retorna largura e altura da janela"""
    # Usa winfo_width/height, mas com fallback caso não esteja renderizado
    largura = root.winfo_width() if root.winfo_width() > 1 else 375
    altura = root.winfo_height() if root.winfo_height() > 1 else 812
    return largura, altura


def calcular_tamanho(root, largura_percent=None, altura_percent=None):
    """
    Calcula tamanho baseado em porcentagem da tela
    
    Args:
        root: janela principal
        largura_percent: porcentagem da largura (0.0 a 1.0)
        altura_percent: porcentagem da altura (0.0 a 1.0)
    
    Returns:
        tupla (largura, altura) em pixels
    
    Exemplo:
        largura, altura = calcular_tamanho(root, largura_percent=0.8, altura_percent=0.06)
        # Para tela 375x812: retorna (300, 48)
    """
    w, h = get_dimensoes(root)
    
    largura = int(w * largura_percent) if largura_percent else None
    altura = int(h * altura_percent) if altura_percent else None
    
    return largura, altura


def calcular_padding(root, percent=0.05):
    """
    Calcula padding baseado na altura da tela
    
    Args:
        root: janela principal
        percent: porcentagem da altura (padrão 5%)
    
    Returns:
        padding em pixels
    
    Exemplo:
        pady = calcular_padding(root, 0.05)  # 5% da altura
    """
    _, h = get_dimensoes(root)
    return int(h * percent)


def calcular_font_size(root, base_size=14):
    """
    Ajusta tamanho da fonte baseado na altura da tela
    
    Args:
        root: janela principal
        base_size: tamanho base da fonte (para tela 812px)
    
    Returns:
        tamanho da fonte em pixels
    
    Exemplo:
        font_size = calcular_font_size(root, base_size=16)
    """
    _, h = get_dimensoes(root)
    # Escala baseada em 812px (iPhone 13 como referência)
    escala = h / 812
    return int(base_size * escala)