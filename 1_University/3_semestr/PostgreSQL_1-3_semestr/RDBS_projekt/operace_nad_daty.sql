-- 2a1 jeden SELECT vypočte průměrný počet záznamů na jednu tabulku v DB --------------------------------------------------------------------------------------------------------
CREATE VIEW prumer_zaznamu AS
-- Průměrný počet záznamů na tabulku
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
CREATE VIEW serazeni_podle_platu_rozdeleno_pohlavim AS
-- Analytická funkce (Pořadí zaměstnanců podle platu v rámci pohlaví)
SELECT name, salary, fk_sex,
       RANK() OVER (PARTITION BY fk_sex ORDER BY salary DESC) as salary_rank
FROM employees
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


CREATE VIEW multi_position_employees AS
WITH employee_counts AS (
    SELECT e.id_employee, e.name, COUNT(er.fk_position) AS position_count
    FROM employees e
    JOIN emp_pos_relation er ON e.id_employee = er.fk_employee
    GROUP BY e.id_employee, e.name
)
SELECT *
FROM employee_counts
WHERE position_count > 1;


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
JOIN positions p ON er.fk_position = p.id_position
WHERE er.percentage = 100
GROUP BY p.name, er.fk_position
HAVING COUNT(*) > 5
ORDER BY employee_count DESC;





CREATE VIEW employee_hierarchy AS
WITH RECURSIVE employee_tree AS (
    SELECT id_employee, name, fk_supervisor, 1 as level
    FROM employees
    WHERE id_employee = 1 -- CEO
    UNION ALL
    SELECT e.id_employee, e.name, e.fk_supervisor, name, et.level + 1
    FROM employees e
    JOIN employee_tree et ON e.fk_supervisor = et.id_employee
)
SELECT * FROM employee_tree;



-- procedure showcase --------------------------------------------------------------------------------
SELECT name, salary FROM positions WHERE salary < 110000;

CALL adjust_salaries_by_cursor(110000, 5);

SELECT name, salary FROM positions WHERE salary < 110000;