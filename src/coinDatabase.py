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
            result = func(self, cursor=cursor, **kwargs)
            sqliteConnector.commit()
            sqliteConnector.close()
            self.logger.info("Disconnected from database.")
            return result

        return connectionHandler

    @databaseHandler
    def createDatabase(self, cursor):
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Coins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kind VARCHAR(25),
            year INT,
            mint VARCHAR(25),
            description VARCHAR(255),
            condition VARCHAR(25),
            value INT
            ); """
        )
        self.logger.info("Database created.")

    @databaseHandler
    def add(self, cursor, coin):
        cursor.execute(
            f"""
            INSERT INTO Coins (
            id,
            kind,
            year, 
            mint,
            description,
            condition,
            value
            ) VALUES (
            NULL,
            "{coin.kind}",
            {coin.year},
            "{coin.mint}",
            "{coin.description}",
            "{coin.condition}",
            {coin.value}
            );"""
        )
        self.logger.info(f"Added {coin}.")

    @databaseHandler
    def remove(self, cursor, id):
        cursor.execute(f"DELETE FROM Coins WHERE id = {id};")
        self.logger.info(f"Deleted coin {id}")

    @databaseHandler
    def search(self, cursor, coin, order):
        kindParameters = '!= ""' if coin.kind == "" else f'= "{coin.kind}"'
        yearParameters = '!= ""' if coin.year == -1 else f'= "{coin.year}"'
        mintParameters = '!= ""' if coin.mint == "" else f'= "{coin.mint}"'
        conditionParameters = (
            '!= ""' if coin.condition == "" else f'= "{coin.condition}"'
        )
        descriptionParameters = (
            '!= ""' if coin.description == "" else f'= "{coin.description}"'
        )
        searchOrder = "" if order == "" else f"ORDER BY {order}"

        cursor.execute(
            f"""
            SELECT
            id,
            kind,
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
            ;"""
        )

        result = cursor.fetchall()
        self.logger.info(
            f"Executed search: kind {kindParameters} AND year {yearParameters} AND mint {mintParameters} AND description {descriptionParameters} AND condition {conditionParameters} {searchOrder}"
        )
        return result

    @databaseHandler
    def dump(self, cursor):
        cursor.execute(
            "SELECT id, kind, year, mint, description, condition, value FROM Coins ORDER BY id;"
        )
        result = cursor.fetchall()
        self.logger.info("Dumped database.")
        return result

    @databaseHandler
    def size(self, cursor, byKind=False, byMint=False):
        if byKind:
            cursor.execute("SELECT kind FROM Coins;")
            result = cursor.fetchall()
            kinds = {
                "Penny": 0,
                "Nickel": 0,
                "Dime": 0,
                "Quarter": 0,
                "Half Dollar": 0,
                "Dollar": 0,
                "Other": 0,
            }

            for kind in result:
                if kind[0] == "Penny":
                    kinds["Penny"] += 1
                elif kind[0] == "Nickel":
                    kinds["Nickel"] += 1
                elif kind[0] == "Dime":
                    kinds["Dime"] += 1
                elif kind[0] == "Quarter":
                    kinds["Quarter"] += 1
                elif kind[0] == "Half Dollar":
                    kinds["Half Dollar"] += 1
                else:
                    kinds["Other"] += 1

            self.logger.info(f"Dumped kind count: {kinds}")
            return kinds

        elif byMint:
            cursor.execute("SELECT mint FROM Coins;")
            result = cursor.fetchall()
            locations = {"P": 0, "D": 0, "S": 0, "W": 0, "Other": 0}

            for location in result:
                if location[0] == "P":
                    locations["P"] += 1
                elif location[0] == "D":
                    locations["D"] += 1
                elif location[0] == "S":
                    locations["S"] += 1
                elif location[0] == "W":
                    locations["W"] += 1
                else:
                    locations["Other"] += 1

            self.logger.info(f"Dumped location count: {locations}")
            return locations

        else:
            cursor.execute("SELECT id FROM Coins;")
            result = cursor.fetchall()
            self.logger.info(f"Dumped coin count: {len(result)}")
            return len(result)

    @databaseHandler
    def totalValue(self, cursor):
        cursor.execute("SELECT value FROM Coins;")
        result = cursor.fetchall()

        total = 0
        for value in result:
            total += value[0]

        self.logger.info(f"Dumped total value: {total}")
        return total

    @databaseHandler
    def highestValue(self, cursor):
        cursor.execute("SELECT value FROM Coins;")
        result = cursor.fetchall()

        highest = 0
        for value in result:
            if value[0] > highest:
                highest = value[0]

        self.logger.info(f"Dumped highest value: {highest}")
        return highest

    @databaseHandler
    def oldestYear(self, cursor):
        cursor.execute("SELECT year FROM Coins;")
        result = cursor.fetchall()

        if result == []:
            oldest = -1
        else:
            oldest = result[0][0]
            for year in result:
                if year[0] < oldest:
                    oldest = year[0]

        self.logger.info(f"Dumped oldest year: {oldest}")
        return oldest
