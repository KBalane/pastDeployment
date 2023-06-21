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
-- Table structure for table `digiinsurance_user_user_permissions`
--

DROP TABLE IF EXISTS `digiinsurance_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `digiinsurance_user_user_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `digiinsurance_user_user__user_id_permission_id_1b6bfd1c_uniq` (`user_id`,`permission_id`),
  KEY `digiinsurance_user_u_permission_id_f52bd7f7_fk_auth_perm` (`permission_id`),
  CONSTRAINT `digiinsurance_user_u_permission_id_f52bd7f7_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `digiinsurance_user_u_user_id_26f85828_fk_digiinsur` FOREIGN KEY (`user_id`) REFERENCES `digiinsurance_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=365 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digiinsurance_user_user_permissions`
--

LOCK TABLES `digiinsurance_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `digiinsurance_user_user_permissions` DISABLE KEYS */;
INSERT INTO `digiinsurance_user_user_permissions` VALUES (183,4,1),(184,4,2),(185,4,3),(186,4,4),(187,4,5),(188,4,6),(189,4,7),(190,4,8),(191,4,9),(192,4,10),(193,4,11),(194,4,12),(195,4,13),(196,4,14),(197,4,15),(198,4,16),(199,4,17),(200,4,18),(201,4,19),(202,4,20),(203,4,21),(204,4,22),(205,4,23),(206,4,24),(207,4,25),(208,4,26),(209,4,27),(210,4,28),(211,4,29),(212,4,30),(213,4,31),(214,4,32),(215,4,33),(216,4,34),(217,4,35),(218,4,36),(219,4,37),(220,4,38),(221,4,39),(222,4,40),(223,4,41),(224,4,42),(225,4,43),(226,4,44),(227,4,45),(228,4,46),(229,4,47),(230,4,48),(231,4,49),(232,4,50),(233,4,51),(234,4,52),(235,4,53),(236,4,54),(237,4,55),(238,4,56),(239,4,57),(240,4,58),(241,4,59),(242,4,60),(243,4,61),(244,4,62),(245,4,63),(246,4,64),(247,4,65),(248,4,66),(249,4,67),(250,4,68),(251,4,69),(252,4,70),(253,4,71),(254,4,72),(255,4,73),(256,4,74),(257,4,75),(258,4,76),(259,4,77),(260,4,78),(261,4,79),(262,4,80),(263,4,81),(264,4,82),(265,4,83),(266,4,84),(267,4,85),(268,4,86),(269,4,87),(270,4,88),(271,4,89),(272,4,90),(273,4,91),(274,4,92),(275,4,93),(276,4,94),(277,4,95),(278,4,96),(279,4,97),(280,4,98),(281,4,99),(282,4,100),(283,4,101),(284,4,102),(285,4,103),(286,4,104),(287,4,105),(288,4,106),(289,4,107),(290,4,108),(291,4,109),(292,4,110),(293,4,111),(294,4,112),(295,4,113),(296,4,114),(297,4,115),(298,4,116),(299,4,117),(300,4,118),(301,4,119),(302,4,120),(303,4,121),(304,4,122),(305,4,123),(306,4,124),(307,4,125),(308,4,126),(309,4,127),(310,4,128),(311,4,129),(312,4,130),(313,4,131),(314,4,132),(315,4,133),(316,4,134),(317,4,135),(318,4,136),(319,4,137),(320,4,138),(321,4,139),(322,4,140),(323,4,141),(324,4,142),(325,4,143),(326,4,144),(327,4,145),(328,4,146),(329,4,147),(330,4,148),(331,4,149),(332,4,150),(333,4,151),(334,4,152),(335,4,153),(336,4,154),(337,4,155),(338,4,156),(339,4,157),(340,4,158),(341,4,159),(342,4,160),(343,4,161),(344,4,162),(345,4,163),(346,4,164),(347,4,165),(348,4,166),(349,4,167),(350,4,168),(351,4,169),(352,4,170),(353,4,171),(354,4,172),(355,4,173),(356,4,174),(357,4,175),(358,4,176),(359,4,177),(360,4,178),(361,4,179),(362,4,180),(363,4,181),(364,4,182),(1,5,1),(2,5,2),(3,5,3),(4,5,4),(5,5,5),(6,5,6),(7,5,7),(8,5,8),(9,5,9),(10,5,10),(11,5,11),(12,5,12),(13,5,13),(14,5,14),(15,5,15),(16,5,16),(17,5,17),(18,5,18),(19,5,19),(20,5,20),(21,5,21),(22,5,22),(23,5,23),(24,5,24),(25,5,25),(26,5,26),(27,5,27),(28,5,28),(29,5,29),(30,5,30),(31,5,31),(32,5,32),(33,5,33),(34,5,34),(35,5,35),(36,5,36),(37,5,37),(38,5,38),(39,5,39),(40,5,40),(41,5,41),(42,5,42),(43,5,43),(44,5,44),(45,5,45),(46,5,46),(47,5,47),(48,5,48),(49,5,49),(50,5,50),(51,5,51),(52,5,52),(53,5,53),(54,5,54),(55,5,55),(56,5,56),(57,5,57),(58,5,58),(59,5,59),(60,5,60),(61,5,61),(62,5,62),(63,5,63),(64,5,64),(65,5,65),(66,5,66),(67,5,67),(68,5,68),(69,5,69),(70,5,70),(71,5,71),(72,5,72),(73,5,73),(74,5,74),(75,5,75),(76,5,76),(77,5,77),(78,5,78),(79,5,79),(80,5,80),(81,5,81),(82,5,82),(83,5,83),(84,5,84),(85,5,85),(86,5,86),(87,5,87),(88,5,88),(89,5,89),(90,5,90),(91,5,91),(92,5,92),(93,5,93),(94,5,94),(95,5,95),(96,5,96),(97,5,97),(98,5,98),(99,5,99),(100,5,100),(101,5,101),(102,5,102),(103,5,103),(104,5,104),(105,5,105),(106,5,106),(107,5,107),(108,5,108),(109,5,109),(110,5,110),(111,5,111),(112,5,112),(113,5,113),(114,5,114),(115,5,115),(116,5,116),(117,5,117),(118,5,118),(119,5,119),(120,5,120),(121,5,121),(122,5,122),(123,5,123),(124,5,124),(125,5,125),(126,5,126),(127,5,127),(128,5,128),(129,5,129),(130,5,130),(131,5,131),(132,5,132),(133,5,133),(134,5,134),(135,5,135),(136,5,136),(137,5,137),(138,5,138),(139,5,139),(140,5,140),(141,5,141),(142,5,142),(143,5,143),(144,5,144),(145,5,145),(146,5,146),(147,5,147),(148,5,148),(149,5,149),(150,5,150),(151,5,151),(152,5,152),(153,5,153),(154,5,154),(155,5,155),(156,5,156),(157,5,157),(158,5,158),(159,5,159),(160,5,160),(161,5,161),(162,5,162),(163,5,163),(164,5,164),(165,5,165),(166,5,166),(167,5,167),(168,5,168),(169,5,169),(170,5,170),(171,5,171),(172,5,172),(173,5,173),(174,5,174),(175,5,175),(176,5,176),(177,5,177),(178,5,178),(179,5,179),(180,5,180),(181,5,181),(182,5,182);
/*!40000 ALTER TABLE `digiinsurance_user_user_permissions` ENABLE KEYS */;
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

-- Dump completed on 2021-07-28 10:44:26