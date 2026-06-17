SELECT annotator_id, article_id, political_typology, effect, explanation, 
       article_index, change, reinforce, date_created
  FROM "webis.annotation.tool".annotator_task;

SELECT COUNT(*) FROM "webis.annotation.tool".annotator_task;

SELECT annotator_id, max(article_index) n, batch

FROM   "webis.annotation.tool".annotator_task
INNER JOIN "webis.annotation.tool".annotator on id= annotator_id
GROUP BY annotator_id, batch
ORDER BY batch, n

SELECT max(article_index) from "webis.annotation.tool".annotator_task where ANNOTATOR_ID = 'C14'
SELECT * from "webis.annotation.tool".annotator_task where ANNOTATOR_ID = 'C14'  ORDER BY article_index
  insert into "webis.annotation.tool".annotator values ('tester', 'C20', 'batch3', 'Market Skeptic Republicans')

SELECT * from "webis.annotation.tool".annotator_task where annotator_id = 'L11' and article_index = 91
commit
SELECT * from "webis.annotation.tool".annotator ORDER BY ID


SELECT effect, explanation, 
       change, reinforce
  FROM "webis.annotation.tool".annotator_task WHERE effect = 3


  SELECT effect, explanation, 
       change, reinforce
  FROM "webis.annotation.tool".annotator_task WHERE effect = 3

 
  SELECT * FROM "webis.annotation.tool".annotator  ORDER BY id

UPDATE "webis.annotation.tool".annotator SET id = 'C05O' where id = 'C05'

  COPY annotator_task (annotator_id, article_id, political_typology, effect, explanation, article_index, change, reinforce, date_created) FROM stdin;
  COPY "webis.annotation.tool".annotator_task TO '/home/cifo3206/Documents/projects-private/emnlp2018/data/annotations/annotations_latest.csv' DELIMITER ',' CSV HEADER;


  SELECT * FROM  "webis.annotation.tool".annotator_task  where article_index = NULL

  UPDATE "webis.annotation.tool".annotator_task
  SET article_index = 91
  WHERE annotator_id = 'L11' AND article_id = '1773203.txt'
  SELECT * FROM "webis.annotation.tool".annotator_task WHERE annotator_id = 'L11' AND article_id = '1773203.txt'

 SELECT * FROM "webis.annotation.tool".annotator_task WHERE article_index 