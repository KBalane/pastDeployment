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
-- Table structure for table `digiinsurance_insureepolicy`
--

DROP TABLE IF EXISTS `digiinsurance_insureepolicy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `digiinsurance_insureepolicy` (
  `id` int NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `modified_at` datetime(6) NOT NULL,
  `status` varchar(10) NOT NULL,
  `premium_amount_due` decimal(10,2) NOT NULL,
  `premium_date_due` date DEFAULT NULL,
  `premium_last_paid` decimal(10,2) NOT NULL,
  `premium_last_date` date DEFAULT NULL,
  `policy_type` varchar(10) NOT NULL,
  `policy_type2` varchar(10) NOT NULL,
  `active_premium_interval` varchar(11) NOT NULL,
  `Currency` varchar(3) DEFAULT NULL,
  `policy_id` int NOT NULL,
  `insuree_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `digiinsurance_insure_policy_id_6e695070_fk_digiinsur` (`policy_id`),
  KEY `digiinsurance_insure_insuree_id_886072d1_fk_digiinsur` (`insuree_id`),
  CONSTRAINT `digiinsurance_insure_insuree_id_886072d1_fk_digiinsur` FOREIGN KEY (`insuree_id`) REFERENCES `digiinsurance_insuree` (`user_id`),
  CONSTRAINT `digiinsurance_insure_policy_id_6e695070_fk_digiinsur` FOREIGN KEY (`policy_id`) REFERENCES `digiinsurance_policy` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digiinsurance_insureepolicy`
--

LOCK TABLES `digiinsurance_insureepolicy` WRITE;
/*!40000 ALTER TABLE `digiinsurance_insureepolicy` DISABLE KEYS */;
INSERT INTO `digiinsurance_insureepolicy` VALUES (1,'2021-07-15 01:57:28.833002','2021-07-15 01:57:28.833002','paid',100000.00,'2021-07-15',100000.00,'2021-07-15','life','lite','one_time','PHP',2,1),(10,'2021-07-16 01:49:45.899739','2021-07-16 01:49:45.899801','Active',12500.00,'2021-07-16',12500.00,'2021-07-16','home','basic','quarterly','PHP',8,85),(11,'2021-07-16 05:27:19.460427','2021-07-16 05:27:19.460474','Active',2500.00,'2021-07-16',2500.00,'2021-07-16','health','standard','quarterly','PHP',9,102),(12,'2021-07-16 05:27:29.928224','2021-07-16 05:27:29.928262','Active',2500.00,'2021-07-16',2500.00,'2021-07-16','health','standard','quarterly','PHP',9,102),(13,'2021-07-16 05:27:35.341306','2021-07-16 05:27:35.341346','Active',2500.00,'2021-07-16',2500.00,'2021-07-16','health','standard','quarterly','PHP',9,102),(14,'2021-07-16 05:28:29.395516','2021-07-16 05:28:29.395562','Active',2500.00,'2021-07-16',2500.00,'2021-07-16','health','standard','quarterly','PHP',9,102),(15,'2021-07-16 05:30:18.172648','2021-07-16 05:30:18.172689','Active',2500.00,'2021-07-16',2500.00,'2021-07-16','health','standard','quarterly','PHP',9,102),(16,'2021-07-16 05:30:21.220503','2021-07-16 05:30:21.220544','Active',2500.00,'2021-07-16',2500.00,'2021-07-16','health','standard','quarterly','PHP',9,102),(17,'2021-07-16 08:06:20.890960','2021-07-16 08:06:20.891001','Active',37500.00,'2021-11-16',37500.00,'2021-07-16','home','pro','quarterly','PHP',8,85),(18,'2021-07-21 01:32:42.418933','2021-07-21 01:32:42.418976','Active',2500.00,'2021-07-21',2500.00,'2021-07-21','health','standard','quarterly','PHP',9,106),(19,'2021-07-21 01:50:31.329117','2021-07-21 01:50:31.329164','Active',5000.00,'2022-01-21',5000.00,'2021-07-21','health','standard','semi_annual','PHP',9,106),(20,'2021-07-21 01:56:02.455952','2021-07-21 01:56:02.455992','Active',2500.00,'2021-07-21',2500.00,'2021-07-21','health','standard','quarterly','PHP',9,107),(21,'2021-07-21 01:56:07.756797','2021-07-21 01:56:07.756838','Active',2500.00,'2021-07-21',2500.00,'2021-07-21','health','standard','quarterly','PHP',9,107),(22,'2021-07-21 02:01:28.134260','2021-07-21 02:01:28.134305','Active',5000.00,'2022-01-21',5000.00,'2021-07-21','health','standard','semi_annual','PHP',9,106),(23,'2021-07-21 02:02:50.472362','2021-07-21 02:02:50.472415','Active',5000.00,'2022-01-21',5000.00,'2021-07-21','health','standard','semi_annual','PHP',9,106),(24,'2021-07-21 03:23:53.046709','2021-07-21 03:23:53.046755','Active',100000.00,'2022-07-21',100000.00,'2021-07-21','home','standard','annual','PHP',8,2),(25,'2021-07-21 06:48:12.875384','2021-07-21 06:48:12.875618','Active',2500.00,'2021-07-21',2500.00,'2021-07-21','health','standard','quarterly','PHP',9,111),(26,'2021-07-21 07:03:11.257870','2021-07-21 07:03:11.257917','Active',12500.00,'2021-08-21',12500.00,'2021-07-21','home','pro','monthly','PHP',8,111),(27,'2021-07-21 07:03:18.470031','2021-07-21 07:03:18.470075','Active',12500.00,'2021-08-21',12500.00,'2021-07-21','home','pro','monthly','PHP',8,111),(28,'2021-07-21 07:12:35.289751','2021-07-21 07:12:35.289794','Active',2500.00,'2021-07-21',2500.00,'2021-07-21','health','standard','quarterly','PHP',9,111),(29,'2021-07-21 07:18:02.897151','2021-07-21 07:18:02.897194','Active',5000.00,'2022-01-21',5000.00,'2021-07-21','health','standard','semi_annual','PHP',9,111),(30,'2021-07-21 07:31:29.289697','2021-07-21 07:31:29.289782','Active',5000.00,'2022-01-21',5000.00,'2021-07-21','health','standard','semi_annual','PHP',9,111),(31,'2021-07-21 08:19:28.451738','2021-07-21 08:19:28.451777','Active',2500.00,'2021-07-21',2500.00,'2021-07-21','health','standard','quarterly','PHP',9,111),(32,'2021-07-21 08:21:16.506082','2021-07-21 08:21:16.506124','Active',2500.00,'2021-07-21',2500.00,'2021-07-21','health','standard','quarterly','PHP',9,111),(34,'2021-07-22 03:02:46.086915','2021-07-22 03:02:46.087257','Active',6000.00,'2021-07-22',6000.00,'2021-07-22','health','basic','quarterly','PHP',10,99),(35,'2021-07-22 03:03:09.545509','2021-07-22 03:03:09.545552','Active',6000.00,'2021-07-22',6000.00,'2021-07-22','health','basic','quarterly','PHP',10,99),(37,'2021-07-22 03:31:03.607452','2021-07-22 03:31:03.607500','Active',2500.00,'2021-07-22',2500.00,'2021-07-22','health','lite','quarterly','PHP',14,102),(38,'2021-07-22 03:31:08.741717','2021-07-22 03:31:08.741765','Active',2500.00,'2021-07-22',2500.00,'2021-07-22','health','lite','quarterly','PHP',14,102),(39,'2021-07-22 04:25:21.351693','2021-07-22 04:25:21.351737','Active',2500.00,'2021-07-22',2500.00,'2021-07-22','health','lite','quarterly','PHP',14,121),(40,'2021-07-22 04:26:07.394951','2021-07-22 04:26:07.395012','Active',2500.00,'2021-07-22',2500.00,'2021-07-22','health','standard','quarterly','PHP',9,121),(41,'2021-07-22 04:28:50.961648','2021-07-22 04:28:50.961688','paid',2500.00,'2021-07-22',2500.00,'2021-07-22','home','standard','quarterly','PHP',11,121),(42,'2021-07-22 04:31:48.769890','2021-07-22 04:31:48.769945','Active',2500.00,'2021-07-22',2500.00,'2021-07-22','health','lite','quarterly','PHP',14,103),(43,'2021-07-22 05:32:08.231429','2021-07-22 05:32:08.231473','Active',12500.00,'2021-07-22',12500.00,'2021-07-22','life','basic','quarterly','PHP',12,103),(44,'2021-07-22 05:32:10.143208','2021-07-22 05:32:10.143251','Active',12500.00,'2021-07-22',12500.00,'2021-07-22','life','basic','quarterly','PHP',12,103),(45,'2021-07-23 04:18:44.772681','2021-07-23 04:18:44.772681','paid',100000.00,'2021-07-23',100000.00,'2021-07-23','health','basic','quarterly','PHP',2,129),(46,'2021-07-23 04:20:50.592800','2021-07-23 04:20:50.592800','paid',100000.00,'2021-07-23',100000.00,'2021-07-23','life','basic','one_time','PHP',2,129),(47,'2021-07-23 05:23:51.157680','2021-07-23 05:23:51.157722','Active',4166.67,'2021-08-23',4166.67,'2021-07-23','health','basic','monthly','PHP',13,111),(48,'2021-07-23 05:23:51.689003','2021-07-23 05:23:51.689058','Active',4166.67,'2021-08-23',4166.67,'2021-07-23','health','basic','monthly','PHP',13,111),(49,'2021-07-23 07:18:00.530515','2021-07-23 07:18:00.530515','paid',50000.00,'2021-07-23',50000.00,'2021-07-23','life','lite','one_time','PHP',2,129),(50,'2021-07-23 07:18:31.846117','2021-07-23 07:18:31.846117','paid',50000.00,'2021-07-23',50000.00,'2021-07-23','life','basic','one_time','PHP',2,129),(51,'2021-07-23 08:30:38.470823','2021-07-23 08:30:38.470823','paid',50000.00,'2021-07-23',50000.00,'2021-07-23','life','basic','one_time','PHP',2,129),(52,'2021-07-25 23:01:04.018578','2021-07-25 23:01:04.018621','Active',2500.00,'2021-07-26',2500.00,'2021-07-26','health','lite','quarterly','PHP',14,136),(53,'2021-07-26 00:03:04.502193','2021-07-26 00:03:04.502260','Active',2500.00,'2021-07-26',2500.00,'2021-07-26','health','lite','quarterly','PHP',14,137),(54,'2021-07-26 00:03:21.161853','2021-07-26 00:03:21.161895','Active',2500.00,'2021-07-26',2500.00,'2021-07-26','health','lite','quarterly','PHP',14,137),(57,'2021-07-26 03:16:35.092695','2021-07-26 03:16:35.092776','Active',4166.67,'2021-08-26',4166.67,'2021-07-26','health','basic','monthly','PHP',13,85),(58,'2021-07-26 06:21:33.186361','2021-07-26 06:21:33.186405','Active',50000.00,'2022-07-26',50000.00,'2021-07-26','health','basic','annual','PHP',17,142),(59,'2021-07-26 06:21:33.640662','2021-07-26 06:21:33.640724','Active',50000.00,'2022-07-26',50000.00,'2021-07-26','health','basic','annual','PHP',17,142),(60,'2021-07-26 06:23:26.576123','2021-07-26 06:23:26.576165','Active',50000.00,'2022-07-26',50000.00,'2021-07-26','health','basic','annual','PHP',17,142),(61,'2021-07-26 06:25:11.243278','2021-07-26 06:38:36.265638','Active',50000.00,'2025-07-26',50000.00,'2021-07-26','health','basic','annual','PHP',17,142),(62,'2021-07-26 21:02:42.400806','2021-07-26 21:02:42.400846','Active',50000.00,'2022-07-27',50000.00,'2021-07-27','health','basic','annual','PHP',17,137),(63,'2021-07-26 21:02:43.437802','2021-07-26 21:02:43.437846','Active',50000.00,'2022-07-27',50000.00,'2021-07-27','health','basic','annual','PHP',17,137),(64,'2021-07-26 21:30:30.328029','2021-07-26 21:30:30.328080','Active',50000.00,'2022-07-27',50000.00,'2021-07-27','health','basic','annual','PHP',17,137);
/*!40000 ALTER TABLE `digiinsurance_insureepolicy` ENABLE KEYS */;
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

-- Dump completed on 2021-07-28 10:44:04
