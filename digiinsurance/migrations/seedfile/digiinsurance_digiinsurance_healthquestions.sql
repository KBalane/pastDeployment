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
-- Table structure for table `digiinsurance_healthquestions`
--

DROP TABLE IF EXISTS `digiinsurance_healthquestions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `digiinsurance_healthquestions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `modified_at` datetime(6) NOT NULL,
  `choices` json DEFAULT NULL,
  `correct_answer` varchar(256) DEFAULT NULL,
  `question` varchar(256) DEFAULT NULL,
  `question_type` varchar(20) NOT NULL,
  `policy_id_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `digiinsurance_health_policy_id_id_f9d637f0_fk_digiinsur` (`policy_id_id`),
  CONSTRAINT `digiinsurance_health_policy_id_id_f9d637f0_fk_digiinsur` FOREIGN KEY (`policy_id_id`) REFERENCES `digiinsurance_policy` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digiinsurance_healthquestions`
--

LOCK TABLES `digiinsurance_healthquestions` WRITE;
/*!40000 ALTER TABLE `digiinsurance_healthquestions` DISABLE KEYS */;
INSERT INTO `digiinsurance_healthquestions` VALUES (1,'2021-07-15 05:32:52.665340','2021-07-15 05:32:52.665340','[{\"option1\": \"1\", \"option2\": \"2\"}]','2','What\'s 1 + 1?','MultipleChoice',3),(2,'2021-07-15 05:59:00.440685','2021-07-15 09:23:38.759562','[]',NULL,'What\'s your name?','MultilineText',8),(3,'2021-07-15 06:07:34.496827','2021-07-15 09:23:38.821704','[]',NULL,'How old are you?','MultilineText',8),(4,'2021-07-15 06:07:34.559601','2021-07-15 09:23:38.882877','[{\"name\": \"Yes\"}, {\"name\": \"No\"}]','No','Have you lost weight during the past twelve months?','MultipleChoice',8),(5,'2021-07-15 06:07:34.831869','2021-07-15 09:23:38.939888','[{\"name\": \"Yes\"}, {\"name\": \"No\"}]','No','Have you been diagnosed of a severe illness?','MultipleChoice',8),(6,'2021-07-16 05:26:31.848587','2021-07-16 05:26:31.848626','[]',NULL,'How old are you?','MultilineText',9),(7,'2021-07-21 05:32:00.184913','2021-07-21 05:32:00.184953','[{\"name\": \"Yes\"}, {\"name\": \"No\"}, {\"name\": \"Maybe\"}]','No','Have you been diagnosed of a severe illness?','MultipleChoice',8),(8,'2021-07-21 08:17:33.818345','2021-07-21 08:18:58.359049','[]',NULL,'What is your name?','MultilineText',10),(9,'2021-07-21 08:17:33.890562','2021-07-21 08:18:58.419246','[{\"name\": \"A\"}, {\"name\": \"B\"}]','A','A or B?','MultipleChoice',10),(10,'2021-07-22 01:11:51.168190','2021-07-22 01:11:51.168231','[]',NULL,'How old are you?','MultilineText',11),(11,'2021-07-22 01:53:06.908058','2021-07-22 01:53:06.908099','[]',NULL,'Lorem ipsum dolor sit amet, consectetur adipiscing elit.','MultilineText',12),(12,'2021-07-22 02:03:29.231458','2021-07-22 02:11:01.509506','[]',NULL,'Lorem ipsum dolor sit amet, consectetur adipiscing elit.','MultilineText',13),(13,'2021-07-22 02:17:25.125574','2021-07-22 02:17:25.125619','[]',NULL,'How old are you?','MultilineText',14),(16,'2021-07-26 05:33:43.462104','2021-07-26 05:37:22.568017','[{\"name\": \"B\"}, {\"name\": \"A\"}]','B','A or B','MultipleChoice',17),(17,'2021-07-26 05:37:22.590302','2021-07-26 05:37:22.590366','[{\"name\": \"ergqrgerg\"}, {\"name\": \"ergerge\"}, {\"name\": \"egerg\"}]','egerg','ehbugrgq','MultipleChoice',17);
/*!40000 ALTER TABLE `digiinsurance_healthquestions` ENABLE KEYS */;
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

-- Dump completed on 2021-07-28 10:44:12
