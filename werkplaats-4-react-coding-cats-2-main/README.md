# Feedbacktool

Deze 360-feedbacktool is ontwikkeld door Coding Cats.

## Installatie

### Virtual Environment (VENV)

Om de applicatie te kunnen starten moet er eerst een VENV worden aangemaakt.

Bij gebruik op Windows kan het nodig zijn om eerst het uitvoeringsbeleid
van PowerShell te wijzigen.
1. Zoek PowerShell in de Windows zoekbalk.
2. Open PowerShell als administrator.
3. Type het volgende commando in PowerShell:
```
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Zorg dat je je in je terminal bevindt in de directory hieronder, of gebruik het commando
hieronder om er naartoe te navigeren:
```
cd .\werkplaats-4-react-coding-cats-2
```

Maak vervolgens een VENV aan met de volgende commando's:
```
pip install virtualenv
virtualenv .venv
.\.venv\scripts\activate.ps1
```

### Vereisten

Zorg voor het gemak dat je twee terminals open hebt staan in je IDE.

Installeer de benodigde packages terwijl je VENV is geactiveerd met het volgende commando in de ene terminal:
```
cd .\Backend\
pip install -r requirements.txt
```


Download de installer voor Node.JS via onderstaande link:

https://nodejs.org/en/download

Ga naar de volgende directory in je tweede terminal:
```
cd .\Frontend\rccforms\
```
Let op de hoofdletter!

Voer vervolgens het volgende commando uit:
```
npm install
```

## Tool runnen

Nu zou je in staat moeten zijn om de applicatie te runnen.
Geef hiervoor het volgende commando terwijl je in je eerste terminal zit:
```
python manage.py runserver
```

Voer het volgende commando uit terwijl je in je tweede terminal zit:
```
npm start
```

De tool zou nu vanzelf moeten starten.

# Inloggen

Log in met de volgende gegevens:
```
Username: mustafa
Password: 123
```
