import time

import pandas as pd
import openpyxl
import re

import unicodedata


def create_df_from_large_xlsx(
    file_name: str,
    sheet_name: str,
    start_row: int = 1,
    chunk_size: int = 1000,
    logging=None,
):
    # Para criar um único DataFrame com todos os chunks:
    try:
        inicio = time.time()
        workbook = openpyxl.load_workbook(file_name, data_only=True, read_only=True)
        worksheet = workbook.active if sheet_name == "" else workbook[sheet_name]
        fim = time.time()
        logging.info(f"Tempo de leitura do arquivo xlsx: {fim - inicio:.2f} segundos")
    except Exception as error:
        raise Exception(f"Erro ao tentar ler o arquivo {file_name}! {error}")

    all_data = []
    inicio = time.time()
    for chunk in read_excel_in_chunks(
        worksheet=worksheet,
        chunk_size=chunk_size,
        start_row=start_row,
    ):
        all_data.append(chunk)

    fim = time.time()
    logging.info(f"Tempo de criacao dos DFs: {fim - inicio:.2f} segundos")

    try:
        # une todos os dataframes da lista all_data
        df = pd.concat(all_data, ignore_index=True)
    except Exception as error:
        raise Exception(f"Erro ao tentar concatenar os DFs! {error}")

    return df


def read_excel_in_chunks(worksheet, chunk_size: int = 1000, start_row: int = 1):
    get_headers = None

    for i in range(start_row, worksheet.max_row, chunk_size):
        # Itera sobre as linhas da planilha, especificando o intervalo de linhas para cada chunk.
        rows = worksheet.iter_rows(
            min_row=i, max_row=min(i + chunk_size, worksheet.max_row)
        )

        # Cria uma lista de listas, onde cada lista interna representa uma linha do chunk.
        data = [[cell.value for cell in row] for row in rows]

        if not get_headers:
            get_headers = data[0]
            data.pop(0)  # exclui o cabecalho do dataframe somente na primeira iteracao

        df_chunk = pd.DataFrame(data, columns=get_headers)
        """
        Retorna um gerador, permitindo processar os chunks de forma eficiente.
        Geradores permitem processar grandes quantidades de dados sem carregá-los todos de uma vez na memória.
        A palavra-chave yield transforma a função em um gerador.
        Em cada iteração do loop, quando yield data é encontrado, o valor de data é retornado para o chamador da função.
        """
        yield df_chunk


def get_sheet_names(file_name):
    try:
        excel_file = pd.ExcelFile(file_name)
        sheet_names = excel_file.sheet_names
    except Exception as error:
        raise FileExistsError(
            f"Erro ao tentar carregar os nomes das planilhas do arquivo {file_name}! {error}"
        )

    return sheet_names


def validar_dado_numerico_como_string(string_data: str):
    try:
        if re.match(r"^\d{4}$", string_data) is not None:
            return True
        else:
            return False
    except Exception as error:
        raise Exception(
            f"Erro no metodo validar_dado_numerico_como_string ao tentar validar o ano {string_data}! {error}"
        )


def normalizar_string(text):
    try:
        return "".join(
            c
            for c in unicodedata.normalize("NFD", text)
            if unicodedata.category(c) != "Mn"
        ).lower()
    except Exception as error:
        raise Exception(f"Erro ao normalizar a string {text}! {error}")
