import os
from psycopg2 import OperationalError
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()


class DbConnect:
    def __init__(self, logging):
        self.db_host = os.getenv("DATABASE_HOST")
        self.db_port = os.getenv("DATABASE_PORT")
        self.db_user = os.getenv("DATABASE_USER")
        self.db_password = os.getenv("DATABASE_PASSWORD")
        self.db_name = os.getenv("DATABASE_NAME")
        self.engine = None
        self.Session = None
        self.session = None
        self.logging = logging

    def create_connection(self):
        self.create_eng()
        self.create_session()
        self.connection_test()

    def create_session(self):
        try:
            if self.Session is None:
                self.Session = sessionmaker(bind=self.engine)
                self.logging.info("sessionmaker Criado!")
            else:
                self.logging.info("Utilizando sessionmaker criada anteriormente...")

            if self.session is None:
                self.session = self.Session()
                self.logging.info("sessao criada!")
            else:
                self.logging.info("Utilizando session criada anteriormente...")
        except OperationalError as error:
            raise OperationalError(f"Erro ao criar session para conexao ao db! {error}")

    def create_eng(self):
        try:
            if self.engine is None:
                self.engine = create_engine(
                    f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}"
                )
                self.logging.info("Engine criada!")
            else:
                self.logging.info("Utilizando engine criada anteriormente...")
        except OperationalError as error:
            raise OperationalError(f"Erro ao criar engine para conexao ao db! {error}")

    def connection_test(self):
        try:
            self.session.execute(text("SELECT 1;"))
            self.session.commit()
            self.logging.info("Conexão ao DB estabelecida!")
        except OperationalError as error:
            raise OperationalError(f"Erro ao testar conexao ao db! {error}")

    def insert_df_database(self, df_object):
        try:
            table_name = list(df_object)[0]
            df_object[table_name].to_sql(
                table_name, self.engine, if_exists="append", index=False
            )
            self.logging.info(f"DF {table_name} inserido no DB!")
        except Exception as error:
            raise Exception(f"Erro ao tentar inserir o DF no banco! {error}")

    def end_connection(self):
        self.session.close()
        self.logging.info("Sessao ao DB encerrada!")

    def run_sql_command(self, sql_command):
        try:
            self.session.execute(sql_command)
            self.session.commit()
        except Exception as error:
            raise Exception(f"Erro ao executar comando SQL! {error}")
