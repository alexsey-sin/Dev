PostgreSQL
база: django
user: alex
password: J3UHx4rwWR
host: 127.0.0.1
port: 5432
django.domconnect.ru

master-pasword: root
=========================================


SELECT pub_date FROM public.api_txv
WHERE "pub_date" < '2022-02-15 00:00:00'
ORDER BY pub_date DESC


DELETE FROM public.api_txv
WHERE "pub_date" < '2022-02-15 00:00:00'

SELECT * FROM public.api_bidrostelecom2


SELECT count(*) as cnt FROM public.mobile_mobiledata


ТХВ Ростелеком
=========================================================
SELECT count(*) as cnt FROM public.api_txv
WHERE "pv_code" = 4 AND "pub_date" > '2022-02-18 11:30:00'

SELECT count(*) as cnt FROM public.api_txv
WHERE "pv_code" = 4 AND "pub_date" > '2022-02-18 11:30:00' AND "status" = 3



Проблемные заявки АВТО Билайн ФЛ
=========================================================
SELECT id_lid, city, street, house, apartment, tarif,
pub_date, bot_log
FROM public.api_bidbeeline
WHERE "pub_date" > '2022-01-01 00:00:00'
AND "status" = 2


Удаляем кэш последнего месяца
=========================================================
DELETE FROM public.domconnect_dccashseo
WHERE "val_date" >= '2022-02-01 00:00:00'

Сколько лидов за несколько дней
=========================================================
SELECT count(*) as cnt FROM public.domconnect_dccrmlid
WHERE "create_date" >= '2022-03-01 00:00:00' AND "create_date" < '2022-03-03 00:00:00'

Скачать ошибки
=========================================================
SELECT region, city, street, house, apartment, bot_log FROM public.api_txv
WHERE "pv_code" = 4 AND "status" = 2
ORDER BY pub_date DESC
LIMIT 100

Скачать ошибки ТхВ Билайн
=========================================================
SELECT region, city, street, house, apartment, bot_log FROM public.api_txv
WHERE pv_code = 1 AND status = 2
ORDER BY pub_date DESC


Удаляем заявки ТхВ старые ДомРу
=========================================================
DELETE FROM public.api_txv
WHERE "pv_code" = 2 AND "pub_date" < '2022-03-22 15:00:00'


Удаляем заявки ТхВ старые Ростелеком
которые бот забрал заявки и работа его была прервана
=========================================================
DELETE FROM public.api_txv
WHERE "pv_code" = 4 AND "pub_date" < '2022-03-22 15:00:00' AND "status" = 1


Удаляем все миграции
=========================================================
DELETE FROM public.django_migrations
WHERE app = 'domconnect'

manage.py migrate --fake contenttypes

ALTER TABLE django_content_type ADD COLUMN name character varying(50) NOT NULL DEFAULT 'someName'

INSERT INTO public.django_migrations (app, name, applied) 
VALUES ('mobile', '0001_initial', '2022-04-17 18:21:41.472674+03')
=========================================================
pv_code = 4  AND

SELECT count(*) FROM public.api_txv
WHERE status = 2 AND bot_log LIKE '%This version of ChromeDriver only supports Chrome%'

UPDATE public.api_txv
SET status = 0, bot_log = ''
WHERE pv_code = 4 AND status = 2 AND bot_log LIKE '%This version of ChromeDriver only supports Chrome%'

Исправляем статус в ТхВ МТС
=========================================================
UPDATE public.api_txv
SET status = 0, bot_log = ''
WHERE pv_code = 3 AND status = 2

Исправляем статус в ТхВ Билайн
=========================================================
UPDATE public.api_txv
SET status = 0, bot_log = ''
WHERE pv_code = 1 AND status = 2 AND pub_date > '2022-04-10 00:00:00'

UPDATE public.api_txv
SET status = 0, bot_log = ''
WHERE pv_code = 7 AND status = 2 AND bot_log LIKE '%Учетная запись пользователя заблокирована%'

UPDATE public.api_txv
SET status = 0, bot_log = '', password_2 = 'Sjod@!5812'
WHERE pv_code = 7 AND status = 2 AND bot_log LIKE '%Для продолжения работы Вам нужно ввести Имя и Пароль%'

UPDATE public.api_txv
SET status = 0, bot_log = ''
WHERE pv_code = 4 AND status = 2 AND
(bot_log LIKE '%Неверное имя пользователя или пароль%'
OR bot_log LIKE '%Учетная запись пользователя заблокирована%'
OR bot_log LIKE '%Нет ссылки Создать заявку ФЛ%')


=========================================================
SELECT * FROM api_botvisit
INSERT INTO api_botvisit

