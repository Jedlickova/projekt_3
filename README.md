# projekt_3
# Scrapování volebních výsledků
Tento projekt slouží k automatickému stažení a zpracování výsledků parlamentních voleb z webových stránek [volby.cz](https://www.volby.cz) a uložení výsledků do csv souboru. Do tohoto souboru se uloží volební výsledky všech kandidujících stran pro všechny obce v daném územním celku. Kód využívá knihovny `requests` a `BeautifulSoup` pro stáhnutí a zpracování dat, knihovnu `csv` k vytvoření .csv souboru a knihovnu sys k získání argumentů z příkazové řádky.
## Instalace
### 1. Vytvoření virtuálního prostředí
Virtuální prostředí zajistí, že všechny knihovny budou nainstalovány v izolovaném prostředí.
```bash
python -m venv virtual_prostredi_projekt_3
```
### 2. Aktivace virtuálního prostředí
```bash
virtual_prostredi_projekt_3\Scripts\Activate
```
### 3. Instalace knihoven
Instalace externích knihoven potřebných ke stahování a úpravě dat:
```bash
pip install beautifulsoup4
pip install requests
```
pokud už je k dispozici soubor se seznamem knihoven, mohou být potřebné knihovny nainstalovány:
```bash
pip install -r requirements.txt
```
### 4. Vypsání knihoven do souboru
Vypsání nainstalovaných knihoven do souboru requirements.txt:
```bash
pip freeze > requirements.txt
```
## Spuštění programu
### 1. Stažení projektu
Kód je možné stáhnout pomocí:
```bash
git clone https adresa na github
cd scraping-volny
```
### 2. Spuštění skriptu
Skript se spouští pomocí dvou argumentů:
platná URL adresa stránky [volby.cz] s výběrem obce a název výstupního CSV souboru. Pro spuštění skriptu je možné použít následující příkaz. Tento příkaz stáhne volební výsledky z konkrétního odkazu a uloží je do CSV souboru.

#### Správně zadaný příkaz:
Platnou URL získáte na stránce https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ kliknutím na „X“ ve sloupci Výběr obce.
```bash
python main.py "platna_URL" "vystup.csv"
```
Výstup:
```bash
Data byla úspěšně uložena do vystup.csv
```
#### Chybně zadaný první argument - nesprávná URL adresa:
```bash
python main.py "nesprávná_URL" "vystup.csv"
```
Výstup:
```bash
Argument neobsahuje správný odkaz
```
#### Chybně zadaný první argument - není URL adresa:
```bash
python main.py "vystup.csv" "platna_URL"
```
Výstup:
```bash
První argument není platná URL: neplatna_URL
```
#### Chybně zadaný druhý argument:
```bash
python main.py "platna_URL" "neplatny_csv_soubor"
```
Výstup:
```bash
Druhý argument není platný CSV soubor
```
### 3. Příklad správného použití
```bash
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=10&xnumnuts=6104" "trebic.csv"
```
Výstup:
```bash
Data byla úspěšně uložena do trebic.csv
```
