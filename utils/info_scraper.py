import os
import psycopg2
import pandas as pd
from flask import request
from bs4 import BeautifulSoup

def _get_corals(data_file):
    """
        This function retrieves and returns a data frame of coral types
        ----------
        Parameters:
        - data_file
        Returns:
        - coral_list (pd.DataFrame):
    """
    coral_list = pd.read_excel(data_file, 0, usecols="A")[:-1]
    coral_list = coral_list.dropna()

    return coral_list.rename(columns = {"Unnamed: 0" :"Names"})


def _get_coral_data():
    """
        This function retrieves coral's information from (www.coralsoftheworld.org)

    """
    return

if __name__ == "__main__":
    _get_coral_data()