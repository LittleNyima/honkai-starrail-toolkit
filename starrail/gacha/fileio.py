import sqlite3

from starrail.gacha.type import GachaType


class GachaDatabase:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        for gacha_type in GachaType:
            self.create_table(gacha_type.name)

    def create_table(self, table_name):
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (
            uid TEXT,
            gacha_id TEXT,
            gacha_type TEXT,
            item_id TEXT,
            count TEXT,
            time TEXT,
            lang TEXT,
            item_type TEXT,
            rank_type TEXT,
            id TEXT PRIMARY KEY
        );''')
        self.conn.commit()

    def add_entry(self, table, entry):
        self.cursor.execute(
            f'INSERT INTO {table} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);',
            self.parse_entry(entry),
        )
        self.conn.commit()

    def get_entries(self, table):
        self.cursor.execute(f'SELECT * FROM {table};')
        entries = self.cursor.fetchall()
        return list(map(self.unparse_entry, entries))

    def close(self):
        self.conn.close()

    @staticmethod
    def parse_entry(entry):
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
        id_ = entry['id']
        return (
            uid, gacha_id, gacha_type, item_id, count, time_, name, lang,
            item_type, rank_type, id_,
        )

    @staticmethod
    def unparse_entry(
        uid, gacha_id, gacha_type, item_id, count, time_, name,
        lang, item_type, rank_type, id_,
    ):
        return dict(
            uid=uid, gacha_id=gacha_id, gacha_type=gacha_type,
            item_id=item_id, count=count, time=time_, name=name,
            lang=lang, item_type=item_type, rank_type=rank_type,
            id=id_,
        )


def export_as_sql():
    pass


def export_as_json():
    pass


def export_as_xlsx():
    pass


def export_as_csv():
    pass


def export_as_html():
    pass
