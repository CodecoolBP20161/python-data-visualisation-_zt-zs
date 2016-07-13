-- 2: Project names
-- -  text size is based on the budget (take care of the different currencies!)
-- -  the color of the text should come from the database (project.main_color)

SELECT name AS project_name,
CASE WHEN budget_currency='USD' THEN round(budget_value::real / 1.11)
     WHEN budget_currency='GBP' THEN round(budget_value::real * 1.18)
     END AS budget_EUR,
               main_color
 FROM project
WHERE name IS NOT NULL
ORDER BY budget_EUR;