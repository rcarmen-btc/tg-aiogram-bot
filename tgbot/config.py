from dataclasses import dataclass

from environs import Env


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str
    postgresuri: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool
    locale: str


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
            locale=env.str("LOCALE")
        ),
        db=DbConfig(
            host=env.str('POSTGRES_HOST'),
            password=env.str('POSTGRES_PASSWORD'),
            user=env.str('POSTGRES_USER'),
            database=env.str('DB_NAME'),
            postgresuri=f"postgresql://{env.str('POSTGRES_USER')}:{env.str('POSTGRES_PASSWORD')}@{env.str('POSTGRES_HOST')}:5432/{env.str('POSTGRES_DB')}"
        ),
        misc=Miscellaneous()
    )
