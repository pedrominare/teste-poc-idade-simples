from utils.df_helper import create_df_from_large_xlsx, get_sheet_names
from utils.df_helper import validar_dado_numerico_como_string


class BuildDf:
    def __init__(self, xlsx_name, sheet_name, logging):
        self.xlsx_name = xlsx_name
        self.sheet_name = sheet_name
        self.skiprows = 6  # primeira linha com dados relevantes do arquivo xlsx
        self.chunk_size = 500  # quantidade de linhas a serem gravadas por DF.
        self.df = None
        self.variables = None
        self.years_columns_list = []
        self.columns_not_years_list = []
        self.column_total_years = "TOTAL_ANOS"
        self.logging = logging

    def get_variables(self):
        self.variables = self.df.columns.tolist()

    def build_data_frame(self):
        self.df = create_df_from_large_xlsx(
            file_name=self.xlsx_name,
            sheet_name=self.sheet_name,
            start_row=self.skiprows,
            chunk_size=self.chunk_size,
            logging=self.logging,
        )

    def define_columns(self):
        for coluna in self.variables:
            # verifica se a variavel (coluna) é ano ou nao
            if validar_dado_numerico_como_string(str(coluna)):
                self.years_columns_list.append(coluna)
            else:
                self.columns_not_years_list.append(coluna)

    # cria a coluna da soma de todos os anos por observacao.
    def build_column_total_years(self):
        # soma os valores de todos os anos disponiveis em cada observação.
        self.df[self.column_total_years] = self.df[self.years_columns_list].sum(axis=1)

    # faz o cruzamento de DFs com base em 2 variaveis (colunas).
    def cross_data(self, first_var, second_var):
        if (
            first_var in self.columns_not_years_list
            and second_var in self.columns_not_years_list
        ):
            try:
                """
                Agrupa as observações do DF por first_var e second_var,
                soma os anos e armazena na coluna self.column_total_years.
                """
                df_crossed = (
                    self.df.groupby([first_var, second_var])
                    .agg({self.column_total_years: "sum"})
                    .reset_index()
                )
            except Exception as error:
                raise Exception(
                    f"Erro ao tentar cruzar dados de {first_var} e {second_var}! {error}"
                )
        else:
            raise ValueError(
                f"As variaveis {first_var} e {second_var} não existem no df criado!"
            )

        return df_crossed
