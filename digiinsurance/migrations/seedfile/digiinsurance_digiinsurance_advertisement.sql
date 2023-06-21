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
-- Table structure for table `digiinsurance_advertisement`
--

DROP TABLE IF EXISTS `digiinsurance_advertisement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `digiinsurance_advertisement` (
  `id` int NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `modified_at` datetime(6) NOT NULL,
  `Type` varchar(30) DEFAULT NULL,
  `Link` varchar(255) DEFAULT NULL,
  `Title` varchar(30) NOT NULL,
  `Description` longtext NOT NULL,
  `Publish_Date` date NOT NULL,
  `Expiration_Date` date NOT NULL,
  `Photo` varchar(100) DEFAULT NULL,
  `Status` varchar(20) DEFAULT NULL,
  `Policy_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `digiinsurance_advert_Policy_id_89b6f028_fk_digiinsur` (`Policy_id`),
  CONSTRAINT `digiinsurance_advert_Policy_id_89b6f028_fk_digiinsur` FOREIGN KEY (`Policy_id`) REFERENCES `digiinsurance_policy` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=85 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digiinsurance_advertisement`
--

LOCK TABLES `digiinsurance_advertisement` WRITE;
/*!40000 ALTER TABLE `digiinsurance_advertisement` DISABLE KEYS */;
INSERT INTO `digiinsurance_advertisement` VALUES (1,'2021-07-21 01:26:28.446743','2021-07-26 06:28:45.716550','link-article','https://screenrant.com/loki-sylvie-nexus-event-theory-explained/','Loki to Sylvie’s Nexus Event','Loki episode 4 may have subtly revealed the nexus event that forced Sophia Di Martino\'s Lady Loki to go on the run in the Marvel Cinematic Universe.','2021-07-21','2022-07-21','','Active',3),(74,'2021-07-23 04:58:12.564807','2021-07-23 04:58:12.564807','Promossss','screenrant.com/loki-sylvie-nexus-event-theory-explained/','Loki to','Loki episode 4 may have subtly revealed the nexus event that forced Sophia Di Martino\'s Lady Loki to go on the run in the Marvel Cinematic Universe.','2021-07-21','2022-07-21','','Active',2),(75,'2021-07-23 04:58:20.668126','2021-07-23 04:58:20.668126','Promossss','screenrant.com/loki-sylvie-nexus-event-theory-explained/','Loki tasdasdasdo','Loki episode 4 may have subtly revealed the nexus event that forced Sophia Di Martino\'s Lady Loki to go on the run in the Marvel Cinematic Universe.','2021-07-21','2022-07-21','','Active',2),(76,'2021-07-23 04:58:34.041172','2021-07-23 04:58:34.041172','Promossss','screenrant.com/loki-sylvie-nexus-event-theory-explained/','Loki tasdasasdasdsadasdasdasdd','Loki episode 4 may have subtly revealed the nexus event that forced Sophia Di Martino\'s Lady Loki to go on the run in the Marvel Cinematic Universe.','2021-07-21','2022-07-21','','Active',2),(77,'2021-07-23 04:58:42.246434','2021-07-23 04:58:42.246434','Promossss','screenrant.com/loki-sylvie-nexus-event-theory-explained/','Loki tasdasasdasdsadasdasdasdd','Loki episode 4 may have subtly revealed the nexus event that forced Sophia Di Martino\'s Lady Loki to go on the run in the Marvel Cinematic Universe.','2021-07-21','2022-07-21','','Active',2),(79,'2021-07-23 05:17:41.834283','2021-07-23 05:17:41.834283','Promossss','screenrant.com/loki-sylvie-nexus-event-theory-explained/','Loki to Sylvie’s Nexus Event','Loki episode 4 may have subtly revealed the nexus event that forced Sophia Di Martino\'s Lady Loki to go on the run in the Marvel Cinematic Universe.','2021-07-21','2022-07-21','','Active',2),(80,'2021-07-23 05:21:26.918572','2021-07-23 05:21:26.918729','Promossss','screenrant.com/loki-sylvie-nexus-event-theory-explained/','Loki to Sylvie’s Nexus Event','Loki episode 4 may have subtly revealed the nexus event that forced Sophia Di Martino\'s Lady Loki to go on the run in the Marvel Cinematic Universe.','2021-07-21','2022-07-21','','Active',2),(82,'2021-07-23 08:17:07.616137','2021-07-23 08:17:07.616137','Promo','screenrant.com/loki-sylvie-nexus-event-theory-explained/','Loki to Sylvie’s Nexus Event','Loki is cute episode 4 may have subtly revealed the nexus event that forced Sophia Di Martino\'s Lady Loki to go on the run in the Marvel Cinematic Universe.','2021-07-21','2022-07-21','','Active',2),(83,'2021-07-26 05:53:08.564306','2021-07-26 05:53:31.940898','link-article','https://screenrant.com/falcon-winter-soldier-mcu-theories-debunked/','Loki to Sylvie’s Nexus Event','jhebfu','2021-07-30','2022-07-29','','Active',3),(84,'2021-07-26 05:54:21.299673','2021-07-26 05:55:29.332641','Promo',NULL,'VanKeith Policy','ejhrfbauegyb','2021-07-30','2022-07-30','promos/VanKeith_Policy.jpg','Inactive',2);
/*!40000 ALTER TABLE `digiinsurance_advertisement` ENABLE KEYS */;
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

-- Dump completed on 2021-07-28 10:44:18
