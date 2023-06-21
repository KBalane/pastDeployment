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
-- Table structure for table `blockchain_certificateaddress`
--

DROP TABLE IF EXISTS `blockchain_certificateaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `blockchain_certificateaddress` (
  `id` int NOT NULL AUTO_INCREMENT,
  `address` varchar(42) NOT NULL,
  `timestamp` datetime(6) DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  `available` tinyint(1) NOT NULL,
  `number` varchar(32) DEFAULT NULL,
  `insuree_id` int DEFAULT NULL,
  `insureePolicy_id` int DEFAULT NULL,
  `policy_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `insureePolicy_id` (`insureePolicy_id`),
  KEY `blockchain_certifica_insuree_id_a131d051_fk_digiinsur` (`insuree_id`),
  KEY `blockchain_certifica_policy_id_f88bc643_fk_digiinsur` (`policy_id`),
  CONSTRAINT `blockchain_certifica_insuree_id_a131d051_fk_digiinsur` FOREIGN KEY (`insuree_id`) REFERENCES `digiinsurance_insuree` (`user_id`),
  CONSTRAINT `blockchain_certifica_insureePolicy_id_65da2a69_fk_digiinsur` FOREIGN KEY (`insureePolicy_id`) REFERENCES `digiinsurance_insureepolicy` (`id`),
  CONSTRAINT `blockchain_certifica_policy_id_f88bc643_fk_digiinsur` FOREIGN KEY (`policy_id`) REFERENCES `digiinsurance_policy` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blockchain_certificateaddress`
--

LOCK TABLES `blockchain_certificateaddress` WRITE;
/*!40000 ALTER TABLE `blockchain_certificateaddress` DISABLE KEYS */;
/*!40000 ALTER TABLE `blockchain_certificateaddress` ENABLE KEYS */;
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

-- Dump completed on 2021-07-28 10:45:00
