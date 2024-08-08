import requests

from bs4 import BeautifulSoup

from postgres import Postgres


class CountryDataManager:
    wiki_url = "https://en.wikipedia.org/w/index.php?title=List_of_countries_by_population_(United_Nations)"

    def __init__(self):
        self.pg = Postgres()

    def _parce_countries_from_wiki(self) -> list:
        response = requests.get(self.wiki_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            table = soup.find('table', {'class': 'wikitable'})

            if not table:
                print("Failed to find the table")
                return []

            country_region_pairs = []

            for row in table.find_all('tr')[2:]:
                columns = row.find_all('td')
                if len(columns) >= 3:
                    country = columns[0].text.strip()
                    population = int(columns[2].text.replace(',', ''))
                    region = columns[4].text.strip()
                    country_region_pairs.append((country, population, region))

            return country_region_pairs
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            return []

    def update_countries(self):
        countries = self._parce_countries_from_wiki()
        for country, population, region in countries:
            self.pg.insert_country(country, population, region)
        self.pg.commit()
        print(f"Successfully updated {len(countries)} countries")

    def get_regions_stats(self) -> list:
        return self.pg.get_regions_stats()

    def print_regions_stats(self):
        stats = self.get_regions_stats()

        for region, population, biggest_country, biggest_population, smallest_county, smallest_population in stats:
            print(
                f"{region} ({population:,}):\n "
                f"\t- Biggest Country: {biggest_country} ({biggest_population:,}) \n"
                f"\t- Smallest Country: {smallest_county} ({smallest_population:,})\n"
                )
