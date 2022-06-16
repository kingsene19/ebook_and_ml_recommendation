from .models import *
import pickle
from joblib import load


def load_models():
    with open("C:\\Users\\Massamba Sene\\Documents\\GIT\\DIC1\\Projets\\Projet-ML\\ebook\\boutique\\sentiment_analysis.pkl", "rb") as f:
        pipe_lr = pickle.load(f)
    with open("C:\\Users\\Massamba Sene\\Documents\\GIT\\DIC1\\Projets\\Projet-ML\\ebook\\boutique\\book_rec_model.pkl", "rb") as f:
        pipe_br = pickle.load(f)
    return pipe_lr, pipe_br


def load_data():
    pivot_df, produits = load(
        "C:\\Users\\Massamba Sene\\Documents\\GIT\\DIC1\\Projets\\Projet-ML\\ebook\\boutique\\data.joblib")
    return pivot_df, produits


def average_rating(rating_list):
    if not rating_list:
        return 0
    else:
        return round(sum(rating_list)/len(rating_list))
