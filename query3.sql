-- 3: All clients based on the number of projects
-- -  text size is based on the project ID
-- -  the color of the text is based on the main color
SELECT company_name, id, main_color
FROM project
WHERE main_color IS NOT NULL
GROUP BY company_name, id, main_color
ORDER BY id