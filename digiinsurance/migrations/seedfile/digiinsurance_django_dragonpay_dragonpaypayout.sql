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
-- Table structure for table `django_dragonpay_dragonpaypayout`
--

DROP TABLE IF EXISTS `django_dragonpay_dragonpaypayout`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_dragonpay_dragonpaypayout` (
  `id` varchar(40) NOT NULL,
  `refno` varchar(8) DEFAULT NULL,
  `user_id` varchar(40) DEFAULT NULL,
  `user_name` varchar(64) DEFAULT NULL,
  `processor_id` varchar(8) DEFAULT NULL,
  `processor_detail` varchar(32) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `mobile` varchar(32) DEFAULT NULL,
  `amount` decimal(8,2) NOT NULL,
  `description` varchar(128) NOT NULL,
  `currency` varchar(3) NOT NULL,
  `status` varchar(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `modified_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_dragonpay_dragonpaypayout`
--

LOCK TABLES `django_dragonpay_dragonpaypayout` WRITE;
/*!40000 ALTER TABLE `django_dragonpay_dragonpaypayout` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_dragonpay_dragonpaypayout` ENABLE KEYS */;
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

-- Dump completed on 2021-07-28 10:45:13
