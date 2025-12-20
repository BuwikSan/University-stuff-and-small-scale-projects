INSERT INTO sex (id_sex, text_form) VALUES
(1, 'Muž'),
(2, 'Žena'),
(3, 'Neurčeno');

INSERT INTO positions (id_position, name, description, salary) VALUES
-- Management a administrativa
(1, 'Ředitel komplexu', 'Celkový management a strategické vedení komplexu', 250000),
(2, 'Zástupce ředitele', 'Zástupce ředitele komplexu', 180000),
(3, 'Administrativní pracovník', 'Administrativa a podpora vedení', 90000),
(4, 'Recepční', 'Recepce a komunikace s návštěvníky', 70000),
(5, 'Asistent vedení', 'Podpora managementu a administrativy', 80000),
(6, 'Projektový manažer', 'Řízení projektů v rámci komplexu', 140000),
(7, 'Manažer kvality', 'Zajištění kvality procesů a služeb', 130000),

-- Výzkum, laboratoře a vývoj
(8, 'Vedoucí laboratoře', 'Vedení výzkumné laboratoře', 170000),
(9, 'Výzkumný pracovník', 'Výzkum a vývoj v laboratoři', 140000),
(10, 'Laboratorní technik', 'Technická podpora laboratoře', 110000),
(11, 'Genetik', 'Genetický výzkum a modifikace', 160000),
(12, 'Fyziolog', 'Fyziologický výzkum', 150000),
(13, 'Behaviorální specialista', 'Výzkum chování subjektů', 145000),
(14, 'Hybridizační expert', 'Vývoj a testování hybridních druhů', 155000),
(15, 'Etik', 'Etické posuzování výzkumu', 120000),
(16, 'Biotechnolog', 'Aplikace biotechnologií ve výzkumu', 135000),
(17, 'Molekulární biolog', 'Molekulárně biologický výzkum', 145000),
(18, 'Zoolog', 'Výzkum zvířecích druhů a jejich chování', 130000),
(19, 'Ekolog', 'Ekologické studie a environmentální dohled', 125000),
(20, 'Vývojář simulačních prostředí', 'Vývoj a správa simulačních zařízení', 120000),

-- Zdravotnictví a péče
(21, 'Vedoucí zdravotního střediska', 'Vedení zdravotního střediska', 160000),
(22, 'Lékař', 'Zdravotní péče o zaměstnance a subjekty', 150000),
(23, 'Zdravotní sestra', 'Ošetřovatelská péče', 110000),
(24, 'Rehabilitační specialista', 'Rehabilitace subjektů', 120000),
(25, 'Poradce pro subjekty', 'Psychologická a sociální podpora', 115000),
(26, 'Veterinář', 'Veterinární péče o zvířelidi', 130000),
(27, 'Farmaceut', 'Příprava a výdej léčiv', 110000),
(28, 'Fyzioterapeut', 'Fyzioterapie a pohybová péče', 115000),
(29, 'Zdravotnický laborant', 'Laboratorní vyšetření a analýzy', 105000),
(30, 'Psycholog', 'Psychologická péče o subjekty', 125000),

-- Bezpečnost a provoz
(31, 'Vedoucí bezpečnosti', 'Vedení bezpečnostního týmu', 140000),
(32, 'Bezpečnostní pracovník', 'Ochrana osob a majetku', 90000),
(33, 'Operátor bezpečnostních systémů', 'Monitoring a správa bezpečnostních zařízení', 95000),
(34, 'Technik údržby', 'Údržba zařízení a budov', 95000),
(35, 'Správce budovy', 'Správa provozu budovy', 105000),
(36, 'Facility manažer', 'Komplexní správa areálu', 120000),
(37, 'Požární technik', 'Prevence a řešení požárních situací', 100000),
(38, 'Krizový manažer', 'Řízení krizových situací a havárií', 135000),

