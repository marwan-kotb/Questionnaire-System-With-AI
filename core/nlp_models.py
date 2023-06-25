import numpy as np
from scipy.special import softmax
from transformers import AutoModelForSequenceClassification, AutoTokenizer

EN_MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
en_tokenizer = AutoTokenizer.from_pretrained(EN_MODEL)
en_model = AutoModelForSequenceClassification.from_pretrained(EN_MODEL)

AR_MODEL = "CAMeL-Lab/bert-base-arabic-camelbert-da-sentiment"
ar_tokenizer = AutoTokenizer.from_pretrained(AR_MODEL)
ar_model = AutoModelForSequenceClassification.from_pretrained(AR_MODEL)


def score_english(text: str):
    """
    Predict the sentiment for a given english sentence
    -1 -> Negative
    0 -> Neutral
    1 -> Positive

    Args:
         text (str): english text to be scored

    Returns:
        (int): the predicted class for the given sample
    """
    encoded_input = en_tokenizer(
        text, return_tensors="pt", padding=True, truncation=True, max_length=64
    )
    output = en_model(**encoded_input)[0].detach().numpy()
    preds = softmax(output, axis=1)
    final_pred = np.argmax(preds, axis=1)[0]

    if final_pred == 0:
        return -1  # negative
    elif final_pred == 1:
        return 0  # neutral
    elif final_pred == 2:
        return 1  # positive


def score_arabic(text: str):
    """
    Predict the sentiment for a given arabic sentence
    -1 -> Negative
    0 -> Neutral
    1 -> Positive

    Args:
         text (str): arabic text to be scored

    Returns:
        (int): the predicted class for the given sample
    """
    encoded_input = ar_tokenizer(
        text, return_tensors="pt", padding=True, truncation=True, max_length=64
    )
    output = ar_model(**encoded_input)[0].detach().numpy()
    preds = softmax(output, axis=1)
    final_pred = np.argmax(preds, axis=1)[0]

    if final_pred == 0:
        return 1  # positive
    elif final_pred == 1:
        return -1  # negative
    elif final_pred == 2:
        return 0  # neutral
