import httpx

from bs4 import BeautifulSoup

from env import SourceEnv
from sources import SourcesUrl
from postgres import Postgres


class CountryDataManager:
    def __init__(self):
        self.pg = Postgres()
        self.source = SourceEnv.name

    @staticmethod
    async def _parce_countries_from_wiki() -> list:
        async with httpx.AsyncClient() as client:
            response = await client.get(SourcesUrl.wiki_url)

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

        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []

    @staticmethod
    async def _parce_countries_from_statisticstimes() -> list:
        async with httpx.AsyncClient() as client:
            response = await client.get(SourcesUrl.statisticstimes_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            table = soup.find('table', {'id': 'table_id'})

            country_data = []

            for row in table.find_all('tr')[1:]:  # Skip the header row
                columns = row.find_all('td')
                if len(columns) >= 4:
                    country = columns[0].text.strip()
                    population = int(columns[3].text.replace(',', ''))
                    region = columns[8].text.strip()
                    country_data.append((country, population, region))

            return country_data

        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []

    async def update_countries(self):
        if self.source == "statisticstimes":
            countries = await self._parce_countries_from_statisticstimes()
        elif self.source == "wiki":
            countries = await self._parce_countries_from_wiki()
        else:
            print(
                "Unknown source, please check the env file. "
                "SOURCE_NAME should be either 'statisticstimes' or 'wiki'"
            )
            return

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


if __name__ == "__main__":
    import asyncio

    cdm = CountryDataManager()
    res = asyncio.run(cdm._parce_countries_from_statisticstimes())
    print(res)
