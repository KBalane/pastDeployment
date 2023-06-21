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
-- Table structure for table `django_dragonpay_dragonpaytransaction`
--

DROP TABLE IF EXISTS `django_dragonpay_dragonpaytransaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_dragonpay_dragonpaytransaction` (
  `id` varchar(40) NOT NULL,
  `token` varchar(40) NOT NULL,
  `refno` varchar(8) DEFAULT NULL,
  `amount` decimal(8,2) NOT NULL,
  `currency` varchar(3) NOT NULL,
  `description` varchar(128) NOT NULL,
  `email` varchar(40) NOT NULL,
  `param1` varchar(80) DEFAULT NULL,
  `param2` varchar(80) DEFAULT NULL,
  `status` varchar(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `modified_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_dragonpay_dragonpaytransaction`
--

LOCK TABLES `django_dragonpay_dragonpaytransaction` WRITE;
/*!40000 ALTER TABLE `django_dragonpay_dragonpaytransaction` DISABLE KEYS */;
INSERT INTO `django_dragonpay_dragonpaytransaction` VALUES ('152deD40cFA37BafbC96','d3904af742d91ffe54d479ac904b30f2',NULL,2520.00,'PHP','rjdeguzman@upedu.ph Payments for Product 1, PHP 2520.00','rjdeguzman@upedu.ph',NULL,NULL,'P','2021-07-21 08:21:17.210575','2021-07-21 08:21:17.210617'),('24D6ebcF0d5faB1978CA','2bb43d0da4659f243e9f3130001d4dcf','M2WSZ542',50020.00,'PHP','neclinga001@gmail.com Payments for Test Plan 2, PHP 50020.00','neclinga001@gmail.com',NULL,NULL,'S','2021-07-26 06:25:12.780118','2021-07-26 06:25:12.780177'),('27fA30eDCB8ad1E6F5b9','449846bce4eb043c8c8f142eca8ef939',NULL,100020.00,'PHP','gojo@example.com Payments for Home Plan, PHP 100020.00','gojo@example.com',NULL,NULL,'P','2021-07-21 03:23:53.644216','2021-07-21 03:23:53.644259'),('2a75F3Afe4d0D6b1CBE8','5671a2404eeb0e0bb9438afa10943fba',NULL,50020.00,'PHP','neclinga001@gmail.com Payments for Test Plan 2, PHP 50020.00','neclinga001@gmail.com',NULL,NULL,'P','2021-07-26 06:21:33.936511','2021-07-26 06:21:33.936554'),('39F0B4EfcD26edA1C5ab','4a8b7b97f6614695f1624fbe945a1fe2',NULL,50020.00,'PHP','neclinga001@gmail.com Payments for Test Plan 2, PHP 50020.00','neclinga001@gmail.com',NULL,NULL,'P','2021-07-26 06:36:47.938604','2021-07-26 06:36:47.938649'),('485360fFbBaAc97Ed2C1','0baf281f8ec1be54e4f9408ff4f4ef28',NULL,5020.00,'PHP','algaringo@gmail.com Payments for Product 1, PHP 5020.00','algaringo@gmail.com',NULL,NULL,'P','2021-07-21 02:02:50.862007','2021-07-21 02:02:50.862046'),('4B17e86C9a0EF35cf2Db','0aa5b10c0b8551c4777fd2dd327bac89',NULL,2520.00,'PHP','jpdenopol@up.edu.ph Payments for Product X, PHP 2520.00','jpdenopol@up.edu.ph',NULL,NULL,'P','2021-07-22 04:28:51.576967','2021-07-22 04:28:51.577008'),('6d0c9D1A8345eb7CFE2f','1d0426b045b4a70d5eaf8142bea7d611',NULL,2020.00,'PHP','overfly15@gmail.com Payments for mypolicy, PHP 2020.00','overfly15@gmail.com',NULL,NULL,'P','2021-07-26 02:59:41.013893','2021-07-26 02:59:41.013936'),('7154E8d9cFBD2C36ae0b','201e581866a475f839f0738245dada5f',NULL,4186.67,'PHP','rjdeguzman@upedu.ph Payments for Health Plan, PHP 4186.67','rjdeguzman@upedu.ph',NULL,NULL,'P','2021-07-23 05:23:52.189881','2021-07-23 05:23:52.189924'),('7A1c68d90D4ae3ECfF2B','71ac897365ce4f64025faa62233a579d',NULL,4186.67,'PHP','rjdeguzman@upedu.ph Payments for Health Plan, PHP 4186.67','rjdeguzman@upedu.ph',NULL,NULL,'P','2021-07-23 05:23:52.208017','2021-07-23 05:23:52.208084'),('8D3dcB97ECb6Fe4A15af','7fbb443dfb90b486554c20376604e78c','5X5ULDM0',12520.00,'PHP','angel.dummy.test@gmail.com Payments for Life Plan, PHP 12520.00','angel.dummy.test@gmail.com',NULL,NULL,'P','2021-07-22 05:32:11.152645','2021-07-22 05:32:11.152688'),('9a5bC72eEfF13D60dA48','15a3197596161fab3bf43be2864d070d',NULL,50020.00,'PHP','neclinga001@gmail.com Payments for Test Plan 2, PHP 50020.00','neclinga001@gmail.com',NULL,NULL,'P','2021-07-26 06:21:34.084092','2021-07-26 06:21:34.084136'),('9aB1dcAD5bf6FC7eE032','3ee00627e63c824fa81f827887ebd424',NULL,50020.00,'PHP','xiviyog713@dmsdmg.com Payments for Test Plan 2, PHP 50020.00','xiviyog713@dmsdmg.com',NULL,NULL,'P','2021-07-26 21:30:31.097260','2021-07-26 21:30:31.097302'),('a03fbcA9d5FD28e46C7E','9eba301c34069488ac72b089cd94c7be',NULL,2520.00,'PHP','rjdeguzman@upedu.ph Payments for Product 1, PHP 2520.00','rjdeguzman@upedu.ph',NULL,NULL,'P','2021-07-21 08:19:29.919608','2021-07-21 08:19:29.919649'),('b5a1EC2e687BFDA0df93','61f20bb8cf9cada114bc79def1e5b7d2','597QJCX5',5020.00,'PHP','algaringo@gmail.com Payments for Product 1, PHP 5020.00','algaringo@gmail.com',NULL,NULL,'P','2021-07-21 02:01:28.527386','2021-07-21 02:01:28.527438'),('Db5A0F148C2c9BeEad76','4777dbde05e3b9d3186371f906734d9a','R6AVLFM0',50020.00,'PHP','neclinga001@gmail.com Payments for Test Plan 2, PHP 50020.00','neclinga001@gmail.com',NULL,NULL,'S','2021-07-26 06:35:46.781395','2021-07-26 06:35:46.781461'),('e483d0b2Df9cBaCE6F51','451999852cb5e67539c2a18be66cccd8','LTKD7VN2',50020.00,'PHP','xiviyog713@dmsdmg.com Payments for Test Plan 2, PHP 50020.00','xiviyog713@dmsdmg.com',NULL,NULL,'P','2021-07-26 21:02:43.490584','2021-07-26 21:02:43.490624'),('e542D79FEd6Ccf0a831A','43b6be4a57fc38c3216727013c7bcad2',NULL,4186.67,'PHP','carlo_coste@questronix.com.ph Payments for Health Plan, PHP 4186.67','carlo_coste@questronix.com.ph',NULL,NULL,'P','2021-07-26 03:16:35.713487','2021-07-26 03:16:35.713532'),('f89BaC0A5FDdb631Ec72','2f7cc9a9d612b5d4365d8e5a19f69e18',NULL,50020.00,'PHP','xiviyog713@dmsdmg.com Payments for Test Plan 2, PHP 50020.00','xiviyog713@dmsdmg.com',NULL,NULL,'P','2021-07-26 21:02:44.325101','2021-07-26 21:02:44.325151'),('F8C1fc5A49D6b2E3d7Be','7faae4224b8c9ad600f32b8b2c7a26df',NULL,2520.00,'PHP','xiviyog713@dmsdmg.com Payments for Product XYZ, PHP 2520.00','xiviyog713@dmsdmg.com',NULL,NULL,'P','2021-07-26 00:03:21.475037','2021-07-26 00:03:21.475080'),('f91cB6CD0ed45bE8Aa32','a9a4e9dc40b1035b06945aabb9e81952',NULL,12520.00,'PHP','angel.dummy.test@gmail.com Payments for Life Plan, PHP 12520.00','angel.dummy.test@gmail.com',NULL,NULL,'P','2021-07-22 05:32:09.364218','2021-07-22 05:32:09.364263'),('FB78ec2bfdED60419CaA','906cc8896e73fa450c982702c997026a',NULL,2520.00,'PHP','tatopi2092@britted.com Payments for Product XYZ, PHP 2520.00','tatopi2092@britted.com',NULL,NULL,'P','2021-07-25 23:01:04.429735','2021-07-25 23:01:04.429777');
/*!40000 ALTER TABLE `django_dragonpay_dragonpaytransaction` ENABLE KEYS */;
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

-- Dump completed on 2021-07-28 10:44:47
