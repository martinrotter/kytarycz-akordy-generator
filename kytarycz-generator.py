from selenium import webdriver

import base64
import bs4
import pathvalidate
import time
import os.path
import argparse

def create_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filter-author", type=str, help="only process songs from specified author")
    return parser

args_parser = create_args()
args = args_parser.parse_args()

if args.help:
    args_parser.print_usage()
    exit()

filter_author = args.filter_author

opts = webdriver.ChromeOptions()
opts.add_argument("--headless=new")

driver = webdriver.Chrome(options=opts)

base_url = "https://akordy.kytary.cz"

# katalog
driver.get("https://akordy.kytary.cz/songs")

catalog = bs4.BeautifulSoup(driver.page_source, "html.parser")
catalog_authors = catalog.select(".blocklist-block")

for author in catalog_authors:   
    author_name = author.select_one(".blocklist-header > a").text
    
    if filter_author and filter_author not in author_name:
        print("Skipping author {author} ...".format(author=author_name))
        continue
    
    songs = author.select(".item > a")
    
    for song in songs:
        print()
            
        song_url = base_url + song["href"]
        print("Processing {song} ...".format(song=song_url))
        
        try:
            driver.get(song_url)
            print("Downloaded {song} ...".format(song=song_url))
            
            pdf_filename = "{tit}.pdf".format(tit=driver.title).replace(" | Akordy", "")
            pdf_filename = pathvalidate.sanitize_filename(pdf_filename)
            
            if os.path.isfile(pdf_filename):
                print("PDF file for song {song} already exists, skipping ...".format(song=song_url))
                continue
            
            pdf = driver.print_page()
            print("Printed {song} to PDF ...".format(song=song_url))

            with open(pdf_filename, 'wb') as file:
                file.write(base64.b64decode(pdf))
                
            print("Saved {song} to file ...".format(song=song_url))
            
        except Exception as e:
            print(e)
        
        time.sleep(3)

driver.quit()