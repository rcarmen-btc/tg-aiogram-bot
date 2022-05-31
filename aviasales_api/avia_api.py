import requests


class AviasalesAPI:

    def __init__(self, token, locale):
        self.token = token
        self.locale = locale
        self.cities = None

    def get_cities(self):
        response = requests.get(f"https://api.travelpayouts.com/aviasales_resources/v3/cities.json?locale={self.locale}")
        return response.json()

    def get_countries(self):
        response = requests.get(f"https://api.travelpayouts.com/aviasales_resources/v3/countries.json?locale={self.locale}")
        return response.json()


