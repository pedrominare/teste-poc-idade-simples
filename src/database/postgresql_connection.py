import os
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DbConnect:
    def __init__(self):
        self.db_host = os.getenv('DATABASE_HOST')
        self.db_port = os.getenv('DATABASE_PORT')
        self.db_user = os.getenv('DATABASE_USER')
        self.db_password = os.getenv('DATABASE_PASSWORD')
        self.db_name = os.getenv('DATABASE_NAME')
        # self.cursor = None
        # self.connection = None
        self.engine = create_engine(
            f'postgresql://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}'
        )
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def insert_df_database(self, df_object):
        try:
            table_name = list(df_object)[0]
            df_object[table_name].to_sql(
                table_name,
                self.engine,
                if_exists='append',
                index=False
            )
        except Exception as error:
            raise Exception(f"Erro ao tentar inserir o DF no banco! {error}")

    def end_connection(self):
        self.session.close()

    def run_sql_command(self, sql_command):
        try:
            self.session.execute(sql_command)
            self.session.commit()
        except Exception as error:
            raise Exception(f"Erro ao executar comando SQL! {error}")

    """
    def create_connection_psycopg2(self):
        try:
            self.connection = psycopg2.connect(
                host=self.db_host,
                port=self.db_port,
                user=self.db_user,
                password=self.db_password,
                dbname=self.db_name
            )
            self.cursor = self.connection.cursor()

        except Exception as error:
            raise Exception(f"Erro ao conectar ou criar tabelas: {error}")

    def run_sql_command_psycopg2(self, sql_command):
        try:
            self.cursor.execute(sql_command)
            self.connection.commit()
            print("Comando SQL executado!")
        except Exception as error:
            raise Exception(f"Erro ao executar comando SQL! {error}")
        
    def end_connection_psycopg2(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
    """