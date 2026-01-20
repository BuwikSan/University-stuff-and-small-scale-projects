-- 2d FUNCTION: Pouze vypočítá hodnotu a vrátí ji (čistý výpočet)
CREATE OR REPLACE FUNCTION calculate_salary_value(emp_id BIGINT)
RETURNS DECIMAL AS $$
DECLARE
    final_salary DECIMAL;
BEGIN
    SELECT COALESCE(SUM(p.salary * r.percentage / 100), 0)
    INTO final_salary
    FROM emp_pos_relation r
    JOIN positions p ON r.fk_position = p.id_position
    WHERE r.fk_employee = emp_id;

    RETURN final_salary;
END;
$$ LANGUAGE plpgsql;




-- f) TRIGGER: Využije funkci výše a provede UPDATE !!!!!!!!!!!!!!!ukázat že funguje

-- Pomocná funkce triggeru (tzv. Trigger Function)
CREATE OR REPLACE FUNCTION trigger_recalculate_logic()
RETURNS TRIGGER AS $$
DECLARE
    target_emp_id BIGINT;
    new_salary DECIMAL;
BEGIN
    -- Určení ID zaměstnance podle operace
    IF (TG_OP = 'DELETE') THEN
        target_emp_id := OLD.fk_employee;
    ELSE
        target_emp_id := NEW.fk_employee;
    END IF;

    -- Použití funkce z bodu d) pro získání hodnoty
    new_salary := calculate_salary_value(target_emp_id);

    -- Zápis do DB
    UPDATE employees
    SET salary = new_salary
    WHERE id_employee = target_emp_id;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;



-- Samotný Trigger
CREATE TRIGGER emp_pos_relation_salary_update
AFTER INSERT OR UPDATE OR DELETE ON emp_pos_relation
FOR EACH ROW
EXECUTE FUNCTION trigger_recalculate_logic();






-- e) + g) PROCEDURE: Cursor, Handler, Transaction   !!!!!!!!!!!!!!!ukázat že funguje
CREATE OR REPLACE PROCEDURE adjust_salaries_by_cursor(min_threshold DECIMAL, increase_rate DECIMAL)
LANGUAGE plpgsql AS $$
DECLARE
    -- 1x CURSOR (bod e)
    pos_record RECORD;
    pos_cursor CURSOR FOR SELECT id_position, salary FROM positions;
    
    error_occurred BOOLEAN := FALSE;
BEGIN
    OPEN pos_cursor;
    
    LOOP
        FETCH pos_cursor INTO pos_record;
        EXIT WHEN NOT FOUND;

        -- Bod e) Ošetření chyb (HANDLER)
        -- V Postgresu musíme použít vnořený blok, abychom zachytili chybu
        -- a zároveň neodstřelili celou proceduru, pokud chceme logovat.
        BEGIN
            -- Simulace logiky: Pokud je plat podezřele záporný (chyba dat), vyvolej chybu
            IF pos_record.salary < 0 THEN
                RAISE EXCEPTION 'Záporný plat u pozice %', pos_record.id_position;
            END IF;

            -- Aktualizace
            IF pos_record.salary < min_threshold THEN
                UPDATE positions 
                SET salary = salary * (1 + increase_rate / 100)
                WHERE id_position = pos_record.id_position;
            END IF;

        EXCEPTION WHEN OTHERS THEN
            -- Zde zachytíme chybu konkrétního řádku, ale NESMÍME tu volat ROLLBACK celé transakce.
            RAISE NOTICE 'Chyba při zpracování ID %: %', pos_record.id_position, SQLERRM;
            error_occurred := TRUE; -- Poznačíme si, že se stala chyba
        END;

    END LOOP;
    
    CLOSE pos_cursor;

    -- Bod g) TRANSACTION (ROLLBACK / COMMIT)
    -- Rozhodnutí o transakci děláme v hlavním bloku (mimo EXCEPTION blok)
    IF error_occurred THEN
        RAISE NOTICE 'V průběhu došlo k chybám -> vracím změny (ROLLBACK).';
        ROLLBACK; -- Zde je to bezpečné
    ELSE
        RAISE NOTICE 'Vše OK -> potvrzuji změny (COMMIT).';
        COMMIT;
    END IF;
END;
$$;