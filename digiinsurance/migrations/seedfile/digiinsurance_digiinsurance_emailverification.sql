-- MySQL dump 10.13  Distrib 8.0.23, for Win64 (x86_64)
--
-- Host: db-mysql-sgp1-52145-do-user-6523329-0.b.db.ondigitalocean.com    Database: digiinsurance
-- ------------------------------------------------------
-- Server version	8.0.23

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '125b46f7-bd8f-11eb-9da3-ca8ebb750982:1-19450,
be53edbf-f7f8-11ea-b541-66d0fb5d070c:1-38449';

--
-- Table structure for table `digiinsurance_emailverification`
--

DROP TABLE IF EXISTS `digiinsurance_emailverification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `digiinsurance_emailverification` (
  `id` int NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `modified_at` datetime(6) NOT NULL,
  `email` varchar(254) NOT NULL,
  `token` longtext NOT NULL,
  `is_archived` tinyint(1) NOT NULL,
  `type` varchar(1) NOT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `digiinsurance_emailv_user_id_8035fd88_fk_digiinsur` FOREIGN KEY (`user_id`) REFERENCES `digiinsurance_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=116 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digiinsurance_emailverification`
--

LOCK TABLES `digiinsurance_emailverification` WRITE;
/*!40000 ALTER TABLE `digiinsurance_emailverification` DISABLE KEYS */;
INSERT INTO `digiinsurance_emailverification` VALUES (1,'2021-07-15 00:56:04.993424','2021-07-15 00:56:04.993473','gojo@example.com','b\'eyJ1aWQiOiAyLCAiZW1haWwiOiAiZ29qb0BleGFtcGxlLmNvbSIsICJ0b2tlbiI6ICJhcHRrdGctODhkM2NhNzY1ZjE3YjU1M2E3ZjVhZTczYmI0ZTk3MTgifQ==\'',0,'v',2),(2,'2021-07-15 03:56:44.643820','2021-07-15 03:56:44.643820','v@v.com','b\'eyJ1aWQiOiA3LCAiZW1haWwiOiAidkB2LmNvbSIsICJ0b2tlbiI6ICJhcHR0NmstZjUwM2U3ZjJiZjhhNWFkOWRmMTQ1MGQ4OWYyMTIxMTkifQ==\'',0,'v',7),(11,'2021-07-15 05:56:33.448600','2021-07-15 05:56:33.448600','2ndcabrera23@gmail.com','b\'eyJ1aWQiOiAxNiwgImVtYWlsIjogIjJuZGNhYnJlcmEyM0BnbWFpbC5jb20iLCAidG9rZW4iOiAiYXB0eXE5LTEwNmQzYjgxNTJjNDBmZTUxYTFjZDdlMTVjY2ZmNDhlIn0=\'',0,'v',16),(12,'2021-07-15 06:07:39.035432','2021-07-15 06:07:39.035432','2ndcabrera24@gmail.com','b\'eyJ1aWQiOiAxNywgImVtYWlsIjogIjJuZGNhYnJlcmEyNEBnbWFpbC5jb20iLCAidG9rZW4iOiAiYXB0ejhxLTFkYjZhMDIxMDNkNjZkZDliZTliZDQ1NTY3MDFjZGVkIn0=\'',0,'v',17),(13,'2021-07-15 07:04:24.875799','2021-07-15 07:04:24.876740','2ndcabrera25@gmail.com','b\'eyJ1aWQiOiAxOCwgImVtYWlsIjogIjJuZGNhYnJlcmEyNUBnbWFpbC5jb20iLCAidG9rZW4iOiAiYXB1MXZjLWFiMWU5MDc0ZjllM2JiZGFkOTk5ZjZiNTMwOTk2OThlIn0=\'',0,'v',18),(18,'2021-07-15 07:28:52.368831','2021-07-15 07:28:52.368831','2ndcabrera26@gmail.com','b\'eyJ1aWQiOiAyMywgImVtYWlsIjogIjJuZGNhYnJlcmEyNkBnbWFpbC5jb20iLCAidG9rZW4iOiAiYXB1MzA0LTViZGNmZGEyMjkwZTJhNTNkNWNlMWI0MTU1NTAyNGFhIn0=\'',0,'v',23),(27,'2021-07-15 08:22:21.194603','2021-07-15 08:22:21.194806','renz.valentino@gmail.com','b\'eyJ1aWQiOiAzNCwgImVtYWlsIjogInJlbnoudmFsZW50aW5vQGdtYWlsLmNvbSIsICJ0b2tlbiI6ICJhcHU1aDktM2E2M2UxZTJkNTI5OThmZWJmZmUyOWRkYjg0ZjQzNjYifQ==\'',0,'v',34),(66,'2021-07-15 14:00:32.092287','2021-07-15 14:00:32.092361','renz.valentino3@gmail.com','b\'eyJ1aWQiOiA4MCwgImVtYWlsIjogInJlbnoudmFsZW50aW5vM0BnbWFpbC5jb20iLCAidG9rZW4iOiAiYXB1bDR3LWM5YTMyNDI0YTc2N2VmZjI0ZDRkZjY0YjNkZDYyOTJlIn0=\'',0,'v',80),(67,'2021-07-15 14:05:58.605785','2021-07-15 14:05:58.605828','renz.valentino+1@gmail.com','b\'eyJ1aWQiOiA4MSwgImVtYWlsIjogInJlbnoudmFsZW50aW5vKzFAZ21haWwuY29tIiwgInRva2VuIjogImFwdWxkeS05MDQ1MTBjN2M4OTc2ZmI1MGRmYmVhZDM3YWY5Yzc2MSJ9\'',0,'v',81),(68,'2021-07-15 14:07:17.716649','2021-07-15 14:07:17.716793','renz.valentino+2@gmail.com','b\'eyJ1aWQiOiA4MiwgImVtYWlsIjogInJlbnoudmFsZW50aW5vKzJAZ21haWwuY29tIiwgInRva2VuIjogImFwdWxnNS1hMTIzNjc5YTk2YzMxZTNiZGUyNTlkMWJiMjdkNTk3NSJ9\'',0,'v',82),(69,'2021-07-15 14:16:27.704504','2021-07-15 14:16:27.704546','renz.valentino+3@gmail.com','b\'eyJ1aWQiOiA4MywgImVtYWlsIjogInJlbnoudmFsZW50aW5vKzNAZ21haWwuY29tIiwgInRva2VuIjogImFwdWx2Zi1hNWY3ZDVhZTFkNTI2ZDY4ZGJkMTFhNGQ4YWRjNjY4ZiJ9\'',0,'v',83),(70,'2021-07-15 14:22:36.482237','2021-07-15 14:22:36.482299','renz.valentino+4@gmail.com','b\'eyJ1aWQiOiA4NCwgImVtYWlsIjogInJlbnoudmFsZW50aW5vKzRAZ21haWwuY29tIiwgInRva2VuIjogImFwdW01by1iYmU1YWRlZDk1YmI5MDdlMmNhZjNkMWNmOGJjYTAyMiJ9\'',0,'v',84),(71,'2021-07-16 01:11:59.172227','2021-07-16 01:11:59.172298','carlo_coste@questronix.com.ph','b\'eyJ1aWQiOiA4NSwgImVtYWlsIjogImNhcmxvX2Nvc3RlQHF1ZXN0cm9uaXguY29tLnBoIiwgInRva2VuIjogImFwdmc3ei1hMGIwNWQ2MzQ4ZjE3ZDgxZTNkMDM3NzY0ZTU3ZmYxNyJ9\'',1,'v',85),(72,'2021-07-16 01:16:50.409626','2021-07-16 01:16:50.409626','2ndcabrera27@gmail.com','b\'eyJ1aWQiOiA4NiwgImVtYWlsIjogIjJuZGNhYnJlcmEyN0BnbWFpbC5jb20iLCAidG9rZW4iOiAiYXB2Z2cyLWIwN2NjY2U0OWNlOGJjNThmMjU4NDM5ZjAxNjM3YTVlIn0=\'',0,'v',86),(82,'2021-07-16 03:30:58.760679','2021-07-16 03:30:58.760714','vkalmazan@gmail.com','b\'eyJ1aWQiOiA5NywgImVtYWlsIjogInZrYWxtYXphbkBnbWFpbC5jb20iLCAidG9rZW4iOiAiYXB2bW5tLTZiYmYyZjVkNTc5MDkwNTk4MDJlZTkwYjZjNDYyNzQ5In0=\'',1,'v',97),(83,'2021-07-16 03:50:24.113187','2021-07-16 03:50:24.113225','amenxd01@gmail.com','b\'eyJ1aWQiOiA5OCwgImVtYWlsIjogImFtZW54ZDAxQGdtYWlsLmNvbSIsICJ0b2tlbiI6ICJhcHZuazAtYjZmMTI2NDhkOTYxZDUxMTMyZDAwYzlmZDNiYTYyOWYifQ==\'',1,'v',98),(84,'2021-07-16 03:56:59.607608','2021-07-16 03:56:59.607641','rexcornes@yahoo.com','b\'eyJ1aWQiOiA5OSwgImVtYWlsIjogInJleGNvcm5lc0B5YWhvby5jb20iLCAidG9rZW4iOiAiYXB2bnV6LTdkOTNkMzNmMDRjM2Y5Yzc3MjliYTk2NDg4MjA2MjEzIn0=\'',0,'v',99),(85,'2021-07-16 04:52:53.280933','2021-07-16 04:52:53.280966','chanbu0217@gmail.com','b\'eyJ1aWQiOiAxMDAsICJlbWFpbCI6ICJjaGFuYnUwMjE3QGdtYWlsLmNvbSIsICJ0b2tlbiI6ICJhcHZxZzUtOTQ4Y2YyNWI3MmJjZDJjZjQzYjU0NDFmYTVkZDliNWIifQ==\'',0,'v',100),(87,'2021-07-16 05:01:29.226131','2021-07-16 05:01:29.226169','iamclient@gmail.com','b\'eyJ1aWQiOiAxMDIsICJlbWFpbCI6ICJpYW1jbGllbnRAZ21haWwuY29tIiwgInRva2VuIjogImFwdnF1aC1jNzAzZTlkNTQ3N2FhYTNjOWJjMmNjNWVhNTA2M2MxOCJ9\'',0,'v',102),(88,'2021-07-16 06:06:04.919921','2021-07-16 06:06:04.919962','angel.dummy.test@gmail.com','b\'eyJ1aWQiOiAxMDMsICJlbWFpbCI6ICJhbmdlbC5kdW1teS50ZXN0QGdtYWlsLmNvbSIsICJ0b2tlbiI6ICJhcHZ0dTQtNjIwNjJjZGE1NWJkYzFiNmU0MTg2MjlmMDFjMjhhMzcifQ==\'',1,'v',103),(89,'2021-07-16 07:12:45.316100','2021-07-16 07:12:45.316142','algaringo@gmail.com','b\'eyJ1aWQiOiAxMDYsICJlbWFpbCI6ICJhbGdhcmluZ29AZ21haWwuY29tIiwgInRva2VuIjogImFwdnd4OS04OGRmMDJjNjhmYmU5YjhkYjMwYjMyOGJkYTlmMzIwZiJ9\'',1,'v',106),(90,'2021-07-21 01:53:52.635817','2021-07-21 01:53:52.635857','angelugaringo@gmail.com','b\'eyJ1aWQiOiAxMDcsICJlbWFpbCI6ICJhbmdlbHVnYXJpbmdvQGdtYWlsLmNvbSIsICJ0b2tlbiI6ICJhcTRyaHMtNWUwYjczMTVhN2JhMmE5ZWMyNDI0ZWJjODE4ZmQyNGIifQ==\'',1,'v',107),(91,'2021-07-21 06:18:21.504522','2021-07-21 06:18:21.504579','elijah.cephia_bagio@questronix.com.ph','b\'eyJ1aWQiOiAxMDksICJlbWFpbCI6ICJlbGlqYWguY2VwaGlhX2JhZ2lvQHF1ZXN0cm9uaXguY29tLnBoIiwgInRva2VuIjogImFxNTNxbC00ZDQ4YjZjN2FlNDM3YWIxNmRmYWRmMTM3Y2RhNjQ3NCJ9\'',0,'v',109),(92,'2021-07-21 06:19:08.829505','2021-07-21 06:19:08.829542','rmfquijada@gmail.com','b\'eyJ1aWQiOiAxMTAsICJlbWFpbCI6ICJybWZxdWlqYWRhQGdtYWlsLmNvbSIsICJ0b2tlbiI6ICJhcTUzcnctNmM5ZjQwYjQyNjc5OTU0MmNlMzJlMzFiMDU0NDc5MTkifQ==\'',0,'v',110),(93,'2021-07-21 06:30:45.427322','2021-07-21 06:30:45.427360','rjdeguzman@upedu.ph','b\'eyJ1aWQiOiAxMTEsICJlbWFpbCI6ICJyamRlZ3V6bWFuQHVwZWR1LnBoIiwgInRva2VuIjogImFxNTRiOS01ZDY4ZTZkMTI1YWQzMmNiNDg0ZjlmMmE1ZWUwYjQyYyJ9\'',0,'v',111),(94,'2021-07-21 08:21:08.263986','2021-07-21 08:21:08.264022','burazon1@up.edu.ph','b\'eyJ1aWQiOiAxMTIsICJlbWFpbCI6ICJidXJhem9uMUB1cC5lZHUucGgiLCAidG9rZW4iOiAiYXE1OWY4LWIyODgxMTBjNGQxYjc2NDMzMGFhYjcwZTNlNmNmMTg3In0=\'',1,'v',112),(96,'2021-07-21 08:30:10.748622','2021-07-21 08:30:10.748808','psylacantos.trial@gmail.com','b\'eyJ1aWQiOiAxMTQsICJlbWFpbCI6ICJwc3lsYWNhbnRvcy50cmlhbEBnbWFpbC5jb20iLCAidG9rZW4iOiAiYXE1OXVhLWRhOGU3OGJlOWEyZGZlYjQyZDYzODdkNTVlMmNjM2VmIn0=\'',0,'v',114),(98,'2021-07-21 08:37:44.616079','2021-07-21 08:37:44.616110','reenamyka@yahoo.com','b\'eyJ1aWQiOiAxMTYsICJlbWFpbCI6ICJyZWVuYW15a2FAeWFob28uY29tIiwgInRva2VuIjogImFxNWE2dy02ZTk2ZjQwN2M1ZDNjZDJkMmI3ZDE4MGEzZGIzZGJhNiJ9\'',0,'v',116),(102,'2021-07-22 04:23:39.986654','2021-07-22 04:23:39.986700','jpdenopol@up.edu.ph','b\'eyJ1aWQiOiAxMjEsICJlbWFpbCI6ICJqcGRlbm9wb2xAdXAuZWR1LnBoIiwgInRva2VuIjogImFxNnQzZi02OWQ3Yjc0YzYxNDA5NDdkN2MzMzY3YzAyYzhhNmZmNSJ9\'',1,'v',121),(103,'2021-07-22 09:05:49.367976','2021-07-22 09:05:49.367976','lex@gmail.com','b\'eyJ1aWQiOiAxMjUsICJlbWFpbCI6ICJsZXhAZ21haWwuY29tIiwgInRva2VuIjogImFxNzY1cC03ZDZkOWExNzE0NzkzODdkZGU4ZTQ2MjVkNjg3MDcxZSJ9\'',0,'v',125),(104,'2021-07-23 02:11:29.408875','2021-07-23 02:11:29.408875','testuser@example.com','b\'eyJ1aWQiOiAxMjYsICJlbWFpbCI6ICJ0ZXN0dXNlckBleGFtcGxlLmNvbSIsICJ0b2tlbiI6ICJhcThobjUtZWVkMDcwODAzNTk3YmQ3YjQyZDE1NDQ4YzRjMmVkN2UifQ==\'',0,'v',126),(105,'2021-07-23 02:15:48.272471','2021-07-23 02:15:48.272529','bermylle@gmail.com','b\'eyJ1aWQiOiAxMjcsICJlbWFpbCI6ICJiZXJteWxsZUBnbWFpbC5jb20iLCAidG9rZW4iOiAiYXE4aHVjLWZkNDNiZGEyZDYzYjI1ZGMxZjYyNDM4MjQ4NWJlNzRkIn0=\'',1,'v',127),(106,'2021-07-23 03:35:12.992180','2021-07-23 03:35:12.992180','testuser05@example.com','b\'eyJ1aWQiOiAxMzAsICJlbWFpbCI6ICJ0ZXN0dXNlcjA1QGV4YW1wbGUuY29tIiwgInRva2VuIjogImFxOGxpby1kZjFiN2I1YjViMDUwN2RkNWIwNzNmYmU0MDEyZDBlOSJ9\'',0,'v',130),(107,'2021-07-23 04:54:22.271788','2021-07-23 04:54:22.271788','testuser699@example.com','b\'eyJ1aWQiOiAxMzEsICJlbWFpbCI6ICJ0ZXN0dXNlcjY5OUBleGFtcGxlLmNvbSIsICJ0b2tlbiI6ICJhcThwNm0tMzc5MmQzNjBhY2Q4NDEwMmU5NzQ1ODY1Y2IzNjYyODYifQ==\'',0,'v',131),(108,'2021-07-23 06:00:43.328093','2021-07-23 06:00:43.328137','rjdeguzman@up.edu.ph','b\'eyJ1aWQiOiAxMzIsICJlbWFpbCI6ICJyamRlZ3V6bWFuQHVwLmVkdS5waCIsICJ0b2tlbiI6ICJhcThzOTctNzBkMGNkMGVhYzBlNWUwZWU1ODc5YTFmNmU0OTQ1MTgifQ==\'',0,'v',132),(109,'2021-07-23 07:13:15.512258','2021-07-23 07:13:15.512258','testuser69@example.com','b\'eyJ1aWQiOiAxMzMsICJlbWFpbCI6ICJ0ZXN0dXNlcjY5QGV4YW1wbGUuY29tIiwgInRva2VuIjogImFxOHZtMy05M2NiMGI0YzBhYjk0Y2I0Y2MwYmRmZGEzZTUyZmFkYSJ9\'',0,'v',133),(110,'2021-07-23 08:15:28.135377','2021-07-23 08:15:28.135377','testuser695@example.com','b\'eyJ1aWQiOiAxMzQsICJlbWFpbCI6ICJ0ZXN0dXNlcjY5NUBleGFtcGxlLmNvbSIsICJ0b2tlbiI6ICJhcTh5aHMtZTM3MDc0NWYwYjczMzVmMGRkZDMwZjNiYjM0MGU4N2QifQ==\'',0,'v',134),(111,'2021-07-23 08:18:41.167787','2021-07-23 08:18:41.167835','bermyllerazon@ymail.com','b\'eyJ1aWQiOiAxMzUsICJlbWFpbCI6ICJiZXJteWxsZXJhem9uQHltYWlsLmNvbSIsICJ0b2tlbiI6ICJhcTh5bjUtMjBjYmY0NzAxYWVkZGU1YjA5ZmIzOTAyMTk2Yzc0ZmIifQ==\'',1,'v',135),(112,'2021-07-25 22:59:16.141636','2021-07-25 22:59:16.141682','tatopi2092@britted.com','b\'eyJ1aWQiOiAxMzYsICJlbWFpbCI6ICJ0YXRvcGkyMDkyQGJyaXR0ZWQuY29tIiwgInRva2VuIjogImFxZHNxcy0zZWU3YmRjNjdiNWQzNjZkNGI4MGJjYmIyMzVkOWYyOSJ9\'',1,'v',136),(113,'2021-07-26 00:02:18.229270','2021-07-26 00:02:18.229316','xiviyog713@dmsdmg.com','b\'eyJ1aWQiOiAxMzcsICJlbWFpbCI6ICJ4aXZpeW9nNzEzQGRtc2RtZy5jb20iLCAidG9rZW4iOiAiYXFkdm51LTYyNzE3ZDI2YTBkYTA5NzE1YzIxODdlMzE4Y2I2MTJiIn0=\'',1,'v',137),(115,'2021-07-26 06:16:01.439869','2021-07-26 06:16:01.439919','neclinga001@gmail.com','b\'eyJ1aWQiOiAxNDIsICJlbWFpbCI6ICJuZWNsaW5nYTAwMUBnbWFpbC5jb20iLCAidG9rZW4iOiAiYXFlY3lwLTk3OTFjOTYwZWE3NjIzMTE3MDRhMjRkODdiMGE3YzRmIn0=\'',1,'v',142);
/*!40000 ALTER TABLE `digiinsurance_emailverification` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-07-28 10:44:58
