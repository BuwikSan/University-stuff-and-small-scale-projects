-- === Table: sex ===
CREATE TABLE sex (
    id_sex SERIAL PRIMARY KEY,
    text_form TEXT NOT NULL
);

-- === Table: employees ===
CREATE TABLE employees (
    id_employee SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    fk_sex SERIAL NOT NULL,
    birth_date DATE NOT NULL,
    email TEXT NOT NULL UNIQUE,
    salary DECIMAL(12, 2),
    address TEXT NOT NULL,
    phone_number VARCHAR(20) NOT NULL CHECK (phone_number ~ '^\+?[0-9]{9,15}$'),
    date_of_hire DATE NOT NULL DEFAULT CURRENT_DATE,

    CONSTRAINT fk_employees_sex FOREIGN KEY (fk_sex) REFERENCES sex(id_sex)
);

-- === Table: building_complexes ===
CREATE TABLE building_complexes (
    id_complex SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT NOT NULL
);

-- === Table: focus ===
CREATE TABLE focus (
    id_focus SERIAL PRIMARY KEY,
    description TEXT NOT NULL
);

-- === Table: buildings ===
CREATE TABLE buildings (
    id_building SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    fk_focus SERIAL NOT NULL,
    fk_complex SERIAL NOT NULL,

    CONSTRAINT fk_buildings_focus FOREIGN KEY (fk_focus) REFERENCES focus(id_focus),
    CONSTRAINT fk_buildings_complex FOREIGN KEY (fk_complex) REFERENCES building_complexes(id_complex)
);

-- === Table: admin_emp ===
CREATE TABLE emp_building (
    fk_building SERIAL,
    fk_employee SERIAL,
    PRIMARY KEY (fk_building, fk_employee),

    CONSTRAINT fk_admin_emp_building FOREIGN KEY (fk_building) REFERENCES buildings(id_building),
    CONSTRAINT fk_admin_emp_employee FOREIGN KEY (fk_employee) REFERENCES employees(id_employee)
);

-- === Table: subject_species ===
CREATE TABLE subject_species (
    id_specie SERIAL PRIMARY KEY,
    full_name TEXT NOT NULL,
    adulthood_year INT NOT NULL,
    life_expectancy INT NOT NULL,
    fk_complex SERIAL NOT NULL,

    CONSTRAINT fk_subject_species_complex FOREIGN KEY (fk_complex) REFERENCES building_complexes(id_complex)
);

-- === Table: subjects ===
CREATE TABLE subjects (
    id_subject SERIAL PRIMARY KEY,
    fk_specie SERIAL NOT NULL,
    fk_sex SERIAL NOT NULL,
    name TEXT NOT NULL,
    date_of_creation DATE NOT NULL,

    CONSTRAINT fk_subjects_specie FOREIGN KEY (fk_specie) REFERENCES subject_species(id_specie),
    CONSTRAINT fk_subjects_sex FOREIGN KEY (fk_sex) REFERENCES sex(id_sex)
);

-- === Table: positions ===
CREATE TABLE positions (
    id_position SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    salary INT NOT NULL,
    description TEXT NOT NULL
);

-- === Table: emp_pos_relation ===
CREATE TABLE emp_pos_relation (
    fk_employee SERIAL NOT NULL,
    fk_position SERIAL NOT NULL,
    percentage SMALLINT NOT NULL,
    PRIMARY KEY (fk_employee, fk_position),

    CONSTRAINT fk_emp_pos_relation_employee FOREIGN KEY (fk_employee) REFERENCES employees(id_employee),
    CONSTRAINT fk_emp_pos_relation_position FOREIGN KEY (fk_position) REFERENCES positions(id_position),
    CONSTRAINT valid_percentage CHECK (percentage > 0 AND percentage <= 100)
);

-- === Table: functions ===
CREATE TABLE functions (
    id_func SERIAL PRIMARY KEY,
    description TEXT NOT NULL
);

-- === Table: rooms ===
CREATE TABLE rooms (
    id_room SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    fk_building SERIAL NOT NULL,
    fk_func SERIAL NOT NULL,
    
    CONSTRAINT fk_rooms_building FOREIGN KEY (fk_building) REFERENCES buildings(id_building),
    CONSTRAINT fk_rooms_function FOREIGN KEY (fk_func) REFERENCES functions(id_func)
);





-- === INDEXY PRO OPTIMALIZACI VÝKONU ===
-- Indexy pro vyhledávání zaměstnanců podle jména (častý dotaz)
CREATE INDEX idx_employees_name ON employees(name);

-- Index pro vyhledávání subjektů podle druhu a pohlaví (pro filtrování)
CREATE INDEX idx_subjects_species ON subjects(fk_specie);
CREATE INDEX idx_subjects_name ON subjects(name);

-- Index pro vyhledávání budov podle komplexu (hierarchické vyhledávání)
CREATE INDEX idx_buildings_complex ON buildings(fk_complex);

-- Index pro vyhledávání místností podle budovy (hierarchické vyhledávání) 
CREATE INDEX idx_rooms_building ON rooms(fk_building);
CREATE INDEX idx_rooms_function ON rooms(fk_func);

-- Indexy pro provázání zaměstnanců a pozic (často využíváno při výpočtu platů)
CREATE INDEX idx_emp_pos_employee ON emp_pos_relation(fk_employee);
CREATE INDEX idx_emp_pos_position ON emp_pos_relation(fk_position);

-- Složený index pro filtrování subjektů podle druhu a data vytvoření
CREATE INDEX idx_subjects_species_date ON subjects(fk_specie, date_of_creation);




CREATE UNIQUE INDEX idx_unique_employee_identity ON employees(name, phone_number);

CREATE INDEX idx_pos_description_fulltext ON positions USING gin(to_tsvector('en', description));

-- Komentáře k indexům:
-- 1. Indexy na jména (employees, subjects) zrychlují vyhledávání podle textu
-- 2. Indexy na cizí klíče (fk_*) zrychlují spojování tabulek (JOINy)
-- 3. Složený index umožňuje efektivní filtrování podle více kritérií najednou 


-- no problema


-- kdyby náhodou...
DROP TABLE emp_building;
DROP TABLE emp_pos_relation;
DROP TABLE employees;
DROP TABLE subjects;
DROP TABLE subject_species;
DROP TABLE sex;
DROP TABLE rooms;
DROP TABLE functions;
DROP TABLE buildings;
DROP TABLE focus;
DROP TABLE building_complexes;
DROP TABLE positions;