-- 1: All clients at once
-- -  text size is based on the number of projects from the client
-- -  the color of the text should be the mix of the project colors from the client

SELECT company_name, COUNT(company_name) AS number_of_projects, string_agg(main_color, ' ') AS colors
FROM project
GROUP BY company_name;
