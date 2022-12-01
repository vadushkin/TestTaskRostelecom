import os

from pony.orm import Database, Required

UserAppealDB = Database()

DB_CONFIG = dict(
    provider=os.environ.get('DB_PROVIDER', 'postgres'),
    user=os.environ.get('POSTGRES_USER', 'postgres'),
    password=os.environ.get('POSTGRES_PASSWORD', 'password'),
    database=os.environ.get('POSTGRES_DB', 'user_appeal'),
    host=os.environ.get('DB_HOST', 'localhost'),
    port=os.environ.get('DB_PORT', '5433')
)

UserAppealDB.bind(**DB_CONFIG)


class UserAppeal(UserAppealDB.Entity):
    first_name = Required(str)
    last_name = Required(str)
    patronymic = Required(str)
    phone_number = Required(int, size=64, sql_type='BIGINT')
    message = Required(str)
