from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase
import requests                     #import bibliotek wykorzystanych w kodzie

class CreateAccountWindow(Screen):  #Okno tworzenia konta
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    loc = ObjectProperty(None)

    def submit(self):               #zapisanie wartości podanych przy rejestracji
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0 and self.loc.text != "": #sprawdzanie czy wszystkie pola przy rejestracji są poprawne(w poprawnym formacie)
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.namee.text, self.loc.text)

                self.reset()

                self.manager.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):                #zmiana okna na okno logowania
        self.reset()
        self.manager.current = "login"

    def reset(self):                #czyszczenie pozycji tekswoych
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""

class LoginWindow(Screen):          #Okno logowania
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):             #funkcjonalność klawisza logowania
        if db.validate(self.email.text, self.password.text):
            MainWindow.current = self.email.text
            self.reset()
            self.manager.current = "main"
        else:
            invalidLogin()

    def createBtn(self):            #funkcjonalność klawisza zarejestruj się
        self.reset()
        self.manager.current = "create"

    def reset(self):                #czyszczenie pozycji tekstowych
        self.email.text = ""
        self.password.text = ""

class MainWindow(Screen):           #Okno główne aplikacji

    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ""
    nowalokalizacja = ObjectProperty(None)

    temp = NumericProperty()
    pressure = NumericProperty()
    humidity = NumericProperty()
    feels = NumericProperty()
    speed = NumericProperty()
    desc = StringProperty()

    def Weather(self):              #pobieranie informacji z API
        api_key = "587f5c5b0c2ab012c50c342fa0e33eba"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        city_name = self.created.text if self.created.text else "Wroclaw"
        complete_url = base_url + "appid=" + api_key + "&lang=pl&q=" + city_name
        response = requests.get(complete_url)
        x = response.json()

        y = x["main"]
        current_temperature = y["temp"]
        current_pressure = y["pressure"]
        current_humidiy = y["humidity"]
        current_feels_like = y["feels_like"]
        c = x["wind"]
        current_speed = c["speed"]
        z = x["weather"]
        current_weather_description = z[0]["description"]

        self.temp = round(current_temperature - 273, 2)
        self.feels = round(current_feels_like - 273, 2)
        self.pressure = current_pressure
        self.humidity = current_humidiy
        self.speed = current_speed
        self.desc = current_weather_description

    def logOut(self):               #funkjonalność przycisku wyloguj
        self.manager.current = "login"

    def on_enter(self, *args):      #funkcjonalność przycisku lupy, wywołanie funkcji pobierania infomacji o pogodzie i wypis ich na ekran
        password, name, created = db.get_user(self.current)
        self.created.text = created
        self.Weather()

class WindowManager(ScreenManager): #Okno odpowiadające za przechodzenie między poszczególnymi oknami: logowania, rejestracji i okna głównego aplikacji
    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)
        screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"), MainWindow(name="main")]
        for screen in screens:
            self.add_widget(screen)
        self.current = "login"

def invalidLogin():         #Błędy przy logowaniu
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()

def invalidForm():          #Błędy przy logowaniu
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()

kv = Builder.load_file("my.kv")
db = DataBase("users.txt")

class MyMainApp(App):       #Główna klasa programu

    def build(self):
        return WindowManager()

    def color(self):
        pass

if __name__ == "__main__":
    MyMainApp().run()
