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
-- Table structure for table `digiinsurance_userbankaccount`
--

DROP TABLE IF EXISTS `digiinsurance_userbankaccount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `digiinsurance_userbankaccount` (
  `id` int NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `modified_at` datetime(6) NOT NULL,
  `bank_name` varchar(255) DEFAULT NULL,
  `bank_branch` varchar(255) DEFAULT NULL,
  `account_name` varchar(255) DEFAULT NULL,
  `account_number` varchar(255) DEFAULT NULL,
  `is_preferred` tinyint(1) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `digiinsurance_userba_user_id_ec579916_fk_digiinsur` (`user_id`),
  CONSTRAINT `digiinsurance_userba_user_id_ec579916_fk_digiinsur` FOREIGN KEY (`user_id`) REFERENCES `digiinsurance_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digiinsurance_userbankaccount`
--

LOCK TABLES `digiinsurance_userbankaccount` WRITE;
/*!40000 ALTER TABLE `digiinsurance_userbankaccount` DISABLE KEYS */;
INSERT INTO `digiinsurance_userbankaccount` VALUES (1,'2021-07-15 01:14:30.507176','2021-07-21 06:13:37.292926','Bank of Berm','Valenzuela','Bermylle Razon','1111111111111111',1,2),(2,'2021-07-16 05:31:38.278597','2021-07-16 05:31:38.278640','wer','er','I Am Client','1234567890123456',0,102),(3,'2021-07-19 06:22:13.658771','2021-07-21 00:13:14.178286','A','BDO Ermita','asdfasl','1111111111111111',0,99),(4,'2021-07-19 06:23:39.853296','2021-07-19 06:28:10.526829','asdfasdf','asdfasdf','asdfasdfa','1231123123123111',1,99),(9,'2021-07-21 00:17:20.064195','2021-07-21 00:17:20.064234','Sglbhkk','Tondo','Dylftunnh','111111112',0,99),(10,'2021-07-21 05:42:47.546108','2021-07-21 06:13:37.219277','bank of Berm twos','manila','Bermylle two','097075151077',0,2),(11,'2021-07-21 06:38:10.510081','2021-07-23 05:33:48.452662','Bank','Philippines','Jacob Peralta','7842569145823677',1,103),(12,'2021-07-21 06:39:10.532796','2021-07-21 06:39:24.958004','DOB','Philippines','Jacob Peralta','5688964221587963',0,103),(13,'2021-07-21 07:35:59.870143','2021-07-21 08:04:41.536902','BDO','Ermita','Reena De Guzman','1234567890123456',1,111),(15,'2021-07-21 08:05:37.279820','2021-07-21 08:05:37.279862','BDO','Tondo','Reena De Guzman','1234567890123456',0,111),(17,'2021-07-22 02:04:22.236129','2021-07-22 02:06:53.004805','Unionbank','Makati','Maria Cruz','1234567812345677',1,114),(22,'2021-07-22 04:36:26.441012','2021-07-22 04:36:26.441055','wer','er','Allen Denopol','1234567890123456',0,121),(25,'2021-07-26 03:14:40.662078','2021-07-26 03:14:40.662124','BDO','Makati City','Carlo Geronimo Coste','0231111111111111',0,85),(28,'2021-07-26 06:32:38.732664','2021-07-26 06:45:14.491308','bod','London','Londonacc','1234567890',1,142),(30,'2021-07-26 06:46:21.610194','2021-07-26 06:46:21.610248','BDO','Shaw Blvd','Bronya Zaychik','6534534555543455',0,142);
/*!40000 ALTER TABLE `digiinsurance_userbankaccount` ENABLE KEYS */;
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

-- Dump completed on 2021-07-28 10:44:19
