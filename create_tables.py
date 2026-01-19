from app.database import engine, Base
from app.models import User

print("Conectando no banco...")
Base.metadata.create_all(bind=engine)
print("Tabelas criadas.")
