import requests
from config import Config

class APINinjaClient:
    @staticmethod
    def get_address_validation(address):
        response = requests.get(
            "https://api.api-ninjas.com/v1/geocoding",
            headers={'X-Api-Key': Config.API_NINJA_KEY},
            params={'address': address}
        )
        return response.json()

    @staticmethod
    def get_demographics(zip_code):
        response = requests.get(
            "https://api.api-ninjas.com/v1/demographics",
            headers={'X-Api-Key': Config.API_NINJA_KEY},
            params={'zip_code': zip_code}
        )
        return response.json()
    
    @staticmethod
    def get_naics_classification(description):
        response = requests.get(
            "https://api.api-ninjas.com/v1/naics",
            headers={'X-Api-Key': Config.API_NINJA_KEY},
            params={'query': description}
        )
        return response.json()