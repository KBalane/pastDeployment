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
-- Table structure for table `digiinsurance_beneficiaries`
--

DROP TABLE IF EXISTS `digiinsurance_beneficiaries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `digiinsurance_beneficiaries` (
  `id` int NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `modified_at` datetime(6) NOT NULL,
  `first_name` varchar(32) NOT NULL,
  `middle_name` varchar(32) DEFAULT NULL,
  `last_name` varchar(32) NOT NULL,
  `relationship` varchar(16) DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `birthplace` varchar(32) NOT NULL,
  `nationality` varchar(32) NOT NULL,
  `country` varchar(32) NOT NULL,
  `beneficiary_address` varchar(255) NOT NULL,
  `benefeciary_status` varchar(8) NOT NULL,
  `request_type` varchar(8) NOT NULL,
  `percentage_of_share` decimal(10,2) DEFAULT NULL,
  `user_policy_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `digiinsurance_benefi_user_policy_id_248f83d9_fk_digiinsur` (`user_policy_id`),
  CONSTRAINT `digiinsurance_benefi_user_policy_id_248f83d9_fk_digiinsur` FOREIGN KEY (`user_policy_id`) REFERENCES `digiinsurance_insureepolicy` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digiinsurance_beneficiaries`
--

LOCK TABLES `digiinsurance_beneficiaries` WRITE;
/*!40000 ALTER TABLE `digiinsurance_beneficiaries` DISABLE KEYS */;
INSERT INTO `digiinsurance_beneficiaries` VALUES (1,'2021-07-16 01:49:45.997672','2021-07-16 02:19:56.090942','James','Buchanan','Barnes','Brother','2001-12-12','MCU','American','United States','312 Osaka Shiyahahuhaji','APPROVED','Update',70.00,10),(3,'2021-07-16 08:06:21.079920','2021-07-16 08:06:21.079958','James','Buchanan','Barnes','Brother','1989-03-10','MCU','American','United States','United States','APPROVED','Update',75.00,17),(5,'2021-07-21 03:23:53.141903','2021-07-21 03:23:53.141944','bermylle','johgn','razon','Father','2021-06-28','manila city','filipino','Philippines','asdadasdasdasdasdasdasd','Pending','Add',60.00,24),(9,'2021-07-22 04:31:48.964017','2021-07-22 04:31:48.964078','McClane','Santiago','Peralta','Son','2017-06-13','New York','Filipino','Philippines','cxcfdgdf2 312 this is a legit address thank u','APPROVED','Update',70.00,42),(11,'2021-07-22 11:37:12.629263','2021-07-22 11:37:12.629263','Angelu',NULL,'Garingo','qertyuio',NULL,'Birthplace','Nationality','Philippines','qqqqqqqqqqqqqqqqqqqq','APPROVED','ADD',55.00,18),(14,'2021-07-23 07:20:13.927260','2021-07-23 07:20:13.930108','Alexandra','Miranda','Trese','Daughter','2005-12-12','Terra Mundo','Filipino','Philippines','Terra Mundo','APPROVED','Add',25.00,10),(15,'2021-07-23 08:28:20.127651','2021-07-23 08:28:20.130091','Alexandra','Miranda','Trese','Daughter','2005-12-12','Terra Mundo','Filipino','Philippines','uayefgiqyer','APPROVED','Add',20.00,17),(16,'2021-07-25 23:01:04.142695','2021-07-25 23:01:04.142756','Sample','Sample','Sample','Sample','1111-11-11','Sample birthplace','Filipino','Phil','Sample address Sample address Sample address','PENDING','Delete',80.00,52),(17,'2021-07-26 05:41:14.829882','2021-07-26 05:41:14.835142','Sample','Sample','Sample','Sample','1111-11-11','Sample birthplace','Filipino','Phil','qwertuopio[piuyte','APPROVED','Add',15.00,52),(18,'2021-07-26 06:21:33.321079','2021-07-26 06:21:33.321122','Neill Elijah','Cortez','Linga','yaboi','1996-01-30','birthpalce','birthpalce','Philippines','525 B M. Gonzaga St. Brgy. Hagdang Bato Itaas','Pending','Add',50.00,58),(19,'2021-07-26 06:21:33.394866','2021-07-26 06:21:33.394911','Neill Elijahg','Cgg','Linga','yaboiiiii','2006-01-31','birthpalce','birthpalce','Philippines','525 B M. Gonzaga St. Brgy. Hagdang Bato Itaas','Pending','Add',50.00,58),(20,'2021-07-26 06:21:33.727231','2021-07-26 06:21:33.727274','Neill Elijahg','Cgg','Linga','yaboiiiii','2006-01-31','birthpalce','birthpalce','Philippines','525 B M. Gonzaga St. Brgy. Hagdang Bato Itaas','Pending','Add',50.00,59),(21,'2021-07-26 06:21:33.727519','2021-07-26 06:21:33.727565','Neill Elijah','Cortez','Linga','yaboi','1996-01-30','birthpalce','birthpalce','Philippines','525 B M. Gonzaga St. Brgy. Hagdang Bato Itaas','Pending','Add',50.00,59),(22,'2021-07-26 06:23:26.655342','2021-07-26 06:23:26.655388','Neill Elijah','Cortez','Linga','yaboiiiii','1999-01-26','birthpalce','birthpalce','Philippines','525 B M. Gonzaga St. Brgy. Hagdang Bato Itaas','PENDING','Delete',100.00,60),(23,'2021-07-26 06:25:11.349249','2021-07-26 06:25:11.349309','Neill Elijah','Cyr','Linga','yaboiiiii','1999-03-01','birthpalce','birthpalce','Philippines','525 B M. Gonzaga St. Brgy. Hagdang Bato Itaas','Pending','Update',55.00,61),(24,'2021-07-26 21:02:42.522686','2021-07-26 21:02:42.522746','Sample','Sample','Sample','Sample','1111-11-11','Sample birthplace','Filipino','Phil','qwertyuiop[','Pending','Update',70.00,62),(25,'2021-07-26 21:02:44.761136','2021-07-26 21:02:44.761193','Sample','Sample','Sample','Sample','1111-11-11','Sample birthplace','Filipino','Phil','qwertyuiop[','Pending','Add',70.00,63),(26,'2021-07-26 21:30:30.403995','2021-07-26 21:30:30.404040','Sample','Sample','Sample','Sample','1111-11-11','Sample birthplace','Filipino','Phil','1234567890','Pending','Add',100.00,64);
/*!40000 ALTER TABLE `digiinsurance_beneficiaries` ENABLE KEYS */;
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

-- Dump completed on 2021-07-28 10:44:24
