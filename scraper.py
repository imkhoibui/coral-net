from flask import request
import pandas as pd
import requests
import os 

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

def scrap_coralnet(coral_list: pd.DataFrame, web_content):
    """
        This function scrap the 
    """
    for iter, coral in enumerate(coral_list["Names"]):
        coral_list["url"][iter] = iter
    return

def get_coral_link(url):
    url_list = []

    print("Getting coral types")
    coral_list = _get_corals("data/coral_list_apr2019.xlsx")

    web_content = requests.get(url)
    soup = BeautifulSoup(web_content.text, "html.parser")

    for link in soup.find_all("td"):

        # Split the string to get the coral name
        child = link.contents
        coral_name = child[0].string
        
        # Check if the coral name is in the list of corals
        for iter, name in enumerate(coral_list["Names"]):
            # name = name.lower()
            # coral_name = coral_name.lower()

            if name == coral_name:
                # print("Found", name)
                coral_page_link = "https://coralnet.ucsd.edu" + child[0].get("href")
                # print(child[0].get("href"))

                page_content = requests.get(coral_page_link)
                new_soup = BeautifulSoup(page_content.text, "html.parser")

                for a in new_soup.find_all("a"):
                    source = a.get("href")
                    if source[:7] == "/source" and source not in url_list:
                        url_list.append(source)

    return url_list

def get_labelset(url_list):
    source_link = "https://coralnet.ucsd.edu"
    for link in url_list:
        label_content = requests.get(source_link + link + "browse/images/")

        page_soup = BeautifulSoup(label_content.text, "html.parser")

        title = page_soup.find("h2").find("a").text

        first_image = 0

        # Accessing the page to get the number of images
        for a in page_soup.find_all("a"):
            if a.get("href")[:6] == "/image":
                first_image = int(a.get("href")[7:-6])
                print(first_image)
                break

        num_image = page_soup.find("div", {"class": "line"}).find("span").text
        num_image = int(num_image.split()[-1])

        print(num_image)

        # Create a directory for the label
        os.makedirs(os.path.join("data/scraped_dataset/", title), exist_ok=True)

        # Download image
        for i in range(first_image, first_image + num_image):
            image_soup = BeautifulSoup(source_link + f"image/{i}/view/")
            image_url = image_soup.find_all("img").get("href")
            r = requests.get(image_url, allow_redirects=True)
            

        break

if __name__ == "__main__":
    url_list = get_coral_link("https://coralnet.ucsd.edu/label/list/")
    get_labelset(url_list)