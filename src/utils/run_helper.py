from database.postgresql_connection import DbConnect
from sqlalchemy import text
from database.queries import query_sexo_local, query_idade_local, query_sexo_idade


def build_df_cross_data(obj_memory_usage, obj_data, logging):
    logging.info("Construindo DataFrames a partir do arquivo xlsx...")
    obj_memory_usage.add_checkpoint(name="Construindo DFs a partir do arquivo xlsx")

    obj_data.build_df()

    # Executar os cruzamentos de variáveis
    logging.info("Executando cruzamento de SEXO e LOCAL...")
    obj_memory_usage.add_checkpoint(name="Executando cruzamento de SEXO e LOCAL")
    obj_data.run_crossing(first_var="SEXO", second_var="LOCAL")

    logging.info("Executando cruzamento de IDADE e LOCAL...")
    obj_memory_usage.add_checkpoint(name="Executando cruzamento de IDADE e LOCAL")
    obj_data.run_crossing(first_var="IDADE", second_var="LOCAL")

    logging.info("Executando cruzamento de SEXO e IDADE...")
    obj_memory_usage.add_checkpoint(name="Executando cruzamento de SEXO e IDADE")
    obj_data.run_crossing(first_var="SEXO", second_var="IDADE")


def save_data_to_db(obj_memory_usage, obj_data, logging):
    obj_db = None
    try:
        # Conectar ao banco de dados
        logging.info("Conectando ao banco de dados...")
        obj_memory_usage.add_checkpoint(name="Conectando ao banco de dados")
        obj_db = DbConnect()
        obj_db.create_connection()

        # Limpar tabelas anteriores
        logging.info("Limpando db anterior...")
        obj_memory_usage.add_checkpoint(name="Limpando db anterior")
        obj_db.run_sql_command(
            text("DROP TABLE IF EXISTS sexo_local, idade_local, sexo_idade CASCADE;")
        )
        logging.info("DB limpo!")

        # Criar tabelas e inserir dados
        logging.info("Criando tabelas e inserindo dados...")
        obj_memory_usage.add_checkpoint(name="Criando tabelas e inserindo dados")
        obj_db.run_sql_command(query_sexo_local)
        obj_db.run_sql_command(query_idade_local)
        obj_db.run_sql_command(query_sexo_idade)

        for df_object in obj_data.df_cross_result:
            table_name = list(df_object)[0]
            logging.info(f"Salvando DF em {table_name}...")
            obj_memory_usage.add_checkpoint(name=f"Salvando DF em {table_name}")
            obj_db.insert_df_database(df_object)

    finally:
        if obj_db:
            obj_db.end_connection()
            logging.info("Conexão com o banco de dados encerrada.")
            obj_memory_usage.add_checkpoint(
                name=f"Conexão com o banco de dados encerrada."
            )
            obj_memory_usage.stop_checkpoint()
