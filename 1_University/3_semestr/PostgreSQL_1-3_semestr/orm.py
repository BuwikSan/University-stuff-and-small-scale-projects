from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Připojení k databázi (nahraď svými údaji)
# formát: 'postgresql://uzivatel:heslo@localhost:5432/nazev_databaze'
engine = create_engine('postgresql://postgres:Coconut12@localhost:5432/postgres')
Base = declarative_base()

# 2. Definice objektu (Mapování tabulky employees)
class Employee(Base):
    __tablename__ = 'employees'
    
    id_employee = Column(Integer, primary_key=True)
    name = Column(String)
    salary = Column(Numeric(12, 2))
    email = Column(String)

# 3. Vytvoření relace (Session)
Session = sessionmaker(bind=engine)
session = Session()

# 4. Samotný úkol přes ORM (např. výpis zaměstnanců s platem nad 40k)
print("--- Výpis zaměstnanců přes ORM ---")
vysledek = session.query(Employee).filter(Employee.salary > 40000).all()

for emp in vysledek:
    print(f"Jméno: {emp.name} | Email: {emp.email} | Plat: {emp.salary}")

# Ukázka INSERTU přes ORM 
# novy_clovek = Employee(name="Jan Novák", email="novak@seznam.cz", salary=45000)
# session.add(novy_clovek)
# session.commit()