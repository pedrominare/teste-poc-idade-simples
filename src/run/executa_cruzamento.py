import pandas as pd

from src.data_frames.build_df import BuildDF
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

    for sheet in sheet_names_xlsx:
        obj_df = BuildDF(
            xlsx_name=path_xlsx,
            sheet_name=sheet,
            skiprows=valid_data_row,
            chunk_size=chunk_size
        )

        # gera o DF do arquivo
        obj_df.build_data_frame()

        # carrega as variaveis do DF criado
        obj_df.get_variables()

        # obtem os nomes das variaveis (colunas) do DF
        obj_df.define_columns()

        # Soma todos os anos em uma nova coluna 'TOTAL'
        obj_df.build_column_total_years()

        # Cruzamento SEXO x LOCAL
        sexo_local = obj_df.cross_data(
            first_var="SEXO",
            second_var="LOCAL"
        )

        # Cruzamento LOCAL x IDADE
        local_idade = obj_df.cross_data(
            first_var="IDADE",
            second_var="LOCAL"
        )

        # Cruzamento SEXO x IDADE
        sexo_idade = obj_df.cross_data(
            first_var="SEXO",
            second_var="IDADE"
        )

        with pd.ExcelWriter("cross_analysis_results.xlsx") as writer:
            sexo_local.to_excel(writer, sheet_name="SEXO_x_LOCAL", index=False)
            local_idade.to_excel(writer, sheet_name="LOCAL_x_IDADE", index=False)
            sexo_idade.to_excel(writer, sheet_name="SEXO_x_IDADE", index=False)

