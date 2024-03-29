# Code voor de robot spin van groep 9.
### Links
https://sites.google.com/view/robotspin/home

https://github.com/pprotas/robot-spider

## Installatie
### Python 3.7
Installeer **Python 3.7** voor jouw OS [hier](https://wiki.python.org/moin/BeginnersGuide/Download)

Bevestig je Python versie met ```python -V```. 

In het geval dat deze versie niet correct is, probeer ```python3 -V```. Je moet vanaf nu dan ook ```python3``` in plaats van ```python``` gebruiken.
### (Optioneel maar aanbevolen) Virtualenv
Bevestig je PIP versie met ```python -m pip -V``` in je favoriete terminal.

**Het is belangrijk dat je Python versie 3.7 gebruikt. Zo voorkomen we conflicten tussen developers.**

**(Windows & Ubuntu):**

```python -m pip install virtualenv```
### Gebruik
1. Maak je development environment met ```python -m virtualenv venv```

**(Windows):**

2. Activeer de script: ```./venv/Scripts/activate```

**(Ubuntu):**

2. Activeer de script: ```source venv/bin/activate```
3. Bevestig dat je in de virtual environment zit. Als het goed is zie je nu ```(venv)``` aan het begin van je command line prompt staan.
## Dependencies
Om alle dependencies te installeren voor dit project: ```python -m pip install -r requirements.txt```
### Eigen dependencies toevoegen
**Voer eerst de bovenstaande stap uit. Kijk ook goed dat je werkelijk in de virtual environment zit, anders worden alle Python packages op je computer in de requirements.txt gezet (laat staan dat het dan waarschijnlijk een foute Python versie zal gebruiken).**

In het geval dat je nieuwe packages installeert die nodig zijn om jouw code te laten werken voer de commando ```python -m pip freeze > requirements.txt``` uit terwijl je je in de virtual environment bevindt.
## Testen
De tests bevinden zich in de ```tests/``` directory. Om tests uit te voeren gebruik je de commando ```python -m pytest```.
## Werking
Ga naar de ```app/``` directory en voer de commando ```python -m main``` uit.
