from selenium import webdriver
from selenium.webdriver.common.print_page_options import PrintOptions

import base64
import bs4
import pathvalidate
import time
import os.path
import argparse

base_url = "https://akordy.kytary.cz"

def create_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filter-author", type=str, help="only process songs from specified author")
    return parser

def initialize_driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument("--headless=new")

    return webdriver.Chrome(options=opts)

def construct_pdf_filename(author_name: str, song_name: str):
    pdf_filename = "{auth} - {song}.pdf".format(auth=author_name, song=song_name)
    pdf_filename = pathvalidate.sanitize_filename(pdf_filename)
    return pdf_filename

def process_songs(driver: webdriver.Chrome, author: dict):
    author_html = author["html"]
    author_name = author["name"]
    songs = author_html.select(".item > a")
    
    for song in songs:
        song_name = song.get_text(strip=True)
        song_url = base_url + song["href"]
        pdf_filename = construct_pdf_filename(author_name, song_name)
        
        if os.path.isfile(pdf_filename):
            print("PDF file for song {song} already exists, skipping ...".format(song=song_name))
            continue

        print("Processing {song} ...".format(song=song_name))
        
        try:
            driver.get(song_url)
            print("Downloaded {song} ...".format(song=song_name))
            
            pdf_opts = PrintOptions()
            pdf_opts.background = False
            pdf_opts.margin_bottom = 0.7
            pdf_opts.margin_top = 0.7
            pdf_opts.margin_left = 0.45
            pdf_opts.margin_right = 0.45
            
            pdf = driver.print_page(pdf_opts)
            print("Printed {song} to PDF ...".format(song=song_name))

            with open(pdf_filename, 'wb') as file:
                file.write(base64.b64decode(pdf))
                
            print("Saved {song} to file ...".format(song=song_name))
            
        except Exception as e:
            print(e)
        
        time.sleep(3)

def load_catalog_get_authors(driver: webdriver.Chrome):
    driver.get(base_url + "/songs")
    
    authors = list()
    catalog = bs4.BeautifulSoup(driver.page_source, "html.parser")
    catalog_authors = catalog.select(".blocklist-block")
    
    for author_html in catalog_authors:
        author_name = author_html.select_one(".blocklist-header > a").text
        authors.append(dict(name=author_name, html=author_html))
        
    return authors

def main():
    args_parser = create_args()
    args = args_parser.parse_args()
    filter_author = args.filter_author
    driver = initialize_driver()

    # Get full catalog.
    catalog_authors = load_catalog_get_authors(driver)

    for author in catalog_authors:
        author_name = author["name"]
        
        if filter_author and filter_author not in author_name:
            print("Skipping author {author} ...".format(author=author_name))
        else:
            print("Processing author {author} ...".format(author=author_name))
            process_songs(driver, author)


    driver.quit()

if __name__=="__main__":
    main()