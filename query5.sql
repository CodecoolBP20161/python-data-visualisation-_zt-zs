-- 5: All managers
-- -  text size is based on the status ID
-- -  the color of the text is based on the main color
SELECT DISTINCT manager, status, main_color
FROM project
WHERE manager IS NOT NULL AND main_color IS NOT NULL;