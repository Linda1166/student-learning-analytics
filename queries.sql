-- Equivalent to sql_summary() in analysis.py.
-- The Python runner creates students and study_categories in SQLite.
-- Bind NULL twice to use both schools; bind 'GP' twice to filter one school.
SELECT s.studytime, l.study_label, COUNT(*) AS n,
       AVG(s.G3) AS mean_grade, AVG(s.absences) AS mean_absences
FROM students AS s
INNER JOIN study_categories AS l ON s.studytime = l.studytime
WHERE (? IS NULL OR s.school = ?)
GROUP BY s.studytime, l.study_label
HAVING COUNT(*) >= 1
ORDER BY s.studytime;
