# Webová aplikace LoubNaturál
  SDA PythonRemoteZ4073-Závěrečný projekt.

# Úvod
  Vítejte v repozitáři závěrečného projektu v kurzu programování v Pythnu od SDA.
  Tato webová aplikace je navržená pro kamarádku kosmetičku, aby měla o svých zakaznicích a jejich požadavcích přehled.

## Popis projektu
 -[ ] Pedikúra
   - Název ošetření + popis
     - Pedikúra basic : (do 60min.)
     - Pedikúra plus : (70 min.)
     - Pedikúra lady : (90 min.)
 -[ ] Řasy
   - Název ošetření
    - Volume 3D-4D 
    - Objemové 
    - Lash Lifting, Lash botox

-[ ] Zdraví
  - Koloidní stříbro
  - Diochi

-[ ] Kontakt
  - Adresa 
  - Telefon
  - Email
  - IČO
  - Mapa
  - 
## Databáze
-[ ] 1 Jméno příjmení
-[ ] 2 Datum narození
-[ ] 3 Telefon (int)
-[ ] 4 Email (1:n -> Email )
-[ ] 5 Datum registrace (Date)
-[ ] 6 Zakázka (n:n -> Jméno Příjmení) 
 
## User
- 

### Migrace
 Migrace mění chéma databáze a skládá se ze dvou kroků :

 ```bash
   python manage.py makemigrations
 ```
- vytvoří migrační skript popisující změny
 ```bash 
   python manage.py migrate
 ``` 
 - spustí migrační skripty ->  změnu schématu databáze

### Admin panel
 - vytvoření superuser : 
 ```bash
   python manage.py createsuperuser
 ````
 - do souboru ' viewer.admin.py ' zaregistrujeme vytvořený model:
   - from viewer.models import Pedikura
   - admin.site.register(Pedikura)

## Django
 ### Instalace
 ```bash
   pip install django, kontrola nainstalovaného balíčku 
   pip freeze > requirements
    django-admin startproject zaverecny_project .
   pip install dotenv
 ````
### DUMP/LOAD databaze
 ```bash
   pip django-dump-load-utf8==0.0.5
 ```
- Přidáme ' django-dump-load-utf8 ' do seznamu
nainstalovaných aplikací v ' settings.py - INSTALLED_APPS '
taky přidame do seznamu ' requirements.txt '

# Dump
```bash
  pip python manage.py dumpdatautf8 viewer --output .\zaloha\fixtures.json'
 ```

 # Struktura projektu
 - ' __init__.py ' - složka projektu (základní informace)
  - ' settings.py ' - nastavení projektu
    - zabespečení hesla v settings.py - vytvoření složky .env po  instalaci ' python-dotenv==1.0.1 ' 
    - > zkopírovaní
      hesla ze settings.py 'zápis bez mezer,závorek a uvozovek'  poté vložení do  ' load_dotenv() ' a nahrazení vygenerovaného klíče ze stránky https://djecrety.ir/
    - pokud je nastavení v ' settings.py ' > DEBUG = True  
    'není potřeba nastavovan adresu hosta v '  ALLOWED_HOSTS = [] 
  - ' urls.py ' - nastavení url cesty
  - ' manage.py ' - hlavní skript pro praci s projektem např.  
    - spuštění servru, testu migrací,  atd.

### Spuštění servru
```bash
  python manage.py runserver
```
 - lze spustit ručně pod nějakým číslem, stopnutí servru Ctrl+c

# Aplikace
## Vytvoření aplikace
 - v terminálu spuštění přes příkaz - 
 ```bash
  python manage.py startapp viewer 
 ```
> [ ! WARNING ]
> 
> Nesmíme zapomenout zaregistrovat aplikaci do souboru  ' setings.py ' 
 - složka s názvem projektu   

### Struktura aplikace
 - ' viewer ' - složka aplikace
 - ' migration ' - složka obsahující migrační skripty
 - ' __init__.py ' - slouží pouze k tomu aby složka byla package
 - ' admin ' - zde registrujeme  modely, ktere budeme chtít zobrazit v admin sekci
 - ' apps.py ' - nastavení aplikace
 - ' models.py ' - definice modelů (schéma databáze)
 - ' testy.py ' - testy
 - ' views.py ' - funkcionalita
