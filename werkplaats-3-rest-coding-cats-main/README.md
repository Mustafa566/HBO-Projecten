# Aanwezigheidsapp

Deze Aanwezigheidsapplicatie is ontwikkeld door Coding Cats. 

## Installatie

### Virtual Environment (VENV)

Bij gebruik op Windows kan het nodig zijn om eerst het uitvoeringsbeleid van PowerShell te wijzigen,
voordat de VENV kan worden geactiveerd.
Doe hiervoor het volgende:

1. Zoek PowerShell in de Windows-zoekbalk.
2. Open PowerShell als Administrator.
3. Geef het volgende commando binnen PowerShell:
```
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Controleer daarna in je IDE of je je in de directory van de repository bevindt.
Dit zou gelijk moeten zijn aan de volgende directory:
```
.\werkplaats-3-rest-coding-cats
```

Activeer de VENV met het volgende commando in je terminal:
```
.\venv\Scripts\activate.ps1 
```

Navigeer vervolgens naar deze directory:
```
cd .\Aanwezigheids-tool\
```

### Vereisten

Installeer de benodigde packages, terwijl je VENV is geactiveerd en je je bevindt in de directory `Aanwezigheidstool`.
Geef het volgende commando in de terminal van je IDE:
```
pip install -r requirements.txt
```

## Tool runnen

Nu zou je in staat moeten zijn om de applicatie te runnen.
Geef hiervoor het volgende commando in de terminal van je IDE:
```
python manage.py runserver
```

Open de URL in je browser.


*Mocht je het runnen van de server willen stoppen, type dan `CTRL` + `C` in je terminal.*


## Inloggen

Met behulp van het item `Inloggen` op de navigatiebalk kom je bij het inlogscherm.

Hier kan worden ingelogd met drie accounttypen, die ieder hun eigen features te zien krijgen:
- Admin

De Admin ziet alle items op de navigatiebalk van zowel docenten als studenten.
Het testaccount voor Admin is:
```
Gebruikersnaam: admin
Wachtwoord: 123
```
Met dit account kan ook worden ingelogd op de ingebouwde Django-adminpagina.
De URL voor deze pagina is `http://127.0.0.1:8000/admin`.

- Docenten

Het testaccount voor docenten is:
```
Gebruikersnaam: docent@hr.nl
Wachtwoord: 123
```

- Studenten

Het testaccount voor studenten is:
```
Gebruikersnaam: 123
Wachtwoord: 123
```

## Feature-overzicht en permissies

In onderstaande tabel zijn alle navigatiebalkitems te vinden en ook welke accounttypes
deze items bevatten.

| Feature                 | Admin | Docent | Student |
|-------------------------|-------|--------|---------|
| Home                    | ✅     | ✅      | ✅       |
| Docent toevoegen        | ✅     | ❌      | ❌       |
| Alle bijeenkomsten      | ✅     | ✴️     | ✴       |
| Bijeenkomsten toevoegen | ✅     | ✅      | ❌       |
| Alle studenten          | ✅     | ✅      | ❌       |
| Student toevoegen       | ✅     | ✅      | ❌       |
| Aanwezigheid            | ✅     | ✅      | ✴       |
| Rooster (student)       | ❌     | ❌      | ✅       |
| Rooster (docent)        | ❌     | ✅      | ❌       |

| Legenda |                                |
|---------|--------------------------------|
| ✅       | Is toegankelijk                |
| ❌       | Is afgeschermd                 |
| ✴       | Ziet er per account anders uit |
