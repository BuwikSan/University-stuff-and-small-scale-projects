-- 2a1 jeden SELECT vypočte průměrný počet záznamů na jednu tabulku v DB --------------------------------------------------------------------------------------------------------
CREATE VIEW prumer_zaznamu AS
-- Průměrný počet záznamů na tabulku (velmi zjednodušeně pro účely zadání)
SELECT (
    (SELECT COUNT(*) FROM sex) +
    (SELECT COUNT(*) FROM employees) +
    (SELECT COUNT(*) FROM building_complexes) +
    (SELECT COUNT(*) FROM focus) +
    (SELECT COUNT(*) FROM buildings) +
    (SELECT COUNT(*) FROM emp_building) +
    (SELECT COUNT(*) FROM subject_species) +
    (SELECT COUNT(*) FROM subjects) +
    (SELECT COUNT(*) FROM positions) +
    (SELECT COUNT(*) FROM emp_pos_relation) + 
    (SELECT COUNT(*) FROM functions) +
    (SELECT COUNT(*) FROM rooms)
) / 12.0 AS avg_records_per_table;



-- 2a2 jeden SELECT bude obsahovat vnořený SELECT (select v selectu)-------------------------------------------------------------------------------------------------------
CREATE OR REPLACE VIEW nadprumerne_platy AS
SELECT e.name AS employee_name, p.name AS position, e.salary AS salary
FROM employees e
LEFT JOIN emp_pos_relation er ON e.id_employee = er.fk_employee
LEFT JOIN positions p ON p.id_position = er.fk_position
WHERE e.salary > (SELECT AVG(salary) FROM employees);



-- 2a3 jeden SELECT bude obsahovat nějakou analytickou funkci ---------------------------------------------------------------------------------------------------
CREATE OR REPLACE VIEW naklady_na_budovy AS
SELECT
    b.name AS budova,
    SUM(e.salary) AS naklady_budova,
    -- Analytická funkce vypočítaná po seskupení (agregaci)
    SUM(SUM(e.salary)) OVER() AS celkove_naklady_firmy,
    -- Výpočet procenta
    ROUND((SUM(e.salary) / SUM(SUM(e.salary)) OVER()) * 100, 2) AS procentualni_podil
FROM employees e
JOIN emp_building ae ON e.id_employee = ae.fk_employee
JOIN buildings b ON ae.fk_building = b.id_building
GROUP BY b.id_building, b.name;


-- 2a4 jeden SELECT bude řešit rekurzi ------------------------------------------------------------------------------------------

