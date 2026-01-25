ALTER TABLE employees ADD COLUMN fk_supervisor BIGINT;
UPDATE employees SET fk_supervisor = 1 WHERE id_employee BETWEEN 2 AND 10;
UPDATE employees SET fk_supervisor = 2 WHERE id_employee BETWEEN 11 AND 20;
ALTER TABLE employees
ADD CONSTRAINT fk_employees_supervisor 
FOREIGN KEY (fk_supervisor) REFERENCES employees(id_employee);

INSERT INTO emp_building (fk_employee, fk_building)
WITH
  e_rand AS (
    SELECT id_employee, row_number() OVER (ORDER BY random()) as rn
    FROM employees
  ),
  b_rand AS (
    SELECT id_building, row_number() OVER (ORDER BY random()) as rn
    FROM buildings
  ),
  b_count AS (
    SELECT count(*) as total FROM buildings
  )
SELECT
    e_rand.id_employee,
    b_rand.id_building
FROM e_rand
JOIN b_rand ON b_rand.rn = ((e_rand.rn - 1) % (SELECT total FROM b_count) + 1);