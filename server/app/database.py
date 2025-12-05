from sqlmodel import SQLModel, create_engine
import os

abs_path = os.path.dirname(os.path.abspath(__file__))
if os.getenv("EXECUTION_EN_DOCKER") == "true":
    sqlite_file_name = "/app/data/supervision.db"
else:
    sqlite_file_name = f"{abs_path}/../data/supervision.db"

sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=False)

def configure_db():
    SQLModel.metadata.create_all(engine)