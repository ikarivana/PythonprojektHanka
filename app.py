import os
import sys

# Přidání cesty k projektu, aby Python věděl, kde hledat
sys.path.append('/srv/app')

# Nastavení modulu s nastavením - upravte 'LoubNatural' podle názvu vaší složky se settings.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LoubNatural.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()