-- Logistika, stravování a podpora
(39, 'Vedoucí logistiky', 'Řízení logistiky a zásobování', 130000),
(40, 'Logistik', 'Zajištění zásobování a dopravy', 100000),
(41, 'Skladník', 'Správa skladu a zásob', 85000),
(42, 'Vedoucí jídelny', 'Vedení stravovacího provozu', 95000),
(43, 'Kuchař', 'Příprava jídel', 80000),
(44, 'Pomocná síla ve stravování', 'Podpora kuchyně a jídelny', 70000),
(45, 'Řidič', 'Přeprava osob a materiálu', 90000),
(46, 'Úklidový pracovník', 'Úklid a údržba prostor', 70000),

-- IT, data, komunikace
(47, 'IT specialista', 'Správa IT infrastruktury', 120000),
(48, 'Správce databází', 'Správa a údržba databází', 115000),
(49, 'Datový analytik', 'Analýza dat a reporting', 125000),
(50, 'Manažer komunikace', 'Firemní a veřejná komunikace', 130000),
(51, 'PR specialista', 'Vztahy s veřejností a médii', 120000),
(52, 'Webmaster', 'Správa webových stránek', 110000),
(53, 'Technik AV', 'Správa audiovizuální techniky', 95000),

-- Korporátní a specializované pozice
(54, 'Finanční manažer', 'Řízení financí komplexu', 160000),
(55, 'Účetní', 'Finanční evidence a reporting', 110000),
(56, 'Právník', 'Právní záležitosti a compliance', 150000),
(57, 'HR specialista', 'Nábor a rozvoj zaměstnanců', 120000),
(58, 'Marketingový specialista', 'Marketing a PR', 120000),
(59, 'Manažer marketingu', 'Vedení marketingového oddělení', 140000),
(60, 'Manažer HR', 'Vedení lidských zdrojů', 140000),
(61, 'Projektový analytik', 'Analýza a podpora projektů', 120000),
(62, 'Manažer právního oddělení', 'Vedení právního týmu', 155000),
(63, 'Manažer financí', 'Vedení finančního oddělení', 155000),
(64, 'Manažer compliance', 'Vedení compliance týmu', 145000),
(65, 'Manažer rozvoje', 'Rozvoj nových projektů a inovací', 145000),
(66, 'Specialista na etiku', 'Etické posuzování a dohled', 120000),
(67, 'Specialista na hybridizaci', 'Vývoj a testování hybridních druhů', 135000),
(68, 'Specialista na krizové řízení', 'Řízení krizových situací', 130000),
(69, 'Specialista na vzdělávání', 'Vzdělávání a školení zaměstnanců', 115000),
(70, 'Specialista na behaviorální studia', 'Výzkum chování a adaptace', 130000),
(71, 'Specialista na genetiku', 'Genetický výzkum a úpravy', 140000),
(72, 'Specialista na fyziologii', 'Fyziologický výzkum', 135000),
(73, 'Specialista na logistiku', 'Optimalizace logistických procesů', 110000),
(74, 'Specialista na výrobu', 'Dohled nad výrobními procesy', 120000),
(75, 'Specialista na testování', 'Testování produktů a subjektů', 115000),
(76, 'Specialista na bezpečnost', 'Bezpečnostní analýzy a prevence', 120000),
(77, 'Specialista na stravování', 'Výživa a stravovací provoz', 105000),
(78, 'Specialista na personalistiku', 'Podpora HR procesů', 100000),
(79, 'Specialista na finance', 'Podpora finančních operací', 105000),
(80, 'Specialista na právní záležitosti', 'Podpora právního oddělení', 110000),
(81, 'Specialista na marketing', 'Podpora marketingových aktivit', 105000),
(82, 'Specialista na komunikaci', 'Podpora interní a externí komunikace', 100000),
(83, 'Specialista na compliance', 'Podpora compliance aktivit', 100000),
(84, 'Specialista na kvalitu', 'Podpora kvality procesů', 100000),
(85, 'Specialista na údržbu', 'Podpora údržby zařízení', 95000),
(86, 'Specialista na AV techniku', 'Podpora audiovizuální techniky', 95000),
(87, 'Specialista na web', 'Podpora webových stránek', 95000),
(88, 'Specialista na datovou analýzu', 'Podpora datových analýz', 105000),
(89, 'Specialista na simulační prostředí', 'Podpora simulačních zařízení', 105000),
(90, 'Specialista na environmentální dohled', 'Ochrana životního prostředí', 110000);


