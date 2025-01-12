import os
from psycopg2 import OperationalError
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()


class DbConnect:
    def __init__(self):
        self.db_host = os.getenv("DATABASE_HOST")
        self.db_port = os.getenv("DATABASE_PORT")
        self.db_user = os.getenv("DATABASE_USER")
        self.db_password = os.getenv("DATABASE_PASSWORD")
        self.db_name = os.getenv("DATABASE_NAME")
        self.engine = None
        self.Session = None
        self.session = None

    def create_connection(self):
        try:
            self.engine = create_engine(
                f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}"
            )
            self.Session = sessionmaker(bind=self.engine)
            self.session = self.Session()
            self.session.execute(text("SELECT 1;"))
            self.session.commit()
            print("Conexao ao db estabelecida!")
        except OperationalError as error:
            raise OperationalError(f"Erro ao estabelecer a conexao com o db! {error}")

    def insert_df_database(self, df_object):
        try:
            table_name = list(df_object)[0]
            df_object[table_name].to_sql(
                table_name, self.engine, if_exists="append", index=False
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
