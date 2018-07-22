---- Get DAY
SELECT to_char(date,'Day') as "DAY", gas_station.id, name, brand, street, AVG(e5) as e5
FROM gas_station_min_history, gas_station
WHERE date > now() - interval '3 weeks' AND place='Dortmund'
GROUP BY 1, gas_station.id 
ORDER BY e5
LIMIT 1

---- AS JSON
SELECT json_agg(x) FROM (SELECT to_char(date,'Day') as "DAY", gas_station.id, name, brand, street, AVG(e5) as e5
FROM gas_station_min_history, gas_station
WHERE date > now() - interval '3 weeks' AND place='Dortmund'
GROUP BY 1, gas_station.id 
ORDER BY e5
LIMIT 1) as x;

---- Get Time
Select to_char(date,'HH24:MI') as "TIME", to_char(date,'Day') as "DAY"
FROM gas_station_information_history
WHERE stid='005056ba-7cb6-1ed2-bceb-57e186e40d16' AND date > now() - interval '1 weeks' 
AND e5=(
 SELECT MIN(e5) 
 FROM gas_station_information_history 
 WHERE  stid='005056ba-7cb6-1ed2-bceb-57e186e40d16' AND date > now() - interval '1 weeks') 

