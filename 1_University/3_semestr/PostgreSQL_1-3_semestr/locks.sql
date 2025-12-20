BEGIN;
LOCK TABLE employees IN ACCESS EXCLUSIVE MODE;
-- V tuto chvíli druhý uživatel (třeba kvetuse_auditor) nemůže z tabulky ani číst.
-- Počkej pár sekund a pak uvolni:
COMMIT;