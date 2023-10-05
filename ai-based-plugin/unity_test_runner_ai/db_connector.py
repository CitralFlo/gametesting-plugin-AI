## db_connector.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from typing import Optional
import logging

class DBConnector:
    def __init__(self, user: str = "root", password: str = "", host: str = "localhost", port: str = "3306"):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.engine = None
        self.session = None

    def create_engine(self, db_name: str):
        try:
            connection_string = f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db_name}"
            self.engine = create_engine(connection_string)
        except Exception as e:
            logging.error(f"Failed to create engine: {e}")
            self.engine = None

    def create_session(self):
        try:
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
        except Exception as e:
            logging.error(f"Failed to create session: {e}")
            self.session = None

    def connect(self, db_name: str):
        self.create_engine(db_name)
        if self.engine is not None:
            self.create_session()

    def get_data(self, table_name: str) -> Optional[pd.DataFrame]:
        if self.engine is not None:
            try:
                data = pd.read_sql_table(table_name, self.engine)
                return data
            except Exception as e:
                logging.error(f"Failed to get data from table {table_name}: {e}")
                return None
        else:
            logging.error("No connection to the database. Please connect first.")
            return None

    def update_data(self, table_name: str, data: pd.DataFrame):
        if self.engine is not None:
            try:
                data.to_sql(table_name, self.engine, if_exists='replace')
            except Exception as e:
                logging.error(f"Failed to update data to table {table_name}: {e}")
        else:
            logging.error("No connection to the database. Please connect first.")

    def close(self):
        if self.session is not None:
            self.session.close()
        if self.engine is not None:
            self.engine.dispose()
