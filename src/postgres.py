import psycopg2

from typing import List

from env import PostgresEnv


class Postgres:
    def __init__(self, conn=None):
        self.conn = Postgres.create_connection() if conn is None else conn
        self.cursor = self.conn.cursor()

    @staticmethod
    def create_connection():
        return psycopg2.connect(PostgresEnv.get_conn_string())

    def commit(self):
        self.conn.commit()

    def insert_country(self, name: str, population: int, region: str):
        query = "INSERT INTO countries (name, population, region) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (name, population, region))
        self.conn.commit()

    def get_regions_stats(self) -> List[dict]:
        query = """
        SELECT
            region,
            SUM(population) AS total_population,
            MAX(name) AS largest_country,
            MAX(population) AS largest_population,
            MIN(name) AS smallest_country,
            MIN(population) AS smallest_population
        FROM (
            SELECT
                region,
                name,
                population,
                RANK() OVER (PARTITION BY region ORDER BY population DESC) AS rank_desc,
                RANK() OVER (PARTITION BY region ORDER BY population ASC) AS rank_asc
            FROM countries
        ) AS ranked_countries
        WHERE rank_desc = 1 OR rank_asc = 1
        GROUP BY region
        ORDER BY region;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
