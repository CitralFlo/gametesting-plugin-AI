## main.py
from ai_model import AIModel
from db_connector import DBConnector
from data_collector import DataCollector
from grammar_checker import GrammarChecker
from api import API
import pandas as pd

class Main:
    def __init__(self):
        self.ai_model = AIModel()
        self.db_connector = DBConnector()
        self.data_collector = DataCollector()
        self.grammar_checker = GrammarChecker()
        self.api = API()

    def run(self):
        try:
            # Connect to the database
            self.db_connector.connect("test_db")

            # Collect data
            data = self.data_collector.collect_data()

            # Train the AI model
            self.ai_model.train(data)

            # Start the API
            self.api.start()
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main = Main()
    main.run()