INSERT INTO building_complexes (id_complex, name, address) VALUES
-- Komplexy specializované na výzkum a vývoj specifických kategorií zvířolidí
(1, 'Feline Research Institute', 'Nishishinjuku, Shinjuku, Tokyo, Japan'),
(2, 'Canine Development Center', 'West 34th Street, Manhattan, New York, USA'),
(3, 'Lagomorph Breeding Complex', 'Charlottenstraße, Berlin-Mitte, Germany'),
(4, 'Marine Mammal Research Facility', 'Bondi Road, Sydney, Australia'),
(5, 'Ursine Adaptation Center', 'Prospekt Mira, Moscow, Russia'),
(6, 'Avian Hybridization Laboratory', 'Al-Azhar Street, Cairo, Egypt'),
(7, 'Reptilian Genetics Complex', 'Avenida Atlântica, Rio de Janeiro, Brazil'),

-- Specializované komplexy pro experimentální a hybridní druhy
(8, 'Experimental Species Laboratory', 'Rue de la Science, Brussels, Belgium'),
(9, 'Advanced Hybrid Research Center', 'Ginza, Chuo City, Tokyo, Japan'),

-- Pilířové a obchodní komplexy pro základní fungování společnosti NekoBuwik Inc.
(10, 'NekoBuwik Global Headquarters', 'Sadie Coles Street, Central London, UK'),
(11, 'NekoBuwik Medical & Ethics Center', 'Marine Drive, Mumbai, India'),
(12, 'NekoBuwik Financial Operations', 'Bahnhofstrasse, Zurich, Switzerland'),
(13, 'NekoBuwik Marketing Division', 'Santa Monica Boulevard, Los Angeles, USA'),
(14, 'NekoBuwik Legal Department', 'Avenue des Champs-Élysées, Paris, France'),
(15, 'NekoBuwik Human Resources Center', 'Potsdamer Platz, Berlin, Germany');

-- === DRUHY ZVÍŘOLIDÍ (SUBJECT_SPECIES) ===
INSERT INTO subject_species (id_specie, full_name, adulthood_year, life_expectancy, fk_complex) VALUES
-- Kočičí typy
(1, 'Felis sapiens domesticus', 6, 50, 1),    -- Domácí kočkoholka/kluk
(2, 'Panthera sapiens leo', 10, 60, 1),        -- Lví zvířolid
(3, 'Acinonyx sapiens jubatus', 8, 56, 1),    -- Gepardí zvířolid
(4, 'Panthera sapiens tigris', 12, 64, 1),     -- Tygří zvířolid
(5, 'Lynx sapiens lynx', 8, 54, 1),           -- Rysí zvířolid

-- Psí typy
(6, 'Canis sapiens familiaris', 4, 44, 2),    -- Obecný psí zvířolid
(7, 'Canis sapiens lupus', 6, 52, 2),         -- Vlčí zvířolid
(8, 'Vulpes sapiens vulpes', 4, 40, 2),       -- Liščí zvířolid
(9, 'Canis sapiens aureus', 6, 48, 2),        -- Šakalí zvířolid
(10, 'Canis sapiens latrans', 6, 46, 2),      -- Kojotí zvířolid

