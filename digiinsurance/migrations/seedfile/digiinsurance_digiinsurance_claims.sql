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
-- Table structure for table `digiinsurance_claims`
--

DROP TABLE IF EXISTS `digiinsurance_claims`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `digiinsurance_claims` (
  `id` int NOT NULL AUTO_INCREMENT,
  `modified_at` datetime(6) NOT NULL,
  `bank_name` varchar(256) DEFAULT NULL,
  `claim_type` varchar(30) DEFAULT NULL,
  `claim_docs` varchar(100) NOT NULL,
  `claims_refno` varchar(256) DEFAULT NULL,
  `amount` decimal(8,2) NOT NULL,
  `UserPolicy_id_id` int NOT NULL,
  `claim_status` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `digiinsurance_claims_UserPolicy_id_id_c0ad0b2a_fk_digiinsur` (`UserPolicy_id_id`),
  CONSTRAINT `digiinsurance_claims_UserPolicy_id_id_c0ad0b2a_fk_digiinsur` FOREIGN KEY (`UserPolicy_id_id`) REFERENCES `digiinsurance_insureepolicy` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digiinsurance_claims`
--

LOCK TABLES `digiinsurance_claims` WRITE;
/*!40000 ALTER TABLE `digiinsurance_claims` DISABLE KEYS */;
INSERT INTO `digiinsurance_claims` VALUES (1,'2021-07-16 05:32:01.926188','wer','','timezone.now','2021-07-16',0.00,11,'Pending'),(2,'2021-07-16 09:51:37.342513','foo','bar','timezone.now','2021-07-16',0.00,12,'Pending'),(3,'2021-07-16 10:04:59.510977','bdo','tezt','timezone.now','2021-07-16',0.00,13,'Pending'),(4,'2021-07-19 07:22:21.529803','ASDBank','Cash','users/None.pdf','2021-07-19',69000.00,12,'denied'),(5,'2021-07-19 07:26:17.472327','ASDBank_2','Cash','users/None_wrXKfwr.pdf','2021-07-19',90000.00,13,'approved'),(8,'2021-07-22 03:32:53.650427','wer','','timezone.now','2021-07-22',0.00,11,'Pending'),(9,'2021-07-22 04:36:33.459518','wer','','timezone.now','2021-07-22',0.00,40,'Pending'),(10,'2021-07-22 04:40:00.152778','wer','','timezone.now','2021-07-22',0.00,40,'Pending'),(11,'2021-07-22 05:55:07.170024','Banks','','timezone.now','2021-07-22',0.00,42,'Pending'),(12,'2021-07-22 06:29:07.317688','Banks','life','users/None_CIiqPBI.jpg','2021-07-22',0.00,43,'Pending'),(13,'2021-07-22 07:45:13.929004','VK Bank','Cash','users/None_wkA80lV.pdf','2021-07-22',69.00,1,'denied'),(14,'2021-07-22 07:46:25.037481','ASDBank99','Cash','timezone.now','2021-07-22',0.05,42,'pending'),(15,'2021-07-22 07:46:25.930161','ASDBank99','Cash','timezone.now','2021-07-22',0.05,42,'pending'),(16,'2021-07-23 04:24:06.520087','ASDBank1999','Cash','users/None_AKGGSYi.pdf','2021-07-23',0.00,46,'approved'),(17,'2021-07-23 05:00:51.380653','BDO','health','users/None_uLzQzZZ.pdf','2021-07-23',0.00,32,'Pending'),(18,'2021-07-23 06:44:25.117346','Asd_bankk','Cash_2','timezone.now','2021-07-23',0.00,15,'pending'),(19,'2021-07-23 06:44:30.462787','Asd_bankk','Cash_2','timezone.now','2021-07-23',0.00,15,'pending'),(20,'2021-07-23 06:44:33.866051','Asd_bankk','Cash_2','timezone.now','2021-07-23',0.00,15,'pending'),(21,'2021-07-23 06:44:34.492605','Asd_bankk','Cash_2','timezone.now','2021-07-23',0.00,15,'pending'),(22,'2021-07-23 06:44:37.989776','Asd_bankk','Cash_2','timezone.now','2021-07-23',0.00,15,'pending'),(23,'2021-07-23 06:44:55.871652','Asd_bankk','Cash_2','timezone.now','2021-07-23',0.00,15,'pending'),(24,'2021-07-23 06:46:07.459201','Asd_bankk','Cash_2','timezone.now','2021-07-23',0.00,15,'pending'),(25,'2021-07-23 06:57:57.837858','BlankBank','Life','timezone.now','2021-07-23',0.00,11,'pending'),(26,'2021-07-23 06:58:00.110989','BlankBank','Life','timezone.now','2021-07-23',0.00,11,'pending'),(27,'2021-07-23 06:58:00.970945','BlankBank','Life','timezone.now','2021-07-23',0.00,11,'pending'),(28,'2021-07-23 06:58:01.134857','BlankBank','Life','timezone.now','2021-07-23',0.00,11,'pending'),(29,'2021-07-23 06:58:01.445663','BlankBank','Life','timezone.now','2021-07-23',0.00,11,'pending'),(30,'2021-07-23 06:58:01.575849','BlankBank','Life','timezone.now','2021-07-23',0.00,11,'pending'),(31,'2021-07-23 06:58:42.217648','BlankBank','Life','timezone.now','2021-07-23',0.00,11,'denied'),(32,'2021-07-23 07:02:30.349193','BlankBank','Life','timezone.now','2021-07-23',0.00,1,'denied'),(33,'2021-07-23 07:02:32.638793','BlankBank','Life','timezone.now','2021-07-23',0.00,1,'denied'),(34,'2021-07-23 07:02:33.873634','BlankBank','Life','timezone.now','2021-07-23',0.00,1,'denied'),(35,'2021-07-23 07:02:54.746657','BlankBank','Life','timezone.now','2021-07-23',0.00,1,'denied'),(36,'2021-07-23 07:02:57.631177','BlankBank','Life','timezone.now','2021-07-23',0.00,1,'denied'),(37,'2021-07-23 07:04:14.105671','BlankBank','Life','timezone.now','2021-07-23',0.00,1,'denied'),(38,'2021-07-23 07:20:50.884301','BlankBank','Life','timezone.now','2021-07-23',0.00,1,'denied'),(39,'2021-07-23 07:21:08.990028','Test01Bank','Life','timezone.now','2021-07-23',0.00,1,'denied'),(40,'2021-07-23 07:21:36.960228','Test01Bank','Life','timezone.now','2021-07-23',0.00,1,'approved'),(41,'2021-07-23 07:21:59.943120','Test01Bank','Life','timezone.now','2021-07-23',0.00,1,'pending'),(42,'2021-07-23 07:27:00.136929','Test01Bank','Life','timezone.now','2021-07-23',0.00,1,'pending'),(43,'2021-07-23 07:28:03.644201','BlankBank','Life','timezone.now','2021-07-23',0.00,1,'denied'),(44,'2021-07-23 07:31:53.532221','BlankBank','Life','timezone.now','2021-07-23',0.00,1,'denied'),(45,'2021-07-23 07:43:57.560771','BlankBank','Life','timezone.now','2021-07-23',0.00,1,'denied'),(46,'2021-07-23 07:44:20.229150','BlankBank','Life','timezone.now','2021-07-23',0.00,1,'denied'),(47,'2021-07-23 07:45:13.294124','BlankBank','Life','timezone.now','2021-07-23',0.00,11,'denied'),(48,'2021-07-23 07:46:21.293849','BlankBank','Life','timezone.now','2021-07-23',0.00,11,'denied'),(49,'2021-07-23 08:31:47.121732','Test01','Life','timezone.now','2021-07-23',0.00,11,'pending'),(50,'2021-07-23 08:32:18.529974','Test01','Life','timezone.now','2021-07-23',0.00,11,'denied'),(51,'2021-07-23 08:34:05.762426','BlankBank','Life','timezone.now','2021-07-23',0.00,1,'denied'),(52,'2021-07-23 08:34:24.551148','BlankBank','Life','timezone.now','2021-07-23',0.00,1,'approved'),(53,'2021-07-24 03:56:51.530542','A','','timezone.now','2021-07-22',0.00,35,'Pending'),(54,'2021-07-26 03:14:50.502784','BDO','','timezone.now','2021-07-26',0.00,10,'Pending'),(55,'2021-07-26 06:33:49.682049','UK Bank','','timezone.now','2021-07-26',0.00,61,'Pending');
/*!40000 ALTER TABLE `digiinsurance_claims` ENABLE KEYS */;
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

-- Dump completed on 2021-07-28 10:44:55
