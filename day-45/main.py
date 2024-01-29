import requests
from bs4 import BeautifulSoup
import time

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

# Write your code below this line 👇

r = requests.get(URL)
response = r.content
#print(response)

soup = BeautifulSoup(response, 'html.parser')
#print(soup)
movie_list = soup.find_all("h3", class_="title")
#print(movie_list)
movie_list.reverse()

with open("movies.txt", "w") as file:
    for name in movie_list:
        time.sleep(0.5)
        #print(name.getText())
        movie_titles = name.getText()
        print(movie_titles)
        file.write(f"{movie_titles}\n")

