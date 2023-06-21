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
-- Table structure for table `digiinsurance_company`
--

DROP TABLE IF EXISTS `digiinsurance_company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `digiinsurance_company` (
  `id` int NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `modified_at` datetime(6) NOT NULL,
  `archived` tinyint(1) NOT NULL,
  `archived_at` datetime(6) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `address` varchar(128) DEFAULT NULL,
  `city` varchar(64) DEFAULT NULL,
  `province` varchar(64) DEFAULT NULL,
  `region` varchar(64) DEFAULT NULL,
  `zip_code` varchar(4) DEFAULT NULL,
  `gps_long` decimal(23,20) DEFAULT NULL,
  `gps_lat` decimal(23,20) DEFAULT NULL,
  `country` varchar(64) DEFAULT NULL,
  `website` varchar(128) DEFAULT NULL,
  `country_code` varchar(5) DEFAULT NULL,
  `area_code` varchar(5) DEFAULT NULL,
  `mobile_number` varchar(16) DEFAULT NULL,
  `phone_number` varchar(16) DEFAULT NULL,
  `email` varchar(128) DEFAULT NULL,
  `logo` varchar(100) DEFAULT NULL,
  `cover` varchar(100) DEFAULT NULL,
  `domain` varchar(32) DEFAULT NULL,
  `dragonpay_merchant_id` varchar(32) DEFAULT NULL,
  `primary_color` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digiinsurance_company`
--

LOCK TABLES `digiinsurance_company` WRITE;
/*!40000 ALTER TABLE `digiinsurance_company` DISABLE KEYS */;
INSERT INTO `digiinsurance_company` VALUES (1,'2021-07-15 01:17:50.959756','2021-07-15 01:17:50.960988',1,'2021-07-15 01:15:47.476000','asdasdasd','asdasdasdasd','Caloocan','PH-00','ARMM','2800',412.41200000000000000000,412.41200000000000000000,'PH','string','63','1440','string','string','string','','','string','string','string'),(2,'2021-07-15 02:35:47.722573','2021-07-15 02:35:47.772439',0,NULL,'Terrasave','Racoon City','Las Pinas','PH-BEN','NCR','2809',12.48181000000000000000,23.81923000000000000000,'Philippines','terrasave.com','+63','27381','283918517629','28198931771','terrasave.example.com','','','terrasave','12389019023','#F90037');
/*!40000 ALTER TABLE `digiinsurance_company` ENABLE KEYS */;
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

-- Dump completed on 2021-07-28 10:44:27
