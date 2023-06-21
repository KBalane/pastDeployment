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
-- Table structure for table `digiinsurance_tempbeneficiaries`
--

DROP TABLE IF EXISTS `digiinsurance_tempbeneficiaries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `digiinsurance_tempbeneficiaries` (
  `id` int NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `modified_at` datetime(6) NOT NULL,
  `beneficiary` int NOT NULL,
  `birthplace` varchar(32) NOT NULL,
  `country` varchar(32) NOT NULL,
  `birthday` date DEFAULT NULL,
  `nationality` varchar(32) NOT NULL,
  `beneficiary_address` varchar(255) NOT NULL,
  `request` varchar(255) DEFAULT NULL,
  `reason` varchar(255) NOT NULL,
  `first_name` varchar(32) NOT NULL,
  `middle_name` varchar(32) DEFAULT NULL,
  `last_name` varchar(32) NOT NULL,
  `relationship` varchar(16) DEFAULT NULL,
  `benefeciary_status` varchar(8) NOT NULL,
  `percentage_of_share` decimal(10,2) DEFAULT NULL,
  `user_policy_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `digiinsurance_tempbe_user_policy_id_72827acc_fk_digiinsur` (`user_policy_id`),
  CONSTRAINT `digiinsurance_tempbe_user_policy_id_72827acc_fk_digiinsur` FOREIGN KEY (`user_policy_id`) REFERENCES `digiinsurance_insureepolicy` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digiinsurance_tempbeneficiaries`
--

LOCK TABLES `digiinsurance_tempbeneficiaries` WRITE;
/*!40000 ALTER TABLE `digiinsurance_tempbeneficiaries` DISABLE KEYS */;
INSERT INTO `digiinsurance_tempbeneficiaries` VALUES (9,'2021-07-22 03:25:39.925663','2021-07-22 03:25:39.928246',7,'','','2021-07-22','','','N/A','test delete','name','name','name',NULL,'Pending',0.00,NULL),(10,'2021-07-22 05:36:04.307862','2021-07-22 05:36:04.311749',42,'Birmingham','Philippines','2020-06-15','Filipino','cxcfdgdf2 312','Add','another child, duh','Thomas','Shelby','Peralta','Son','PENDING',15.00,42),(11,'2021-07-22 05:36:04.361797','2021-07-22 05:36:04.363822',42,'Birmingham','Philippines','2020-06-15','Filipino','cxcfdgdf2 312','Add','another child, duh','Thomas','Shelby','Peralta','Son','PENDING',15.00,42),(14,'2021-07-22 15:21:06.067291','2021-07-22 15:21:06.069991',18,'qwertyuil','phil','1111-11-11','fil','qweryerytuoui','Add','qwertyuiop[]o\\','qwerturyi','qertrstduoyoui','sdtiogiho','qwresrfyiop','PENDING',20.00,18),(27,'2021-07-23 06:31:17.132851','2021-07-23 06:31:17.134966',17,'MCU','Sokovia','1978-12-12','Sokovian','Sokovia, Sokovia','Add','Add this beneficiary','Wanda','','Maximoff','Mother','PENDING',30.00,17),(28,'2021-07-23 06:33:11.180012','2021-07-23 06:33:11.181397',17,'MCU','Sokovia','1978-12-12','Sokovian','Sokovia, Sokovia','Add','Add this beneficiary','Wanda','','Maximoff','Mother','PENDING',30.00,17),(33,'2021-07-23 06:46:19.511005','2021-07-23 06:46:19.512087',10,'Terra Mundo','Philippines','2005-12-12','Filipino','Terra Mundo','Add','Add this beneficiary','Alexandra','Miranda','Trese','Daughter','PENDING',35.00,10),(55,'2021-07-25 23:56:59.219075','2021-07-25 23:56:59.221856',52,'Sample birthplace','Phil','1111-11-11','Filipino','sample saddressssssssssssssssssss','Add','qwertyuiop','Sample','Sample','Sample','Sample','PENDING',15.00,52),(56,'2021-07-25 23:56:59.324872','2021-07-25 23:56:59.329894',52,'Sample birthplace','Phil','1111-11-11','Filipino','sample saddressssssssssssssssssss','Add','qwertyuiop','Sample','Sample','Sample','Sample','PENDING',15.00,52),(57,'2021-07-26 06:30:42.253768','2021-07-26 06:30:42.253812',23,'birthplace','Philippines','1999-03-01','birthplace','525 B M. Gonzaga St. Brgy. Hagdang Bato Itaas','N/A','edit lods','Neill Elijah','Cortez','Linga','yaboiiiii','Pending',100.00,61),(58,'2021-07-26 21:31:26.337127','2021-07-26 21:31:26.337169',24,'Sample birthplace','Phil','1111-11-11','Filipino','qwertyuiop[','N/A','q234567890-','Sample','Sample','Sample','Sample','Pending',70.00,62),(59,'2021-07-26 21:34:32.675037','2021-07-26 21:34:32.677874',63,'Sample birthplace','Phil','1111-11-11','Filipino','1234567890-','Add','qwertyuiop[','Sample','Sample','Sample','Sample','PENDING',70.00,63),(60,'2021-07-26 21:49:16.699658','2021-07-26 21:49:16.700969',16,'','','1111-11-11','','','N/A','qwertyuiop','name','name','name',NULL,'Pending',0.00,NULL),(61,'2021-07-27 07:38:40.282070','2021-07-27 07:38:40.384833',22,'','','1999-01-26','','','N/A','Went to Sunlife','name','name','name',NULL,'Pending',0.00,NULL);
/*!40000 ALTER TABLE `digiinsurance_tempbeneficiaries` ENABLE KEYS */;
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

-- Dump completed on 2021-07-28 10:45:01
