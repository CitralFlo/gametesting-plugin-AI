## api.py
from flask import Flask, request, jsonify
from flasgger import Swagger
from ai_model import AIModel
from db_connector import DBConnector
from data_collector import DataCollector
from grammar_checker import GrammarChecker
import pandas as pd

class API:
    def __init__(self):
        self.app = Flask(__name__)
        self.swagger = Swagger(self.app)
        self.ai_model = AIModel()
        self.db_connector = DBConnector()
        self.data_collector = DataCollector()
        self.grammar_checker = GrammarChecker()

        @self.app.route('/train', methods=['POST'])
        def train():
            """
            Train the AI model
            ---
            parameters:
              - name: body
                in: body
                required: true
                schema:
                  type: object
                  properties:
                    data:
                      type: array
                      items:
                        type: object
            responses:
              200:
                description: Training successful
            """
            data = pd.DataFrame(request.json['data'])
            self.ai_model.train(data)
            return jsonify({"message": "Training successful"}), 200

        @self.app.route('/predict', methods=['POST'])
        def predict():
            """
            Predict the test result
            ---
            parameters:
              - name: body
                in: body
                required: true
                schema:
                  type: object
                  properties:
                    description:
                      type: string
            responses:
              200:
                description: Prediction successful
            """
            description = request.json['description']
            prediction = self.ai_model.predict(description)
            return jsonify({"prediction": prediction}), 200

    def start(self):
        self.app.run(debug=True)
