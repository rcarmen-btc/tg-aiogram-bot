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

    def get_str_latest_prices(self, **kwargs):
        args = ''
        for k, v in kwargs.items():
            if v is not None:
                args += f'{k}={v}&'
        return args

    def prices_for_dates(self, origin, destination, departure_at, return_at, unique, sorting, direct, currency, limit, page, one_way):
        args = self.get_str_latest_prices(origin=origin, destination=destination, departure_at=departure_at, return_at=return_at, one_way=one_way, sorting=sorting, unique=unique, direct=direct, currency=currency, limit=limit, page=page)
        response = requests.get("https://api.travelpayouts.com/aviasales/v3/prices_for_dates?"+args+f'token=74e374ffbb7e61ea2155743ac6ca4e64')
        return response.json()
        # return args

