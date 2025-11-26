insert into mange(numespece,numaliment)
select numespece,numaliment 
from espece 
cross join aliment
order by 1,2;

DELETE FROM mange
WHERE (numespece, numaliment) IN
(SELECT numespece,numaliment FROM mange
ORDER BY RANDOM()
LIMIT (320*0.2));