INSERT INTO api_botaccess
("name", "last_visit", "omission_min", "work", "login", "login_2", "password", "password_2")
VALUES
('Бот автозаявки ОнЛайм','2022-03-31 11:43:28+03',120,False,'inetme12','','RxIT9oxP',''),
('Бот автозаявки ДомРу','2022-03-31 16:02:32.054198+03',120,True,'sinitsin','','BVNocturne20',''),
('Бот автозаявки Билайн_ЮЛ','2022-03-31 16:02:15.052934+03',120,True,'parther_key','','AD8AE6EF4C084ED1',''),
('Бот автозаявки ТТК','2022-03-31 16:02:33.05635+03',120,True,'wd_dc_sg','','QgdjJGNm',''),
('Бот автозаявки МГТС','2022-03-31 16:02:34.052878+03',120,True,'ESubbotin','MChumakova','sr@8Cjmu','Qhvv@!4817'),
('ATS-TRUNK','2022-03-31 15:20:50.647078+03',120,True,'login','','password',''),
('Парсер ЛК mts','2022-03-31 15:24:06.440835+03',120,True,'YrxF9TvrPlK6fbkJNBilUqCw0vUa','','hFtsFhai1ZjtuYg_y58fArkaBCEa',''),
('Парсер ЛК beeline','2022-03-31 15:27:36.868706+03',120,True,'S715792964','','MuE8$lVGpo',''),
('Бот автозаявки Билайн','2022-03-31 16:02:36.057676+03',120,True,'S24-61','1010000101','Ft&dhdk234hbs3',''),
('Бот автозаявки МТС','2022-03-31 16:02:37.054544+03',120,True,'GRYURYEV','','UcoTWY',''),
('Парсер ЛК megafon','2022-03-31 15:18:33.513076+03',120,True,'9201337110','','dkk3D2',''),
('Бот ТХВ Билайн','2022-03-31 16:02:37.079338+03',120,True,'S01-181','1999999222','8GFysus@kffs7',''),
('Бот ТХВ МГТС','2022-03-31 16:02:37.267546+03',120,True,'ESubbotin','MChumakova','sr@8Cjmu','Qhvv@!4817'),
('Бот автозаявки Ростелеком_ЮЛ','2022-03-31 16:02:38.062571+03',120,True,'mos.domconnect@gmail.com','','bvo[7dGr',''),
('Бот ТХВ МТС','2022-03-31 16:02:38.467234+03',120,True,'GRYURYEV','','UcoTWY',''),
('Бот ТХВ ДомРу','2022-03-31 16:02:38.680241+03',120,True,'sinitsin','','BVNocturne20',''),
('Бот ТХВ ТТК','2022-03-31 16:02:38.88183+03',120,True,'wd_dc_sg','','QgdjJGNm',''),
('Бот автозаявки Ростелеком','2022-03-31 16:02:39.061984+03',120,True,'sz_v_an','','m~|HqEu~VB}|P1QDrDX%',''),
('Бот ТХВ ОнЛайм','2022-03-31 16:02:39.090312+03',120,True,'inetme12','','RxIT9oxP',''),
('Бот ТХВ Ростелеком','2022-03-31 15:57:45.925558+03',120,True,'sz_v_an','','m~|HqEu~VB}|P1QDrDX%','')





SELECT count(*) FROM public.api_bid_beeline
WHERE status = 2 AND bot_log LIKE '%Message: session not created%'


UPDATE public.api_txv
SET status = 0, bot_log = ''
WHERE status = 2 AND bot_log LIKE '%Message: session not created%'


Стат SEO
=========================================================
SELECT count(*) as cnt FROM public.domconnect_dccrmlid
WHERE crm_1592566018 = 'SEO' AND create_date >= '2022-03-01 00:00:00' AND create_date < '2022-04-01 00:00:00'

DELETE FROM public.domconnect_dccrmlid
DELETE FROM public.domconnect_dccrmdeal
DELETE FROM public.domconnect_dccashseo



Исправляем заявки ТхВ МТС
=========================================================
SELECT count(*) FROM public.api_txv
WHERE pv_code = 3 AND status = 2 AND bot_log LIKE '%Ошибка нет поля логин%'

UPDATE public.api_txv
SET status = 0, bot_log = ''
WHERE pv_code = 3 AND status = 2 AND bot_log LIKE '%Ошибка нет поля логин%'

Исправляем заявки ТхВ ТТК
=========================================================
SELECT count(*) FROM public.api_txv
WHERE pv_code = 5 AND status = 2 AND bot_log LIKE '%Нет ссылки Сводные панели%'

UPDATE public.api_txv
SET status = 0, bot_log = '', password = '9zWxQjOh'
WHERE pv_code = 5 AND status = 2 AND bot_log LIKE '%Нет ссылки Сводные панели%'


Повторяющиеся записи УДАЛЕНИЕ!!!!
=========================================================
Просмотр
SELECT COUNT(*) cnt FROM public.api_txv
GROUP BY region, city, street, house, apartment, pv_code
HAVING COUNT(*) > 1
=================

DELETE FROM public.api_txv a USING (SELECT
        MAX(b.id) mid, b.region, b.city, b.street, b.house, b.apartment, b.pv_code
        FROM public.api_txv b
        GROUP BY b.region, b.city, b.street, b.house, b.apartment, b.pv_code
    ) c
WHERE
    a.region = c.region
    AND a.city = c.city
    AND a.street = c.street
    AND a.house = c.house
    AND a.apartment = c.apartment
    AND a.pv_code = c.pv_code
    AND a.id < c.mid
=========================================================






SET status = 0, bot_log = ''
WHERE pv_code = 7 AND status = 2 AND bot_log LIKE '%Учетная запись пользователя заблокирована%'

UPDATE public.api_txv
SET status = 0, bot_log = ''
WHERE pv_code = 3 AND status = 2 AND bot_log LIKE '%Message: binary is not a Firefox executable%'

SELECT count(*) FROM public.api_txv
WHERE pv_code = 7 AND status = 2 AND bot_log LIKE '%нет поля login/Ошибка%'


UPDATE public.api_txv
SET status = 0, bot_log = '', login = 'MChumakova', password = 'L4gi5cwJ'
WHERE pv_code = 7 AND status = 2 AND bot_log LIKE '%нет поля login/Ошибка%'


SELECT count(*) FROM public.api_txv
WHERE available_connect = '' AND bot_log = ''



