import sqlite3
from typing import Dict, List, Tuple

from starrail.gacha.type import GachaType
from starrail.utils import loggings

logger = loggings.get_logger(__file__)


class GachaDatabase:
    def __init__(self, db_name: str) -> None:
        """
        A class to handle SQLite database operations related to gacha.

        Args:
            db_name: A string representing the name of the SQLite database
                to use.
        """

        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        for gacha_type in GachaType:
            self.create_table(gacha_type.name)
        self.columns = ', '.join([
            'uid', 'gacha_id', 'gacha_type', 'item_id', 'count', 'time',
            'name', 'lang', 'item_type', 'rank_type', 'region',
            'region_time_zone', 'id',
        ])

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __exec_update(self, sql, parameters=()):
        self.cursor.execute(sql, parameters)
        self.conn.commit()

    def exec_update(self, sql, parameters=()):
        logger.info(f'Call update from external package: {sql}; {parameters}')
        self.__exec_update(sql, parameters)

    def create_table(self, table_name: str) -> None:
        """
        Creates a new table in the database with the specified name.

        Args:
            table_name: A string representing the name of the table to create.
        """

        self.__exec_update(f'''CREATE TABLE IF NOT EXISTS {table_name} (
            uid TEXT,
            gacha_id TEXT,
            gacha_type TEXT,
            item_id TEXT,
            count TEXT,
            time TEXT,
            name TEXT,
            lang TEXT,
            item_type TEXT,
            rank_type TEXT,
            region TEXT,
            region_time_zone TEXT,
            id TEXT PRIMARY KEY
        );''')

    def add_entry(self, table: str, entry: Dict[str, str]) -> None:
        """
        Adds a new entry to the specified table in the database.

        Args:
            table: A string representing the name of the table to add the
                entry to.
            entry: A dictionary representing the entry to add to the table.
        """

        self.__exec_update(
            f'''INSERT INTO {table} ({self.columns})
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''',
            self.parse_entry(entry),
        )

    def get_entries(self, table: str) -> List[Dict[str, str]]:
        """
        Retrieves all entries from the specified table in the database.

        Args:
            table: A string representing the name of the table to retrieve
                entries from.

        Returns:
            A list of dictionaries representing the entries retrieved from the
                table.
        """

        self.cursor.execute(f'SELECT {self.columns} FROM {table};')
        entries = self.cursor.fetchall()
        return [self.unparse_entry(*entry) for entry in entries]

    def close(self) -> None:
        """
        Closes the connection to the database.
        """

        self.cursor.close()
        self.conn.close()

    @property
    def version(self) -> int:
        """
        The version of the database, which should be identical to API_VERSION.

        Returns:
            An integer representing the version of the database.
        """

        self.cursor.execute('PRAGMA user_version;')
        entries = self.cursor.fetchone()[0]
        return entries

    @version.setter
    def version(self, value: int) -> None:
        """
        Sets the version of the database.

        Args:
            value: An integer representing the new version of the database.
        """

        self.__exec_update(f'PRAGMA user_version={value};')

    @staticmethod
    def parse_entry(entry: Dict[str, str]) -> Tuple:
        """
        Parses an entry dictionary into a tuple for insertion into the
        database.

        Args:
            entry: A dictionary representing the entry to parse.

        Returns:
            A tuple representing the parsed entry.
        """

        uid = entry['uid']
        gacha_id = entry['gacha_id']
        gacha_type = entry['gacha_type']
        item_id = entry['item_id']
        count = entry['count']
        time_ = entry['time']
        name = entry['name']
        lang = entry['lang']
        item_type = entry['item_type']
        rank_type = entry['rank_type']
        region = entry['region']
        region_time_zone = entry['region_time_zone']
        id_ = entry['id']
        return (
            uid, gacha_id, gacha_type, item_id, count, time_, name, lang,
            item_type, rank_type, region, region_time_zone, id_,
        )

    @staticmethod
    def unparse_entry(
        uid: str, gacha_id: str, gacha_type: str, item_id: str, count: str,
        time_: str, name: str, lang: str, item_type: str, rank_type: str,
        region: str, region_time_zone: str, id_: str,
    ) -> Dict[str, str]:
        """
        Unparses a tuple from the database into an entry dictionary.

        Args:
            uid: A string representing the UID of the entry.
            gacha_id: A string representing the Gacha ID of the entry.
            gacha_type: A string representing the Gacha type of the entry.
            item_id: A string representing the Item ID of the entry.
            count: A string representing the count of the entry.
            time_: A string representing the timestamp of the entry.
            name: A string representing the name of the entry.
            lang: A string representing the language of the entry.
            item_type: A string representing the Item type of the entry.
            rank_type: A string representing the Rank type of the entry.
            id_: A string representing the ID of the entry.

        Returns:
            A dictionary representing the unparsed entry.
        """

        return dict(
            uid=uid, gacha_id=gacha_id, gacha_type=gacha_type,
            item_id=item_id, count=count, time=time_, name=name,
            lang=lang, item_type=item_type, rank_type=rank_type,
            region=region, region_time_zone=region_time_zone, id=id_,
        )
