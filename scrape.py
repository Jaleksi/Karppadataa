import requests
from bs4 import BeautifulSoup
from gameData import gameData
import csv

def tositoimet():
    
    url = "http://www.eurohockey.com/games.html?id_show=2&date_from=21.10.2009&date_to=21.10.2019&id_country=3&id_league=128-liiga.html&club_name=K%C3%A4rp%C3%A4t+oulu&id_season=0&list_number=-1"

    raw = requests.get(url)
    soup = BeautifulSoup(raw.content, 'html.parser')
    alku = "http://www.eurohockey.com"

    element = soup.select("a[href*=detail]")

    found = []

    with open("karppadataa.csv", "w") as kiekkocsv:
        fwriter = csv.writer(kiekkocsv, delimiter=",", quotechar="|",
        quoting=csv.QUOTE_MINIMAL)
        fwriter.writerow(["Spectators", "Year", "Month", "Weekday", "Date",
        "Timevalue", "Time", "Won", "Score", "Homegame", "Opponent"])

        for i in element:
            link = i['href']
            idNum = "".join(filter(lambda x: x.isdigit(), link))
            if idNum not in found:
                found.append(idNum)
                fwriter.writerow(gameData(alku+link))

if __name__ == "__main__":
    tositoimet()
