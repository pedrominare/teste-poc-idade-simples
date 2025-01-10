import pandas as pd

from src.data_frames.build_df import BuildDF
from src.utils.extract_data import obtem_colunas
from src.utils.load_file import get_sheet_names


def executa_cruzamento(path_xlsx: str):
    # primeira linha do arquivo xlsx com dados relevantes, como cabecalhos e observacoes.
    valid_data_row = 6
    chunk_size = 1000

    # obtem nomes das planilhas do xlsx
    sheet_names_xlsx = get_sheet_names(path_xlsx)

    """
    Obtem dados da planilha
    Caso haja mais de 1 planilha por pasta de trabalho,
    navega em todas
    """

    # coluna que representa a soma dos anos
    soma_anos = 'TOTAL_ANOS'

    for sheet in sheet_names_xlsx:
        obj_df = BuildDF(
            xlsx_name=path_xlsx,
            sheet_name=sheet,
            skiprows=valid_data_row,
            chunk_size=chunk_size
        )
        # carrega as variaveis do DF criado
        obj_df.get_variables()

        # obtem os nomes das variaveis (colunas) do DF
        colunas_anos, lista_demais_colunas = obtem_colunas(obj_df.variables)

        # Soma todos os anos em uma nova coluna 'TOTAL'
        obj_df.df[soma_anos] = obj_df.df[colunas_anos].sum(axis=1)

        # --- 1. Cruzamento SEXO x LOCAL ---
        if (
            "SEXO" in lista_demais_colunas and
            "LOCAL" in lista_demais_colunas
        ):
            sexo_local = obj_df.df.groupby(["SEXO", "LOCAL"]).agg({soma_anos: "sum"}).reset_index()
        else:
            raise ValueError("As variaveis SEXO e LOCAL não existem no df criado!")

        # --- 2. Cruzamento LOCAL x IDADE ---
        if (
            "IDADE" in lista_demais_colunas and
            "LOCAL" in lista_demais_colunas
        ):
            local_idade = obj_df.df.groupby(["LOCAL", "IDADE"]).agg({soma_anos: "sum"}).reset_index()
        else:
            raise ValueError("As variaveis SEXO e LOCAL não existem no df criado!")

        # --- 3. Cruzamento SEXO x IDADE ---
        if (
            "SEXO" in lista_demais_colunas and
            "IDADE" in lista_demais_colunas
        ):
            sexo_idade = obj_df.df.groupby(["SEXO", "IDADE"]).agg({soma_anos: "sum"}).reset_index()
        else:
            raise ValueError("As variaveis SEXO e LOCAL não existem no df criado!")

        with pd.ExcelWriter("cross_analysis_results.xlsx") as writer:
            sexo_local.to_excel(writer, sheet_name="SEXO_x_LOCAL", index=False)
            local_idade.to_excel(writer, sheet_name="LOCAL_x_IDADE", index=False)
            sexo_idade.to_excel(writer, sheet_name="SEXO_x_IDADE", index=False)

