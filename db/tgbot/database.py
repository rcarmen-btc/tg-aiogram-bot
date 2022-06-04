from gino import Gino
from gino.schema import GinoSchemaVisitor


from tgbot.config import load_config

db = Gino()
config = load_config()


async def create_db():
    am = await db.set_bind(config.db.postgresuri)
    db.gino: GinoSchemaVisitor
    # await db.gino.drop_all()
    await db.gino.create_all()

