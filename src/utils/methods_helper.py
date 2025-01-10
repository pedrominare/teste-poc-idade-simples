import re


def validar_dado_numerico_como_string(string_data: str):
    try:
        if re.match(r'^\d{4}$', string_data) is not None:
            return True
        else:
            return False
    except Exception as error:
        raise Exception(f"Erro no metodo validar_dado_numerico_como_string ao tentar validar o ano {string_data}! {error}")
