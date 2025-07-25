"""
main.py: třetí projekt do Engeto Online Python Akademie
author: Monika Jedličková
email: mcmilica@centrum.cz
"""

from bs4 import BeautifulSoup
import requests
import csv
import sys


def ziskej_odpoved_serveru(url):
    odpoved = requests.get(url)
    return odpoved.text


def ziskej_strukturovany_dokument(html):
    polivka = BeautifulSoup(html, features="html.parser")
    return polivka


def ziskej_data(polivka):
    data = []
    strany = []
    obec_td_list = polivka.find_all("td", {"class": "overflow_name"})
    for obec_td in obec_td_list:
        nazev_obce = obec_td.text.strip()
        cislo_obce = obec_td.find_previous("td").text.strip()

        cislo_obce = obec_td.find_previous("td").text.strip()
        url_vyber_okrsku = (
            "https://www.volby.cz/pls/ps2017nss/"
            + obec_td.find_next("td").find("a")["href"]
        )
        html = ziskej_odpoved_serveru(url_vyber_okrsku)
        polivka_obce = ziskej_strukturovany_dokument(html)
        obec = [cislo_obce, nazev_obce] + ziskej_data_obce(polivka_obce, strany)
        data.append(obec)
    return data, strany


def ziskej_data_obce(polivka, strany):
    data_obce = []
    okrsek = polivka.find("th", {"id": "s1"})
    if okrsek is not None:
        okrsek_td_list = polivka.find_all("td", {"headers": "s1"})
        for okrsek_td in okrsek_td_list:
            odkaz = okrsek_td.find("a")
            if odkaz is not None:
                url_okrsek = "https://www.volby.cz/pls/ps2017nss/" + odkaz["href"]
                html = ziskej_odpoved_serveru(url_okrsek)
                polivka_okrsku = ziskej_strukturovany_dokument(html)
                data_okrsku = ziskej_data_okrsku(polivka_okrsku, strany)
                if len(data_obce):
                    for i in range(len(data_obce)):
                        data_obce[i] = int(data_obce[i]) + int(data_okrsku[i])
                else:
                    data_obce = data_okrsku
    else:
        data_obce = ziskej_data_okrsku(polivka, strany)
    return data_obce


def ziskej_data_okrsku(polivka, strany):
    volici = polivka.find("td", {"headers": "sa2"}).text.strip().replace("\xa0", "")
    obalky = polivka.find("td", {"headers": "sa5"}).text.strip().replace("\xa0", "")
    hlasy = polivka.find("td", {"headers": "sa6"}).text.strip().replace("\xa0", "")
    data = [volici, obalky, hlasy]
    strany_celkem_td_list_list = [
        polivka.find_all("td", {"class": "cislo", "headers": "t1sa2 t1sb3"}),
        polivka.find_all("td", {"class": "cislo", "headers": "t2sa2 t2sb3"}),
    ]

    if not len(strany):
        strana_td_list = polivka.find_all("td", {"class": "overflow_name"})
        for strana_td in strana_td_list:
            strana = strana_td.text.strip()
            strany.append(strana)

    for strany_celkem_td_list in strany_celkem_td_list_list:
        for strany_celkem_td in strany_celkem_td_list:
            celkem = strany_celkem_td.text.strip().replace("\xa0", "")
            if celkem.isnumeric():
                data.append(celkem)
    return data


def uloz_do_csv(data, strany, soubor):
    with open(soubor, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "Kód obce",
                "Název obce",
                "Voliči v seznamu",
                "Vydané obálky",
                "Platné hlasy",
            ]
            + strany
        )
        writer.writerows(data)


def main(url, soubor):
    html = ziskej_odpoved_serveru(url)
    polivka = ziskej_strukturovany_dokument(html)
    data, strany = ziskej_data(polivka)

    if not data:
        print("Argument neobsahuje správný odkaz")
    else:
        uloz_do_csv(data, strany, soubor)
        print(f" Data byla úspěšně uložena do {soubor}")

#HLAVNÍ VSTUPNÍ BOD PROGRAMU

def je_url(text):
    return text.startswith("http://") or text.startswith("https://")

def je_csv_soubor(text):
    return text.endswith(".csv")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Musíte zadat přesně 2 argumenty - URL a název výstupního souboru .csv")
    else:
        url = sys.argv[1]
        csv_soubor = sys.argv[2]

        if not je_url(url):
            print(f"První argument není platná URL: {url}")

        elif not je_csv_soubor(csv_soubor):
            print(f"Druhý argument není platný CSV soubor_ {csv_soubor}")
        
        else:
            main(url, csv_soubor)