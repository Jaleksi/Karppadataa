import requests
from bs4 import BeautifulSoup
import datetime


# [yleisö, vuosi, kuukausi, viikonpäivä, pvm, aika-arvo, aika, voitto, tulos, kotiottelu, vastus]
def gameData(url):
    data = []
    raw = requests.get(url)
    soup = BeautifulSoup(raw.content, 'html.parser')


    #Yleisö
    peopleData = soup.find_all('tr', {'class': 'first noborder dark'})
    try:
        data.append(int("".join(peopleData[1].select('b')[1].next_sibling[2:])))
    except Exception:
        data.append("NULL")

    # Date
    dataSlice = soup.find("td")
    try:
        gameDate = "".join(dataSlice.find('a').contents)
        for a in dateArvo(gameDate):
            data.append(a)
    except Exception:
        for _ in range(4):
            data.append("NULL")
    
    # Time: klo <15 = 0, 15-18 = 1, >18 = 2
    try:
        time = "".join(dataSlice.find('b').previous_sibling)[2:7]
        data.append(timeArvo(int(time[:2])))
        data.append(time)
    except Exception:
        for _ in range(2):
            data.append("NULL")

    # Voitto
    try:
        koti = "".join(peopleData[0].find_all('td')[0].contents)
        vieras = "".join(peopleData[0].find_all('td')[2].contents)
        tulos = "".join(peopleData[0].find_all('td')[1].contents)
        
        if voitto(koti, vieras, tulos[:3]):
            data.append(1)
        else:
            data.append(0)
    except Exception:
        data.append("NULL")

    #Lopputulos
    try:
        data.append(tulos[:3])
    except Exception:
        data.append("NULL")
        


    # Kotiottelu ja vastustaja
    try:
        if koti.lower() == "kärpät oulu":
            data.append(1)
            data.append(vieras)
        else:
            data.append(0)
            data.append(koti)

    except Exception:
        for _ in range(2):
            data.append("NULL")



    return data

def timeArvo(time): # Kellonaika vertailtavassa muodossa
    if time > 15:
        if time > 18:
            return 2
        else:
            return 1
    else:
        return 0

def dateArvo(date):
    date = date.split()
    months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep",
    "oct", "nov", "dec"]

    year = int(date[2][2:])
    month = int(months.index(date[1].lower()))
    weekday = datetime.datetime(int("20"+str(year)), month+1, int(date[0])).weekday()
    realdate = "20"+str(year)+"-"+str(month+1)+"-"+str(int(date[0]))
    return [year, month, weekday, realdate]


def voitto(koti, vieras, tulos):
    if koti.lower() == "kärpät oulu":
        return int(tulos[0]) > int(tulos[2])
    else:
        return int(tulos[2]) > int(tulos[0])





if __name__ == "__main__":
    url = "http://www.eurohockey.com/game/detail/167844-ifk-helsinki--krpt-oulu.html"
    print(gameData(url))
