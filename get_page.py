import requests
from bs4 import BeautifulSoup


def get_page(url=None) -> list:
    if url is None:
        url = "https://en.wikipedia.org/w/index.php?title=List_of_countries_by_population_(United_Nations)"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        table = soup.find('table', {'class': 'wikitable'})

        country_region_pairs = []

        for row in table.find_all('tr')[2:]:
            columns = row.find_all('td')
            if len(columns) >= 3:
                country = columns[0].text.strip()
                region = columns[4].text.strip()
                country_region_pairs.append((country, region))

        return country_region_pairs
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []


if __name__ == "__main__":
    for country, region in get_page():
        print(f"Country: {country}, Region: {region}")
