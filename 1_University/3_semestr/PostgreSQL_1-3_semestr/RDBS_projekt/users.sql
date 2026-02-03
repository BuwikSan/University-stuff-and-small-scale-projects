-- 1. Vytvoření role a uživatele (bod 40, 42)
CREATE ROLE auditor_role;
CREATE USER kvetuse_auditor WITH PASSWORD 'tajneHeslo123';

-- 2. Přidělení práv (GRANT - bod 46)
-- Auditor může jen číst tabulky employees a buildings
GRANT auditor_role TO kvetuse_auditor;
GRANT SELECT ON employees, buildings TO auditor_role;