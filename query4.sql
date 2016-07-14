-- 4: All company HQ
-- -  text size is based on the ID
-- -  the color of the text is based on the main color
SELECT company_hq, id, main_color
FROM project
WHERE company_hq IS NOT NULL
