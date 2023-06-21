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
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2021-07-14 15:43:02.633582'),(2,'contenttypes','0002_remove_content_type_name','2021-07-14 15:43:02.909277'),(3,'auth','0001_initial','2021-07-14 15:43:03.416606'),(4,'auth','0002_alter_permission_name_max_length','2021-07-14 15:43:03.774848'),(5,'auth','0003_alter_user_email_max_length','2021-07-14 15:43:03.848616'),(6,'auth','0004_alter_user_username_opts','2021-07-14 15:43:03.924529'),(7,'auth','0005_alter_user_last_login_null','2021-07-14 15:43:04.002686'),(8,'auth','0006_require_contenttypes_0002','2021-07-14 15:43:04.081265'),(9,'auth','0007_alter_validators_add_error_messages','2021-07-14 15:43:04.170585'),(10,'auth','0008_alter_user_username_max_length','2021-07-14 15:43:04.244138'),(11,'auth','0009_alter_user_last_name_max_length','2021-07-14 15:43:04.319250'),(12,'auth','0010_alter_group_name_max_length','2021-07-14 15:43:04.443736'),(13,'auth','0011_update_proxy_permissions','2021-07-14 15:43:04.639370'),(14,'auth','0012_alter_user_first_name_max_length','2021-07-14 15:43:04.716928'),(15,'digiinsurance','0001_initial','2021-07-14 15:43:18.691783'),(16,'admin','0001_initial','2021-07-14 15:43:21.330284'),(17,'admin','0002_logentry_remove_auto_add','2021-07-14 15:43:21.517907'),(18,'admin','0003_logentry_add_action_flag_choices','2021-07-14 15:43:21.606428'),(19,'authtoken','0001_initial','2021-07-14 15:43:21.859704'),(20,'authtoken','0002_auto_20160226_1747','2021-07-14 15:43:22.377251'),(21,'django_dragonpay','0001_initial','2021-07-14 15:43:23.883163'),(22,'django_dragonpay','0002_transaction_status_options','2021-07-14 15:43:23.954322'),(23,'django_dragonpay','0003_larger_max_length','2021-07-14 15:43:24.114435'),(24,'django_dragonpay','0004_auto_20201211_1036','2021-07-14 15:43:24.209885'),(25,'kyc','0001_initial','2021-07-14 15:43:24.958858'),(26,'kyc','0002_auto_20200926_1548','2021-07-14 15:43:25.196249'),(27,'kyc','0003_auto_20210324_1351','2021-07-14 15:43:25.360062'),(28,'sessions','0001_initial','2021-07-14 15:43:25.567037'),(29,'blockchain','0001_initial','2021-07-14 15:50:17.425500'),(30,'kyc','0004_userid_photo_id_back','2021-07-15 14:28:04.717408'),(31,'digiinsurance','0002_auto_20210715_2251','2021-07-15 14:51:40.746395'),(32,'authtoken','0003_tokenproxy','2021-07-16 08:41:24.326425'),(33,'digiinsurance','0003_policy_passing_score','2021-07-19 02:25:36.813449'),(34,'digiinsurance','0003_claims_claim_status','2021-07-19 06:15:11.784507'),(35,'digiinsurance','0004_merge_20210722_1507','2021-07-22 07:08:16.143756'),(36,'digiinsurance','0004_merge_20210723_1100','2021-07-23 03:02:09.169328'),(37,'digiinsurance','0005_auto_20210723_1100','2021-07-23 03:02:09.697560'),(38,'digiinsurance','0006_auto_20210727_1110','2021-07-27 03:23:24.634674');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
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

-- Dump completed on 2021-07-28 10:43:57
