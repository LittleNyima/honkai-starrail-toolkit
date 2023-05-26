from starrail.gacha.database import GachaDatabase
from starrail.gacha.migrate import migrate
from starrail.utils import loggings

logger = loggings.get_logger(__file__)


class DatabaseFactory:

    API_VERSION = 2

    @staticmethod
    def get_database(db_name: str) -> GachaDatabase:
        """
        Retrieves a new instance of a GachaDatabase with the specified name.

        Args:
            db_name: A string representing the name of the database to
                connect to.

        Returns:
            A new instance of a GachaDatabase.
        """
        db = GachaDatabase(db_name)
        if db.version == 0:
            db.version = DatabaseFactory.API_VERSION
        elif db.version < DatabaseFactory.API_VERSION:
            logger.warn(
                'Version of your database is lower than api version. '
                'Migration is required or potential data loss will '
                'occur.',
            )
            logger.warn('Migrating database, donot shut down...')
            migrate(db)
        elif db.version > DatabaseFactory.API_VERSION:
            logger.warn(
                'Version of the program is lower than database '
                'version. Please update your program or unexpected '
                'errors will occur.',
            )
        return db
