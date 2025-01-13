from data_frames.build_df import BuildDF
from utils.df_helper import get_sheet_names


class DataCrossing:
    def __init__(self, path_xlsx):
        self.path_xlsx = path_xlsx
        self.obj_list = []
        self.df_cross_result = []

    def build_df(self):
        # obtem nomes das planilhas do xlsx
        sheet_names_xlsx = get_sheet_names(self.path_xlsx)

        """
            Obtem dados da planilha
            Caso haja mais de 1 planilha por pasta de trabalho,
            navega em todas
        """

        for sheet in sheet_names_xlsx:
            obj_df = BuildDF(
                xlsx_name=self.path_xlsx,
                sheet_name=sheet,
            )

            # gera o DF do arquivo
            obj_df.build_data_frame()

            # carrega as variaveis do DF criado
            obj_df.get_variables()

            # obtem os nomes das variaveis (colunas) do DF
            obj_df.define_columns()

            # Soma todos os anos em uma nova coluna 'TOTAL'
            obj_df.build_column_total_years()

            self.obj_list.append(obj_df)

    def run_crossing(self, first_var: str, second_var: str):
        for obj in self.obj_list:
            df_cross_result = obj.cross_data(first_var=first_var, second_var=second_var)
            # o nome de cada DF sera first_var_second_var
            description = {
                f"{str(first_var).lower()}_{str(second_var).lower()}": df_cross_result
            }
            self.df_cross_result.append(description)
