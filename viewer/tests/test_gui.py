import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loubnatural.settings')
import django
django.setup()

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class TestGUI(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Nastavení cesty k ChromeDriver
        try:
            cls.chromedriver_path = os.environ.get('CHROMEDRIVER_PATH', 'chromedriver')
            print(f"Using ChromeDriver path: {cls.chromedriver_path}")
        except Exception as e:
            print(f"Error setting up ChromeDriver path: {e}")

    def setUp(self):
        """Nastavení před každým testem"""
        try:
            # Nastavení Chrome options
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--disable-extensions')
            options.add_argument('--proxy-server="direct://"')
            options.add_argument('--proxy-bypass-list=*')
            options.add_argument('--start-maximized')

            # Inicializace prohlížeče
            try:
                self.browser = webdriver.Chrome(options=options)
                print("Browser initialized successfully")
            except Exception as e:
                print(f"Failed to initialize browser: {e}")
                raise

            # Nastavení timeoutů
            self.browser.set_page_load_timeout(30)
            self.browser.implicitly_wait(10)

            # Vytvoření testovacího uživatele
            self.username = "testuser"
            self.password = "testpass123"
            try:
                self.user = User.objects.create_user(
                    username=self.username,
                    password=self.password,
                    is_staff=True  # Přidáme práva pro přístup
                )
                print("Test user created successfully")
            except Exception as e:
                print(f"Failed to create test user: {e}")
                raise

        except Exception as e:
            print(f"Setup failed: {e}")
            if hasattr(self, 'browser'):
                self.browser.quit()
            raise

    def test_service_categories(self):
        """Test kategorií služeb na stránce vyhledávání"""
        try:
            # Přihlášení
            print("Attempting to load login page...")
            self.browser.get(f'{self.live_server_url}/login/')
            print(f"Current URL (login): {self.browser.current_url}")

            # Vyplnění přihlašovacího formuláře
            wait = WebDriverWait(self.browser, 5)
            try:
                username_input = wait.until(
                    EC.presence_of_element_located((By.NAME, 'username'))
                )
                password_input = self.browser.find_element(By.NAME, 'password')

                username_input.send_keys(self.username)
                password_input.send_keys(self.password)
                print("Login form filled")

                # Submit formuláře
                password_input.submit()
                print("Login form submitted")

                # Počkáme na přihlášení
                time.sleep(1)
                print(f"Current URL after login: {self.browser.current_url}")

            except Exception as e:
                print(f"Login failed: {e}")
                print(f"Page source: {self.browser.page_source}")
                raise

            # Přejdeme na stránku vyhledávání
            print("Navigating to search page...")
            self.browser.get(f'{self.live_server_url}/search/')
            time.sleep(2)
            print(f"Current URL (search): {self.browser.current_url}")
            print(f"Page source: {self.browser.page_source}")

            # Kontrola nadpisů
            headers = ['Pedikúra', 'Pedikúra - popis', 'Řasy', 'Řasy - popis',
                       'Zdraví', 'Zdraví - popis', 'Kontakty']

            for header in headers:
                try:
                    element = wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH, f"//h2[contains(., '{header}')]")
                        )
                    )
                    self.assertTrue(
                        element.is_displayed(),
                        f"Nadpis '{header}' není viditelný"
                    )
                    print(f"Found header: {header}")
                except Exception as e:
                    print(f"Error finding header '{header}': {e}")
                    print("Available headers:", [
                        h.text for h in self.browser.find_elements(By.TAG_NAME, 'h2')
                    ])
                    raise

        except Exception as e:
            print(f"Test failed: {e}")
            print(f"Final URL: {self.browser.current_url}")
            print(f"Final page source: {self.browser.page_source}")
            raise

    def tearDown(self):
        """Úklid po každém testu"""
        print("Starting teardown...")
        if hasattr(self, 'browser'):
            try:
                self.browser.quit()
                print("Browser closed successfully")
            except Exception as e:
                print(f"Error closing browser: {e}")

        if hasattr(self, 'user'):
            try:
                self.user.delete()
                print("Test user deleted successfully")
            except Exception as e:
                print(f"Error deleting test user: {e}")
