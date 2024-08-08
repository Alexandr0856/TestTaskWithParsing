import asyncio

from country_data_manager import CountryDataManager


async def main():
    cdm = CountryDataManager()
    await cdm.update_countries()


if __name__ == "__main__":
    asyncio.run(main())