CREATE VIEW employee_hierarchy AS
WITH RECURSIVE employee_tree AS (
    -- Anchor: Add a placeholder for supervisor_name because the CEO has no supervisor
    SELECT 
        id_employee, 
        name, 
        fk_supervisor, 
        'No Supervisor'::text as supervisor_name, -- Placeholder to match column count
        1 as level
    FROM employees
    WHERE id_employee = 1
    
    UNION ALL
    
    -- Recursive: Select et.name (the supervisor's name from the previous level)
    SELECT 
        e.id_employee, 
        e.name, 
        e.fk_supervisor, 
        et.name, -- This resolves the ambiguity (et.name is the supervisor)
        et.level + 1
    FROM employees e
    JOIN employee_tree et ON e.fk_supervisor = et.id_employee
)
SELECT * FROM employee_tree;


-- Analytická funkce (Pořadí zaměstnanců podle platu v rámci pohlaví)
CREATE VIEW serazeni_podle_platu_rozdeleno_pohlavim AS
SELECT name, salary, sex.text_form as sex,
       RANK() OVER (PARTITION BY fk_sex ORDER BY salary DESC) as salary_rank
FROM employees
LEFT JOIN sex ON employees.fk_sex = sex.id_sex
WHERE salary IS NOT NULL;


-- 2b -------------------------------------------------------------------------------------------
CREATE VIEW employees_and_positions AS
SELECT e.name AS employee_name, p.name AS position_name, e.salary
FROM employees e
INNER JOIN emp_pos_relation er ON e.id_employee = er.fk_employee
INNER JOIN positions p ON er.fk_position = p.id_position
WHERE e.salary IS NOT NULL
ORDER BY e.salary DESC;


CREATE VIEW employees_without_position AS
SELECT e.name AS employee_name, p.name AS position_name, er.percentage
FROM employees e
LEFT JOIN emp_pos_relation er ON e.id_employee = er.fk_employee
LEFT JOIN positions p ON er.fk_position = p.id_position
WHERE er.percentage IS NULL;


CREATE OR REPLACE VIEW multi_position_employees AS
SELECT
    e.id_employee,
    e.name,
    COUNT(er.fk_position) AS position_count,
    STRING_AGG(p.name, ', ') AS all_positions -- Spojí názvy: "Manager, Vedoucí, Uklízeč"
FROM employees e
JOIN emp_pos_relation er ON e.id_employee = er.fk_employee
JOIN positions p ON er.fk_position = p.id_position
GROUP BY e.id_employee, e.name
HAVING COUNT(er.fk_position) > 1; -- Filtrujeme rovnou zde pomocí HAVING


CREATE VIEW gender_salary_comparison AS
SELECT s.text_form AS gender, AVG(e.salary) AS avg_salary
FROM employees e
INNER JOIN sex s ON e.fk_sex = s.id_sex
WHERE e.salary IS NOT NULL
GROUP BY s.text_form
ORDER BY avg_salary DESC;


CREATE VIEW unfilled_positions AS
SELECT e.name AS employee_name, p.name AS position_name, er.percentage
FROM employees e
FULL OUTER JOIN emp_pos_relation er ON e.id_employee = er.fk_employee
FULL OUTER JOIN positions p ON er.fk_position = p.id_position
WHERE e.name IS NULL OR p.name IS NULL;


CREATE OR REPLACE VIEW position_distribution AS
SELECT
    p.name AS position_name,
    COUNT(*) AS employee_count
FROM emp_pos_relation er
JOIN positions p ON er.fk_position = p.id_position -- Propojení tabulek přes cizí klíč
WHERE er.percentage = 100
GROUP BY p.name, er.fk_position -- Seskupení podle názvu (a ID pro jistotu) [cite: 21]
HAVING COUNT(*) > 5
ORDER BY employee_count DESC;


-- test indexování -----

DROP INDEX idx_unique_employee_identity;
DROP INDEX idx_employees_name;

EXPLAIN ANALYZE
SELECT * FROM employees
WHERE name = 'Jan Novák';

CREATE INDEX idx_employees_name ON employees(name);
CREATE UNIQUE INDEX idx_unique_employee_identity ON employees(name, phone_number);

EXPLAIN ANALYZE
SELECT * FROM employees
WHERE name = 'Jan Novák';


DROP INDEX idx_subjects_species;
DROP INDEX idx_subjects_species_date;

EXPLAIN ANALYZE
SELECT * FROM subjects 
WHERE fk_specie = 1 
  AND fk_sex = 2;

EXPLAIN ANALYZE
SELECT * FROM subjects 
WHERE fk_specie = 5 
  AND date_of_creation > '2023-01-01';

CREATE INDEX idx_subjects_species ON subjects(fk_specie);
CREATE INDEX idx_subjects_species_date ON subjects(fk_specie, date_of_creation);

EXPLAIN ANALYZE
SELECT * FROM subjects 
WHERE fk_specie = 1 
  AND fk_sex = 2;

EXPLAIN ANALYZE
SELECT * FROM subjects 
WHERE fk_specie = 5 
  AND date_of_creation > '2023-01-01';
  

DROP INDEX idx_unique_employee_identity

EXPLAIN ANALYZE
SELECT id_employee 
FROM employees 
WHERE name = 'Petr Svoboda' 
  AND phone_number = '+420777666555';

CREATE UNIQUE INDEX idx_unique_employee_identity ON employees(name, phone_number);

EXPLAIN ANALYZE
SELECT id_employee 
FROM employees 
WHERE name = 'Petr Svoboda' 
  AND phone_number = '+420777666555';




-- procedure showcase --------------------------------------------------------------------------------
CREATE VIEW platy_pred_valorizaci
SELECT name, salary FROM positions WHERE salary < 110000;

CALL adjust_salaries_by_cursor(110000, 5);

CREATE VIEW platy_po_valorizaci
SELECT name, salary FROM positions WHERE salary < 110000;

CALL adjust_salaries_by_cursor(110000, -4.7619);

CREATE VIEW platy_po_reverzní_valorizaci
SELECT name, salary FROM positions WHERE salary < 110000;


