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
-- Table structure for table `digiinsurance_transaction`
--

DROP TABLE IF EXISTS `digiinsurance_transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `digiinsurance_transaction` (
  `id` int NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `modified_at` datetime(6) NOT NULL,
  `archived` tinyint(1) NOT NULL,
  `archived_at` datetime(6) DEFAULT NULL,
  `transaction_date` datetime(6) NOT NULL,
  `txn_id` varchar(64) DEFAULT NULL,
  `amount` decimal(8,2) NOT NULL,
  `fee` decimal(10,2) NOT NULL,
  `vat` decimal(10,2) NOT NULL,
  `updated_at` datetime(6) DEFAULT NULL,
  `channel` varchar(32) DEFAULT NULL,
  `payment_type` varchar(6) NOT NULL,
  `processor_type` varchar(16) DEFAULT NULL,
  `processor` varchar(10) DEFAULT NULL,
  `completed_at` datetime(6) DEFAULT NULL,
  `description` varchar(256) DEFAULT NULL,
  `company_id` int DEFAULT NULL,
  `insureePolicy_id` int NOT NULL,
  `insuree_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `digiinsurance_transa_company_id_450a5216_fk_digiinsur` (`company_id`),
  KEY `digiinsurance_transa_insureePolicy_id_c5d4307e_fk_digiinsur` (`insureePolicy_id`),
  KEY `digiinsurance_transa_insuree_id_80db8ecb_fk_digiinsur` (`insuree_id`),
  CONSTRAINT `digiinsurance_transa_company_id_450a5216_fk_digiinsur` FOREIGN KEY (`company_id`) REFERENCES `digiinsurance_company` (`id`),
  CONSTRAINT `digiinsurance_transa_insuree_id_80db8ecb_fk_digiinsur` FOREIGN KEY (`insuree_id`) REFERENCES `digiinsurance_insuree` (`user_id`),
  CONSTRAINT `digiinsurance_transa_insureePolicy_id_c5d4307e_fk_digiinsur` FOREIGN KEY (`insureePolicy_id`) REFERENCES `digiinsurance_insureepolicy` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digiinsurance_transaction`
--

LOCK TABLES `digiinsurance_transaction` WRITE;
/*!40000 ALTER TABLE `digiinsurance_transaction` DISABLE KEYS */;
INSERT INTO `digiinsurance_transaction` VALUES (1,'2021-07-21 02:01:28.531015','2021-07-21 02:01:28.531058',0,NULL,'2021-07-21 02:01:28.531119','M4I86UQ4ZU',5020.00,0.00,0.00,NULL,'dp','full','otc_bank',NULL,'2021-07-21 02:01:28.533252','algaringo@gmail.com Payments for Product 1, PHP 5020.00',1,22,106),(2,'2021-07-21 02:02:50.865055','2021-07-21 02:02:50.865092',0,NULL,'2021-07-21 02:02:50.865131','Y8U9BY95GA',5020.00,0.00,0.00,NULL,'dp','full','otc_bank',NULL,'2021-07-21 02:02:50.867984','algaringo@gmail.com Payments for Product 1, PHP 5020.00',1,23,106),(3,'2021-07-21 03:23:53.646303','2021-07-21 03:23:53.646341',0,NULL,'2021-07-21 03:23:53.646381','J4VBALWULU',100020.00,0.00,0.00,NULL,'dp','full','otc_bank',NULL,'2021-07-21 03:23:53.647474','gojo@example.com Payments for Home Plan, PHP 100020.00',1,24,2),(4,'2021-07-21 08:19:29.923155','2021-07-21 08:19:29.923195',0,NULL,'2021-07-21 08:19:29.923235','HUYC9KMGWZ',2520.00,0.00,0.00,NULL,'dp','full','otc_bank',NULL,'2021-07-21 08:19:29.925641','rjdeguzman@upedu.ph Payments for Product 1, PHP 2520.00',1,31,111),(5,'2021-07-21 08:21:17.212950','2021-07-21 08:21:17.212988',0,NULL,'2021-07-21 08:21:17.213025','TV45YC5S8S',2520.00,0.00,0.00,NULL,'dp','full','otc_bank',NULL,'2021-07-21 08:21:17.214287','rjdeguzman@upedu.ph Payments for Product 1, PHP 2520.00',1,32,111),(6,'2021-07-22 04:28:51.580641','2021-07-22 04:28:51.580684',0,NULL,'2021-07-22 04:28:51.580722','PKAYRAYGBI',2520.00,0.00,0.00,NULL,'dp','full','otc_bank',NULL,'2021-07-22 04:28:51.583137','jpdenopol@up.edu.ph Payments for Product X, PHP 2520.00',1,41,121),(7,'2021-07-22 05:32:09.367722','2021-07-22 05:32:09.367766',0,NULL,'2021-07-22 05:32:09.367807','3IXNOUEUQB',12520.00,0.00,0.00,NULL,'dp','full','otc_bank',NULL,'2021-07-22 05:32:09.369531','angel.dummy.test@gmail.com Payments for Life Plan, PHP 12520.00',1,43,103),(8,'2021-07-22 05:32:11.156147','2021-07-22 05:32:11.156191',0,NULL,'2021-07-22 05:32:11.156230','MROMTF5RZX',12520.00,0.00,0.00,NULL,'dp','full','otc_bank',NULL,'2021-07-22 05:32:11.157458','angel.dummy.test@gmail.com Payments for Life Plan, PHP 12520.00',1,44,103),(9,'2021-07-23 05:23:52.194196','2021-07-23 05:23:52.194241',0,NULL,'2021-07-23 05:23:52.194281','6EBHIJ3VHV',4186.67,0.00,0.00,NULL,'dp','full','otc_bank',NULL,'2021-07-23 05:23:52.197719','rjdeguzman@upedu.ph Payments for Health Plan, PHP 4186.67',2,48,111),(10,'2021-07-23 05:23:52.211324','2021-07-23 05:23:52.211373',0,NULL,'2021-07-23 05:23:52.211418','TISYCCALRB',4186.67,0.00,0.00,NULL,'dp','full','otc_bank',NULL,'2021-07-23 05:23:52.212529','rjdeguzman@upedu.ph Payments for Health Plan, PHP 4186.67',2,47,111),(11,'2021-07-25 23:01:04.436726','2021-07-25 23:01:04.436801',0,NULL,'2021-07-25 23:01:04.436843','NJNNCNCPLF',2520.00,0.00,0.00,NULL,'dp','full','otc_bank',NULL,'2021-07-25 23:01:04.440778','tatopi2092@britted.com Payments for Product XYZ, PHP 2520.00',NULL,52,136),(12,'2021-07-26 00:03:21.480513','2021-07-26 00:03:21.480556',0,NULL,'2021-07-26 00:03:21.480597','5IRY8MJ9AI',2520.00,0.00,0.00,NULL,'dp','full','otc_bank',NULL,'2021-07-26 00:03:21.482333','xiviyog713@dmsdmg.com Payments for Product XYZ, PHP 2520.00',NULL,54,137),(15,'2021-07-26 03:16:35.722281','2021-07-26 03:16:35.722331',0,NULL,'2021-07-26 03:16:35.722372','RZLZPVSHHN',4186.67,0.00,0.00,NULL,'dp','full','otc_bank',NULL,'2021-07-26 03:16:35.724163','carlo_coste@questronix.com.ph Payments for Health Plan, PHP 4186.67',2,57,85),(17,'2021-07-26 06:21:33.940685','2021-07-26 06:21:33.940730',0,NULL,'2021-07-26 06:21:33.940797','9GVFBF368E',50020.00,0.00,0.00,NULL,'dp','full','otc_bank',NULL,'2021-07-26 06:21:33.944191','neclinga001@gmail.com Payments for Test Plan 2, PHP 50020.00',1,58,142),(18,'2021-07-26 06:21:34.088849','2021-07-26 06:21:34.088909',0,NULL,'2021-07-26 06:21:34.088952','NSHBDWPAI3',50020.00,0.00,0.00,NULL,'dp','full','otc_bank',NULL,'2021-07-26 06:21:34.091145','neclinga001@gmail.com Payments for Test Plan 2, PHP 50020.00',1,59,142),(19,'2021-07-26 06:25:12.789890','2021-07-26 06:25:12.789949',0,NULL,'2021-07-26 06:25:12.790007','MR3RYP3AAI',50020.00,0.00,0.00,NULL,'dp','full','otc_bank',NULL,'2021-07-26 06:25:12.792339','neclinga001@gmail.com Payments for Test Plan 2, PHP 50020.00',1,61,142),(20,'2021-07-26 06:35:46.784240','2021-07-26 06:35:46.784282',0,NULL,'2021-07-26 06:35:46.784322','6FGGY6WVII',50020.00,0.00,0.00,NULL,'dp','full','otc_bank',NULL,'2021-07-26 06:35:46.787971','neclinga001@gmail.com Payments for Test Plan 2, PHP 50020.00',1,61,142),(21,'2021-07-26 06:36:47.941656','2021-07-26 06:36:47.941709',0,NULL,'2021-07-26 06:36:47.941765','NAA5AHDX58',50020.00,0.00,0.00,NULL,'dp','full','otc_bank',NULL,'2021-07-26 06:36:47.943849','neclinga001@gmail.com Payments for Test Plan 2, PHP 50020.00',1,61,142),(22,'2021-07-26 21:02:43.493600','2021-07-26 21:02:43.493637',0,NULL,'2021-07-26 21:02:43.493674','3DKTGANSPN',50020.00,0.00,0.00,NULL,'dp','full','otc_bank',NULL,'2021-07-26 21:02:43.495755','xiviyog713@dmsdmg.com Payments for Test Plan 2, PHP 50020.00',1,62,137),(23,'2021-07-26 21:02:44.329702','2021-07-26 21:02:44.329754',0,NULL,'2021-07-26 21:02:44.329806','RN5J3LP8CH',50020.00,0.00,0.00,NULL,'dp','full','otc_bank',NULL,'2021-07-26 21:02:44.331321','xiviyog713@dmsdmg.com Payments for Test Plan 2, PHP 50020.00',1,63,137),(24,'2021-07-26 21:30:31.100316','2021-07-26 21:30:31.100353',0,NULL,'2021-07-26 21:30:31.100393','9FPZB55NUM',50020.00,0.00,0.00,NULL,'dp','full','otc_bank',NULL,'2021-07-26 21:30:31.104478','xiviyog713@dmsdmg.com Payments for Test Plan 2, PHP 50020.00',1,64,137);
/*!40000 ALTER TABLE `digiinsurance_transaction` ENABLE KEYS */;
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

-- Dump completed on 2021-07-28 10:44:01
