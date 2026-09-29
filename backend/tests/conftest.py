import os

os.environ["DATABASE_URL"] = "sqlite:///./test_jobbot.db"

from app.database import Base, engine
from app import models  # noqa: F401

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
