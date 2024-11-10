SELECT COUNT(*) as num_estrellas, constellation 
FROM stars 
GROUP BY constellation 
ORDER BY num_estrellas DESC 
LIMIT 5;
