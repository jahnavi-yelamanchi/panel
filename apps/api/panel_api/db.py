from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from panel_api.settings import get_settings


def get_session_factory() -> sessionmaker:
    return sessionmaker(bind=create_engine(get_settings().database_url), expire_on_commit=False)

