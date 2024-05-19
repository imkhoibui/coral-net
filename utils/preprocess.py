import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By

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
    coral_list = coral_list.rename(columns = {"Unnamed: 0" :"species"})
    prefix = "www.coralsoftheworld.org/species_factsheets/species_factsheets_summary/"
    for i in range(len(coral_list)):
        name = coral_list.iloc[i]['species']
        coral_list.iloc[i]['species'] = _clean_name(name)
    coral_list['links'] = prefix + coral_list['species'].str.split(" ").str.join("-")
    return coral_list

def _clean_name(coral_name):
    coral_name = coral_name.replace(".", "")
    coral_name = coral_name.lower().strip()
    coral_name = _click_element(coral_name)
    return coral_name

def _click_element(coral_name):
    driver = webdriver.Edge()
    driver.get("www.coralsoftheworld.org/species_factsheets/species_factsheets_summary/")
    species = driver.find_elements(By.TAG_NAME, "li")

    for specie in species:
        specie.click()

    return species

if __name__ == "__main__":
    data = _get_corals("data/coral_list_apr2019.xlsx")
    print(data.head())