-- Králičí/Zajícovití typy
(11, 'Oryctolagus sapiens cuniculus', 2, 30, 3),  -- Králičí zvířolid
(12, 'Lepus sapiens europaeus', 2, 32, 3),        -- Zaječí zvířolid

-- Mořské savce
(13, 'Tursiops sapiens truncatus', 12, 64, 4),     -- Delfíní zvířolid
(14, 'Phoca sapiens vitulina', 10, 58, 4),         -- Tuleňovitý zvířolid

-- Medvědovití
(15, 'Ursus sapiens arctos', 14, 70, 5),           -- Medvědí zvířolid
(16, 'Ailuropoda sapiens melanoleuca', 12, 66, 5), -- Pandí zvířolid

-- Ptačí typy
(17, 'Falco sapiens peregrinus', 4, 40, 6),       -- Sokolí zvířolid
(18, 'Corvus sapiens corax', 4, 44, 6),           -- Havraní zvířolid
(19, 'Aquila sapiens chrysaetos', 6, 50, 6),      -- Orlí zvířolid
(20, 'Bubo sapiens bubo', 6, 48, 6),              -- Sovější zvířolid

-- Plazí typy
(21, 'Varanus sapiens komodoensis', 10, 56, 7),   -- Varaní zvířolid
(22, 'Python sapiens bivittatus', 8, 52, 7),      -- Hadí zvířolid
(23, 'Crocodylus sapiens niloticus', 16, 76, 7),   -- Krokodýlí zvířolid

-- Experimentální druhy
(24, 'Homo sapiens cattus', 8, 52, 8),            -- Lidská báze s kočičími prvky
(25, 'Homo sapiens caninus', 8, 50, 8),           -- Lidská báze s psími prvky
(26, 'Homo sapiens avianus', 6, 44, 8),           -- Lidská báze s ptačími prvky
(27, 'Homo sapiens reptilianus', 10, 56, 8),       -- Lidská báze s plazími prvky
(28, 'Homo sapiens lagomorphus', 6, 40, 8),       -- Lidská báze se zaječími prvky

-- Hybridní druhy
(29, 'Felis-Canis sapiens hybridus', 8, 48, 9),   -- Kočkopsí hybrid
(30, 'Aves-Felis sapiens hybridus', 6, 46, 9),    -- Ptakokočičí hybrid
(31, 'Ursus-Homo sapiens hybridus', 12, 60, 9),   -- Medvědolidský hybrid
(32, 'Reptilia-Mammalia sapiens hybridus', 10, 54, 9), -- Plazosavčí hybrid
(33, 'Vulpes-Lepus sapiens hybridus', 4, 38, 9),  -- Liškozaječí hybrid

-- Hlodavci
(34, 'Rattus sapiens norvegicus', 2, 28, 3),     -- Krysí zvířolid
(35, 'Mus sapiens musculus', 2, 24, 3),           -- Myší zvířolid
(36, 'Sciurus sapiens vulgaris', 4, 36, 3),       -- Veverčí zvířolid
(37, 'Chinchilla sapiens lanigera', 4, 40, 3),    -- Činčilí zvířolid

-- Kopytníci
(38, 'Equus sapiens caballus', 10, 60, 5),         -- Koňský zvířolid
(39, 'Cervus sapiens elaphus', 8, 56, 5),         -- Jelení zvířolid
(40, 'Capreolus sapiens capreolus', 6, 52, 5),    -- Srnčí zvířolid

-- Poddruhové varianty
(41, 'Felis sapiens birmanensis', 6, 48, 1),      -- Barmská kočkoholka
(42, 'Canis sapiens akita', 4, 42, 2),            -- Akita zvířolid
(43, 'Felis sapiens siamensis', 6, 46, 1),       -- Siamská kočkoholka
(44, 'Canis sapiens germanicus', 4, 44, 2),       -- Německý ovčák zvířolid
(45, 'Felis sapiens bengalensis', 6, 50, 1);      -- Bengálská kočkoholka 


-- no problema