
-- Funkce pro výpočet platu zaměstnance na základě jeho pozic a procentuálního podílu
CREATE OR REPLACE FUNCTION recalculate_salary(emp_id BIGINT)
RETURNS VOID AS $$
BEGIN
    UPDATE employees
    SET salary = COALESCE((
        SELECT SUM(p.salary * r.percentage / 100)
        FROM emp_pos_relation r
        JOIN positions p ON r.fk_position = p.id_position
        WHERE r.fk_employee = emp_id
    ), 0)
    WHERE id_employee = emp_id;
END;
$$ LANGUAGE plpgsql;

-- Trigger pro automatické přepočítání platu zaměstnance při změně jeho pozic
CREATE OR REPLACE FUNCTION trigger_recalculate_salary()
RETURNS TRIGGER AS $$
BEGIN
    -- Při INSERT nebo UPDATE použijeme NEW
    IF (TG_OP = 'INSERT' OR TG_OP = 'UPDATE') THEN
        PERFORM recalculate_salary(NEW.fk_employee); 
    
    -- Při DELETE použijeme OLD
    ELSIF (TG_OP = 'DELETE') THEN
        PERFORM recalculate_salary(OLD.fk_employee);
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;
 
-- Trigger pro tabulku emp_pos_relation
CREATE TRIGGER emp_pos_relation_salary_update
AFTER INSERT OR UPDATE OR DELETE ON emp_pos_relation
FOR EACH ROW
EXECUTE FUNCTION trigger_recalculate_salary();

-- no problema