CREATE VIEW position_distribution AS
SELECT fk_position, COUNT(*) AS employee_count
FROM emp_pos_relation
WHERE percentage = 100
GROUP BY fk_position
HAVING COUNT(*) > 5
ORDER BY employee_count DESC;


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