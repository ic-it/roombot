import sqlalchemy

users = [
    sqlalchemy.Column("id",             sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("telegram_id",    sqlalchemy.Integer),
    sqlalchemy.Column("firstname",      sqlalchemy.String()),
    sqlalchemy.Column("lastname",       sqlalchemy.String()),
    sqlalchemy.Column("permissions",    sqlalchemy.String()),
    sqlalchemy.Column("room",           sqlalchemy.String()),
]
