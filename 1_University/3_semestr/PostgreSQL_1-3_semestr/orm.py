from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, joinedload
from datetime import date

import csv

# 1. Připojení k databázi
engine = create_engine('postgresql://postgres:Coconut12@localhost:5432/postgres')
Base = declarative_base()

# 2. Mapování tabulek

# Tabulka druhů (podle tvého druhého screenshotu)
class Specie(Base):
    __tablename__ = 'subject_species'
    id_specie = Column(Integer, primary_key=True)
    full_name = Column(String)
    adulthood_year = Column(Integer)
    life_expectancy = Column(Integer)
    
    # Propojení na subjekty
    subjects = relationship("Subject", back_populates="specie")

# Tabulka subjektů (podle tvého prvního screenshotu)
class Subject(Base):
    __tablename__ = 'subjects'
    id_subject = Column(Integer, primary_key=True)
    name = Column(String)
    date_of_creation = Column(Date) # Assuming this is a Date object
    fk_specie = Column(Integer, ForeignKey('subject_species.id_specie'))
    fk_sex = Column(Integer)
    
    # Propojení na druh
    specie = relationship("Specie", back_populates="subjects")

    # V třídě Subject:
    def get_life_progress(self):
        from datetime import date
        age = (date.today() - self.date_of_creation).days / 365
        return (age / self.specie.life_expectancy) * 100
    

class Employee(Base):
    __tablename__ = 'employees'
    id_employee = Column(Integer, primary_key=True)
    name = Column(String)
    salary = Column(Numeric(12, 2))
    email = Column(String)

    # 1. Dynamický výpočet daně přímo v ORM 
    @property
    def estimated_tax(self):
        return float(self.salary) * 0.15

    # 2. Hezký výpis objektu (pro debugging)
    def __repr__(self):
        return f"<Employee(name='{self.name}', salary={self.salary})>"




# 3. Mapování tvého analytického VIEW
class BuildingStats(Base):
    __tablename__ = 'naklady_na_budovy'
    # Pokud se sloupec ve VIEW jmenuje třeba 'budova', musí to být tady taky tak!
    # 'primary_key=True' tu musí být jen pro SQLAlchemy, i když ve VIEW není.
    nazev = Column('budova', String, primary_key=True)  # Zkus 'budova' místo 'nazev_budovy'
    naklady = Column('naklady_budova', Numeric)
    podil = Column('procentualni_podil', Numeric)




# 4. Vytvoření relace
Session = sessionmaker(bind=engine)
session = Session()

def main():
    try:

        vsechny_subjekty = session.query(Subject).options(joinedload(Subject.specie)).all()

        for s in vsechny_subjekty:
            # Přístup k datům z druhé tabulky přes tečku (s.specie.full_name)
            print(f"{s.name:<15} | {s.specie.full_name:<30} | {s.specie.life_expectancy} let")

        # --- VÝPIS GENETICKÝCH PRODUKTŮ ---
        print(f"{'SUBJEKT':<15} | {'DRUH SAPIENS':<25} | {'DOŽITÍ'}")
        print("-" * 55)

        subjekty = session.query(Subject).options(joinedload(Subject.specie)).all()
        for s in subjekty:
            # Díky relationship() se Python sám podívá do tabulky species!
            print(f"{s.name:<15} | {s.specie.full_name:<25} | {s.specie.life_expectancy} let")

        # --- Analytika z VIEW ---
        print("\n=== TOP 5 NEJDRAŽŠÍCH BUDOV (Data z VIEW) ===")
        stats = session.query(BuildingStats).order_by(BuildingStats.naklady.desc()).limit(5).all()
        for s in stats:
            print(f"Budova: {s.nazev.ljust(20)} | Náklady: {str(s.naklady).rjust(10)} Kč | Podíl: {s.podil}%")

        # --- Výpis zaměstnanců ---
        print("\n=== ZAMĚSTNANCI S PLATEM NAD 160 000 ===") # Removed joinedload as Employee has no relationships defined
        vysledek = session.query(Employee).filter(Employee.salary > 160000).all()
        for emp in vysledek:
            # Malý grafický bonus pro efekt
            bar = "█" * int(emp.salary / 10000)
            print(f"{emp.name.ljust(20)} | {bar} {emp.salary} Kč")

        vysledek = session.query(Employee).all()

        print(f"{'JMÉNO':<25} | {'ČISTÝ PLAT':<12} | {'ODHAD DANĚ':<10}")
        print("-" * 55)

        total_payroll = 0
        for emp in vysledek:
            total_payroll += float(emp.salary)
            # Tady používáme tu naši novou property 'estimated_tax'
            print(f"{emp.name:<25} | {float(emp.salary):>10.2f} Kč | {emp.estimated_tax:>10.2f} Kč")

        # --- ORM Statistika---
        avg_salary = total_payroll / len(vysledek) if vysledek else 0

        print("-" * 55)
        print(f"CELKOVÉ MĚSÍČNÍ NÁKLADY (přes ORM): {total_payroll:,.2f} Kč")
        print(f"PRŮMĚRNÝ PLAT VE FIRMĚ:           {avg_salary:,.2f} Kč")

        # Export reportu do CSV
        with open('report_platu.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Jméno', 'Plat', 'Odhad daně'])
            for emp in vysledek:
                writer.writerow([emp.name, emp.salary, emp.estimated_tax])
        print("Report byl exportován do report_platu.csv")

    except Exception as e:
        print(f"Neočekávaná chyba aplikace: {e}")
    finally:
        session.close()
        print("\n=== Relace s databází ukončena ===")

if __name__ == "__main__":
    main()
