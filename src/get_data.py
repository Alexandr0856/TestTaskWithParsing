import asyncio

from country_data_manager import CountryDataManager


def main():
    cdm = CountryDataManager()
    cdm.update_countries()


if __name__ == "__main__":
    asyncio.run(main())
