import requests
from django.core.management.base import BaseCommand
from base.models import CountryModel


class Command(BaseCommand):
    help = "Fetches country data from RestCountries API and saves it to the database"

    def handle(self, *args, **kwargs):
        url = "https://restcountries.com/v3.1/all"
        response = requests.get(url)

        if response.status_code != 200:
            self.stderr.write("Failed to fetch data from API")
            return

        data = response.json()
        CountryModel.objects.all().delete()

        for country in data:
            name = country.get("name", {}).get("common")
            cca2 = country.get("cca2")
            capital_list = country.get("capital", [])
            capital = capital_list[0] if capital_list else None
            population = country.get("population", 0)
            timezone_list = country.get("timezones", [])
            timezone = timezone_list[0] if timezone_list else None
            flag = country.get("flag")

            CountryModel.objects.create(
                name=name,
                cca2=cca2,
                capital=capital,
                population=population,
                timezone=timezone,
                flag=flag,
            )

        self.stdout.write(self.style.SUCCESS("Country data fetched and stored."))
