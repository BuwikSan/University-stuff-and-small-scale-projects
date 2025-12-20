ALTER TABLE employees ADD COLUMN fk_supervisor BIGINT;
UPDATE employees SET fk_supervisor = 1 WHERE id_employee BETWEEN 2 AND 10;
UPDATE employees SET fk_supervisor = 2 WHERE id_employee BETWEEN 11 AND 20;
ALTER TABLE employees
ADD CONSTRAINT fk_employees_supervisor 
FOREIGN KEY (fk_supervisor) REFERENCES employees(id_employee);