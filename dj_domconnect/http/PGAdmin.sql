-- Перечень таблиц
-- SELECT table_name FROM information_schema.tables;


-- SELECT count(*) as cnt FROM public.api_txv
-- WHERE "pv_code" = 4 AND "pub_date" > '2022-02-18 11:30:00';


-- SELECT COUNT(*) as cnt FROM public.api_txv
-- WHERE "pv_code" = 4 AND "pub_date" > '2022-05-18 11:30:00';

-- SELECT count(*) as cnt FROM api_bidbeeline2
-- WHERE status = 2 AND bot_log LIKE '%ИНН должен состоять из 10 или 12%'


UPDATE api_bidbeeline2
SET status = 0, bot_log = ''
WHERE status = 2 AND bot_log LIKE '%ИНН должен состоять из 10 или 12%'




