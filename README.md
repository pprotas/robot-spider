# Code voor de robot spin van groep 9.
### Website
https://pprotas.github.io/robot-spider/

# Installatie
## Python 3.7
Installeer Python 3.7 voor jouw OS [hier](https://wiki.python.org/moin/BeginnersGuide/Download)
## (Optioneel) Virtualenv
Installeer python-virtualenv [hier](https://virtualenv.pypa.io/en/latest/)

(Ubuntu):
```sudo apt-get install python3-venv```
### Gebruik
1. Maak je development environment
  - ```virtualenv venv```
  - Als dit niet werkt probeer ```python3 -m venv venv```
2. Activeer de script: ```source venv/bin/activate```
## Dependencies
Om alle dependencies te installeren voor dit project:
 ```pip install -r requirements.txt``` of ```pip3 install -r requirements.txt```
# Testen
De tests bevinden zich in de ```tests/``` directory. Om tests uit te voeren gebruik je de commando ```python3 -m pytest```
