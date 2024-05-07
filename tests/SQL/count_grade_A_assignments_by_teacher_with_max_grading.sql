SELECT COUNT(*) AS count_grade_a  
FROM assignments AS assg
JOIN teachers AS t ON assg.teacher_id = t.id 
WHERE assg.grade = 'A'  
GROUP BY t.id  
ORDER BY count_grade_a DESC
LIMIT 1; 