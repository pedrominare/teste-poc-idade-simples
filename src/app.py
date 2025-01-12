import os.path
from time import sleep

from database.postgresql_connection import DbConnect
from database.queries import query_sexo_local, query_idade_local, query_sexo_idade
from run.data_crossing import DataCrossing

from sqlalchemy import text

from run.trace_malloc import MemoryUse

# cria objeto de monitoramento de consumo de memoria
obj_memory_usage = MemoryUse()
obj_memory_usage.add_checkpoint(name="Start to run")

# caminho da fonte de dados
path_xlsx = os.path.join(os.getcwd(), 'projecoes_2024_tab1_idade_simples.xlsx')

# data_crossing(path_xlsx=path_xlsx)
obj_memory_usage.add_checkpoint(name="Building DataFrame From xlsx file")
obj_data = DataCrossing(
    path_xlsx=path_xlsx
)

# esse metodo cria 1 objeto da classe BuildDF por planilha do arquivo xlsx.
obj_data.build_df()
obj_memory_usage.add_checkpoint(name="Crossing SEXO and LOCAL")
# os nomes das tabelas estao nas chaves dos dicts -> nome_tabela: df
# estao em df_cross_result
obj_data.run_crossing(
    first_var="SEXO",
    second_var="LOCAL"
)
obj_memory_usage.add_checkpoint(name="Crossing IDADE and LOCAL")
obj_data.run_crossing(
    first_var="IDADE",
    second_var="LOCAL"
)
obj_memory_usage.add_checkpoint(name="Crossing SEXO and IDADE")
obj_data.run_crossing(
    first_var="SEXO",
    second_var="IDADE"
)

obj_db = None
try:
    # conectar ao banco de dados
    obj_memory_usage.add_checkpoint(name="Connecting to database")
    obj_db = DbConnect()

    # estabele a conexao com o db
    obj_db.create_connection()

    # limpa tabelas anteriores do banco com o mesmo nome
    print("Limpando db anterior...")
    obj_db.run_sql_command(text("DROP TABLE IF EXISTS sexo_local, idade_local, sexo_idade CASCADE;"))
    print("DB limpo!")
    sleep(5)

    # criando as tabelas por meio de queries pré-definidas
    print("Criando as tabelas para inserir os DFs...")
    obj_memory_usage.add_checkpoint(name="Creating tables in database")
    obj_db.run_sql_command(query_sexo_local)
    obj_db.run_sql_command(query_idade_local)
    obj_db.run_sql_command(query_sexo_idade)

    # criar um laco para iterar sobe obj_data.df_cross_result e obter os nomes das chaves e os dfs correspondentes.
    for df_object in obj_data.df_cross_result:
        # o comando to_sql permite inserir os dados no banco direto do DF sem criar previamente as tabelas.
        obj_memory_usage.add_checkpoint(name=f"Saving {list(df_object)[0]} data to database.")
        obj_db.insert_df_database(df_object)

    # fim da execucao do codigo
    obj_memory_usage.stop_checkpoint()
finally:
    if obj_db:
        obj_db.end_connection()
