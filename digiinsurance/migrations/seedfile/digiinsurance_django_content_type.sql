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
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(9,'authtoken','token'),(46,'authtoken','tokenproxy'),(44,'blockchain','certificateaddress'),(43,'blockchain','contract'),(45,'blockchain','transaction'),(42,'blockchain','wallet'),(4,'contenttypes','contenttype'),(35,'digiinsurance','advertisement'),(11,'digiinsurance','auditentry'),(34,'digiinsurance','bankaccount'),(33,'digiinsurance','beneficiaries'),(32,'digiinsurance','claims'),(12,'digiinsurance','company'),(31,'digiinsurance','companyconfig'),(13,'digiinsurance','companyinvestmenttype'),(30,'digiinsurance','companyrequirements'),(29,'digiinsurance','companysocials'),(28,'digiinsurance','documenttemplate'),(27,'digiinsurance','emailverification'),(26,'digiinsurance','favourites'),(14,'digiinsurance','healthquestions'),(25,'digiinsurance','healthquestionsanswers'),(19,'digiinsurance','insuree'),(39,'digiinsurance','insureepaymentdetails'),(15,'digiinsurance','insureepolicy'),(24,'digiinsurance','insureepolicydocs'),(16,'digiinsurance','payout'),(17,'digiinsurance','policy'),(23,'digiinsurance','policycalculator'),(22,'digiinsurance','policyrequirements'),(18,'digiinsurance','product'),(38,'digiinsurance','staff'),(21,'digiinsurance','tempbeneficiaries'),(37,'digiinsurance','transaction'),(10,'digiinsurance','user'),(20,'digiinsurance','userbankaccount'),(36,'digiinsurance','userinvestment'),(6,'django_dragonpay','dragonpaypayout'),(7,'django_dragonpay','dragonpaypayoutuser'),(8,'django_dragonpay','dragonpaytransaction'),(40,'kyc','templateid'),(41,'kyc','userid'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
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

-- Dump completed on 2021-07-28 10:44:09
