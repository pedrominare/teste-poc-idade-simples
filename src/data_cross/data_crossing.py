from data_frames.build_df import BuildDf
from database.postgresql_connection import DbConnect
from utils.df_helper import get_sheet_names
from sqlalchemy import text
from database.queries import query_sexo_local, query_idade_local, query_sexo_idade


class DataCrossing(BuildDf):
    def __init__(self, xlsx_name, logging, memory_usage):
        super().__init__(xlsx_name, sheet_name="", logging=logging)
        self.logging = logging
        self.memory_usage = memory_usage
        self.obj_list = []
        self.df_cross_result = []

    def run(self):
        self.logging.info("Construindo DataFrames a partir do arquivo xlsx...")
        self.memory_usage.add_checkpoint(
            name="Construindo DFs a partir do arquivo xlsx"
        )

        self.build_df()

        # Executar os cruzamentos de variáveis
        self.logging.info("Executando cruzamento de SEXO e LOCAL...")
        self.memory_usage.add_checkpoint(name="Executando cruzamento de SEXO e LOCAL")
        self.run_crossing(first_var="SEXO", second_var="LOCAL")

        self.logging.info("Executando cruzamento de IDADE e LOCAL...")
        self.memory_usage.add_checkpoint(name="Executando cruzamento de IDADE e LOCAL")
        self.run_crossing(first_var="IDADE", second_var="LOCAL")

        self.logging.info("Executando cruzamento de SEXO e IDADE...")
        self.memory_usage.add_checkpoint(name="Executando cruzamento de SEXO e IDADE")
        self.run_crossing(first_var="SEXO", second_var="IDADE")

    def save_data_to_db(self):
        obj_db = DbConnect(logging=self.logging)
        try:
            # Conectar ao banco de dados
            self.logging.info("Conectando ao banco de dados...")
            self.memory_usage.add_checkpoint(name="Conectando ao banco de dados")
            obj_db.create_connection()

            # Limpar tabelas anteriores
            self.logging.info("Limpando db anterior...")
            self.memory_usage.add_checkpoint(name="Limpando db anterior")
            obj_db.run_sql_command(
                text(
                    "DROP TABLE IF EXISTS sexo_local, idade_local, sexo_idade CASCADE;"
                )
            )
            self.logging.info("DB limpo!")

            # Criar tabelas e inserir dados
            self.logging.info("Criando tabelas e inserindo dados...")
            self.memory_usage.add_checkpoint(name="Criando tabelas e inserindo dados")
            obj_db.run_sql_command(query_sexo_local)
            obj_db.run_sql_command(query_idade_local)
            obj_db.run_sql_command(query_sexo_idade)

            for df_object in self.df_cross_result:
                table_name = list(df_object)[0]
                self.logging.info(f"Salvando DF na tabela {table_name}...")
                self.memory_usage.add_checkpoint(name=f"Salvando DF em {table_name}")
                obj_db.insert_df_database(df_object)

        finally:
            obj_db.end_connection()
            self.memory_usage.add_checkpoint(
                name=f"Conexão com o banco de dados encerrada."
            )
            self.memory_usage.stop_checkpoint()

    def build_df(self):
        # obtem nomes das planilhas do xlsx
        sheet_names_xlsx = get_sheet_names(self.xlsx_name)

        """
            Obtem dados da planilha
            Caso haja mais de 1 planilha por pasta de trabalho,
            navega em todas
        """

        for sheet in sheet_names_xlsx:
            obj_df = BuildDf(
                xlsx_name=self.xlsx_name, sheet_name=sheet, logging=self.logging
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
