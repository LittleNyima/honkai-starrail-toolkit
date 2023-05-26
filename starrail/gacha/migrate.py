from starrail.gacha.database import GachaDatabase
from starrail.gacha.type import GachaType


def migrate_1(db: GachaDatabase):
    """By the time database api version is bumped to 2, the application
    supports gf only, so the default value of region and timezone should
    be prod_gf_cn and 8.
    """
    add_column = 'ALTER TABLE {} ADD COLUMN {} {};'
    set_value = 'UPDATE {table} SET {column} = "{value}";'
    for gacha_type in GachaType:
        table = gacha_type.name
        db.exec_update(add_column.format(table, 'region', 'TEXT'))
        db.exec_update(
            set_value.format(
                table=table,
                column='region',
                value='prod_gf_cn',
            ),
        )
        db.exec_update(add_column.format(table, 'region_time_zone', 'TEXT'))
        db.exec_update(
            set_value.format(
                table=table,
                column='region_time_zone',
                value='8',
            ),
        )
    db.version = 2


def migrate(db: GachaDatabase):
    if db.version == 1:
        migrate_1(db)
