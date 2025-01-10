import unicodedata

from src.utils.methods_helper import validar_dado_numerico_como_string


def normalizar_string(text):
    try:
        return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()
    except Exception as error:
        raise Exception(f"Erro ao normalizar a string {text}! {error}")


def obtem_colunas(colunas: list):
    # lista de anos disponiveis no DF
    lista_anos = []
    lista_demais_colunas = []

    for coluna in colunas:
        # verifica se a variavel (coluna) eh ano ou nao
        if validar_dado_numerico_como_string(str(coluna)):
            lista_anos.append(coluna)
        else:
            lista_demais_colunas.append(coluna)

    return lista_anos, lista_demais_colunas
