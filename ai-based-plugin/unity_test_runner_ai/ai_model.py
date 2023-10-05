## ai_model.py
import tensorflow as tf
from tensorflow.keras import layers, preprocessing
from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np

class AIModel:
    def __init__(self):
        self.model = None
        self.tokenizer = preprocessing.text.Tokenizer()
        self.encoder = LabelEncoder()

    def preprocess_data(self, data: pd.DataFrame):
        # Tokenize the descriptions
        descriptions = data['description'].tolist()
        self.tokenizer.fit_on_texts(descriptions)
        sequences = self.tokenizer.texts_to_sequences(descriptions)
        padded_sequences = preprocessing.sequence.pad_sequences(sequences, padding='post')

        # Encode the labels
        labels = self.encoder.fit_transform(data['label'])

        return padded_sequences, labels

    def create_model(self):
        # Create a simple sequential model
        self.model = tf.keras.Sequential([
            layers.Embedding(input_dim=5000, output_dim=16),
            layers.GlobalAveragePooling1D(),
            layers.Dense(16, activation='relu'),
            layers.Dense(1, activation='sigmoid')
        ])

        # Compile the model
        self.model.compile(optimizer='adam',
                           loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                           metrics=['accuracy'])

    def train(self, data: pd.DataFrame):
        # Preprocess the data
        sequences, labels = self.preprocess_data(data)

        # Split the data into training and validation sets
        train_sequences, val_sequences, train_labels, val_labels = train_test_split(sequences, labels, test_size=0.2)

        # Create the model
        self.create_model()

        # Train the model
        self.model.fit(train_sequences, train_labels, epochs=30, validation_data=(val_sequences, val_labels), verbose=2)

    def predict(self, description: str) -> str:
        # Tokenize the description
        sequence = self.tokenizer.texts_to_sequences([description])
        padded_sequence = preprocessing.sequence.pad_sequences(sequence, padding='post')

        # Predict the label
        prediction = self.model.predict(padded_sequence)

        # Decode the label
        label = self.encoder.inverse_transform([np.argmax(prediction)])

        return label[0]
