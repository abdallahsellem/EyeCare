import pandas as pd
import numpy
import pickle
import tensorflow as tf
from transformers import XLNetTokenizer


# Tokenize the data
def tokenize_texts(texts, tokenizer):
    if isinstance(texts, pd.Series):
        texts = texts.tolist()
    return tokenizer(
        texts,
        max_length=128,
        padding='max_length',  # Ensure all sequences are padded to max_length
        truncation=True,
        return_tensors='tf'
    )

# Function to load and predict
def load_and_predict(description, model_path, encoder_path):
    # Load the model
    model = tf.keras.models.load_model(model_path)

    # Preprocess the input description
    tokenized_input = tokenize_texts([description], token)
    prediction = model.predict \
        ({'input_ids': tokenized_input['input_ids'], 'attention_mask': tokenized_input['attention_mask']})

    # Load the team_encoder
    with open(encoder_path, 'rb') as f:
        encoder = pickle.load(f)

    predicted_index = np.argmax(prediction, axis=1)[0]
    prediction = encoder.inverse_transform([predicted_index])[0]

    return prediction



# load tokenizer and model
token = XLNetTokenizer.from_pretrained('xlnet-base-cased')


# Example usage
description = "Unable to delete workspace"
predicted_pri = load_and_predict(description, 'priority_classification.keras', 'priority_encoder.pkl')
predicted_team = load_and_predict(description, 'teams_classification.keras', 'team_encoder.pkl')

print(f'The predicted priority is: {predicted_pri} and predicted assigned team {predicted_team}')
