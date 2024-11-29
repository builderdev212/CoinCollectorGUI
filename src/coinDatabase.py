import logging
import sqlite3

from coinTypes import Coin

class coinDatabase:
    """
    Class to interface with a SQLite database of coin entries.
    """
    def __init__(self, databaseName):
        self.name = databaseName
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Database Name: {self.name}")
        self.createDatabase()

    def databaseHandler(func):
        def connectionHandler(self, **kwargs):
            sqliteConnector = sqlite3.connect(f"{self.name}.db")
            cursor = sqliteConnector.cursor()
            self.logger.info("Connected to database.")
            func(self, cursor=cursor, **kwargs)
            cursor.close()
            self.logger.info("Disconnected from database.")
        return connectionHandler
    
    @databaseHandler
    def createDatabase(self, cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Coins (
            coin_id INT AUTO_INCREMENT PRIMARY KEY,
            kind VARCHAR(25),
            year INT,
            mint VARCHAR(25),
            description VARCHAR(255),
            condition VARCHAR(25),
            value INT,
            time TIMESTAMP
        ); """)
        self.logger.info("Database created.")

    @databaseHandler
    def add(self, cursor, coin):
        cursor.execute(f"""
            INSERT INTO Coins (
            type,
            year, 
            mint,
            description,
            condition,
            value
            ) VALUES (
            "{coin.kind}",
            {coin.year},
            "{coin.mint}",
            "{coin.description}",
            "{coin.condition}",
            {coin.value}
        );""")
        self.logger.info(f"Added {coin}.")

    @databaseHandler
    def remove(self, cursor, id):
        cursor.execute(f"DELETE FROM Coins WHERE coin_id = {id};")
        self.logger.info(f"Deleted coin {id}")

    @databaseHandler
    def search(self, cursor, coin, order):
        kindParameters = "!= \"\"" if coin.kind == "" else f"= \"{coin.kind}\""
        yearParameters = "!= \"\"" if coin.year == -1 else f"= \"{coin.year}\""
        mintParameters = "!= \"\"" if coin.mint == "" else f"= \"{coin.mint}\""
        conditionParameters = "!= \"\"" if coin.condition == "" else f"= \"{coin.condition}\""
        descriptionParameters = "!= \"\"" if coin.description == "" else f"= \"{coin.description}\""
        searchOrder = "" if order == "" else f"ORDER BY {order}"

        cursor.execute(f"""
            SELECT
            coin_id,
            type,
            year,
            mint,
            description,
            condition,
            value
            FROM Coins WHERE
            kind {kindParameters} AND
            year {yearParameters} AND
            mint {mintParameters} AND
            description {descriptionParameters} AND
            condition {conditionParameters}
            {searchOrder}
        ;""")

        results = cursor.fetchall()

        return results
