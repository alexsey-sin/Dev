-- SQLite

.help
-- Список таблиц
.tables

-- Очистка файла базы после удаления записей
VACUUM

SELECT count(*) as cnt FROM domconnect_dccrmlid

DELETE FROM domconnect_dccrmlid
WHERE create_date < '2022-03-01 00:00:00'


DELETE FROM domconnect_dccashseo
WHERE val_date < '2022-03-01'
