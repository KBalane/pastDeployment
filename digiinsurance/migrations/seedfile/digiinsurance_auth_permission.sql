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
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=187 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add Payout',6,'add_dragonpaypayout'),(22,'Can change Payout',6,'change_dragonpaypayout'),(23,'Can delete Payout',6,'delete_dragonpaypayout'),(24,'Can view Payout',6,'view_dragonpaypayout'),(25,'Can add Payout User',7,'add_dragonpaypayoutuser'),(26,'Can change Payout User',7,'change_dragonpaypayoutuser'),(27,'Can delete Payout User',7,'delete_dragonpaypayoutuser'),(28,'Can view Payout User',7,'view_dragonpaypayoutuser'),(29,'Can add Transaction',8,'add_dragonpaytransaction'),(30,'Can change Transaction',8,'change_dragonpaytransaction'),(31,'Can delete Transaction',8,'delete_dragonpaytransaction'),(32,'Can view Transaction',8,'view_dragonpaytransaction'),(33,'Can add Token',9,'add_token'),(34,'Can change Token',9,'change_token'),(35,'Can delete Token',9,'delete_token'),(36,'Can view Token',9,'view_token'),(37,'Can add user',10,'add_user'),(38,'Can change user',10,'change_user'),(39,'Can delete user',10,'delete_user'),(40,'Can view user',10,'view_user'),(41,'Can update permissions',10,'update_permissions'),(42,'View only access',10,'view_only'),(43,'Can add audit entry',11,'add_auditentry'),(44,'Can change audit entry',11,'change_auditentry'),(45,'Can delete audit entry',11,'delete_auditentry'),(46,'Can view audit entry',11,'view_auditentry'),(47,'Can add company',12,'add_company'),(48,'Can change company',12,'change_company'),(49,'Can delete company',12,'delete_company'),(50,'Can view company',12,'view_company'),(51,'Can add company investment type',13,'add_companyinvestmenttype'),(52,'Can change company investment type',13,'change_companyinvestmenttype'),(53,'Can delete company investment type',13,'delete_companyinvestmenttype'),(54,'Can view company investment type',13,'view_companyinvestmenttype'),(55,'Can add health questions',14,'add_healthquestions'),(56,'Can change health questions',14,'change_healthquestions'),(57,'Can delete health questions',14,'delete_healthquestions'),(58,'Can view health questions',14,'view_healthquestions'),(59,'Can add insuree policy',15,'add_insureepolicy'),(60,'Can change insuree policy',15,'change_insureepolicy'),(61,'Can delete insuree policy',15,'delete_insureepolicy'),(62,'Can view insuree policy',15,'view_insureepolicy'),(63,'Can add payout',16,'add_payout'),(64,'Can change payout',16,'change_payout'),(65,'Can delete payout',16,'delete_payout'),(66,'Can view payout',16,'view_payout'),(67,'Can add policy',17,'add_policy'),(68,'Can change policy',17,'change_policy'),(69,'Can delete policy',17,'delete_policy'),(70,'Can view policy',17,'view_policy'),(71,'Can add product',18,'add_product'),(72,'Can change product',18,'change_product'),(73,'Can delete product',18,'delete_product'),(74,'Can view product',18,'view_product'),(75,'Can add insuree',19,'add_insuree'),(76,'Can change insuree',19,'change_insuree'),(77,'Can delete insuree',19,'delete_insuree'),(78,'Can view insuree',19,'view_insuree'),(79,'Can add user bank account',20,'add_userbankaccount'),(80,'Can change user bank account',20,'change_userbankaccount'),(81,'Can delete user bank account',20,'delete_userbankaccount'),(82,'Can view user bank account',20,'view_userbankaccount'),(83,'Can add temp beneficiaries',21,'add_tempbeneficiaries'),(84,'Can change temp beneficiaries',21,'change_tempbeneficiaries'),(85,'Can delete temp beneficiaries',21,'delete_tempbeneficiaries'),(86,'Can view temp beneficiaries',21,'view_tempbeneficiaries'),(87,'Can add policy requirements',22,'add_policyrequirements'),(88,'Can change policy requirements',22,'change_policyrequirements'),(89,'Can delete policy requirements',22,'delete_policyrequirements'),(90,'Can view policy requirements',22,'view_policyrequirements'),(91,'Can add policy calculator',23,'add_policycalculator'),(92,'Can change policy calculator',23,'change_policycalculator'),(93,'Can delete policy calculator',23,'delete_policycalculator'),(94,'Can view policy calculator',23,'view_policycalculator'),(95,'Can add insuree policy docs',24,'add_insureepolicydocs'),(96,'Can change insuree policy docs',24,'change_insureepolicydocs'),(97,'Can delete insuree policy docs',24,'delete_insureepolicydocs'),(98,'Can view insuree policy docs',24,'view_insureepolicydocs'),(99,'Can add health questions answers',25,'add_healthquestionsanswers'),(100,'Can change health questions answers',25,'change_healthquestionsanswers'),(101,'Can delete health questions answers',25,'delete_healthquestionsanswers'),(102,'Can view health questions answers',25,'view_healthquestionsanswers'),(103,'Can add favourites',26,'add_favourites'),(104,'Can change favourites',26,'change_favourites'),(105,'Can delete favourites',26,'delete_favourites'),(106,'Can view favourites',26,'view_favourites'),(107,'Can add email verification',27,'add_emailverification'),(108,'Can change email verification',27,'change_emailverification'),(109,'Can delete email verification',27,'delete_emailverification'),(110,'Can view email verification',27,'view_emailverification'),(111,'Can add document template',28,'add_documenttemplate'),(112,'Can change document template',28,'change_documenttemplate'),(113,'Can delete document template',28,'delete_documenttemplate'),(114,'Can view document template',28,'view_documenttemplate'),(115,'Can add company socials',29,'add_companysocials'),(116,'Can change company socials',29,'change_companysocials'),(117,'Can delete company socials',29,'delete_companysocials'),(118,'Can view company socials',29,'view_companysocials'),(119,'Can add company requirements',30,'add_companyrequirements'),(120,'Can change company requirements',30,'change_companyrequirements'),(121,'Can delete company requirements',30,'delete_companyrequirements'),(122,'Can view company requirements',30,'view_companyrequirements'),(123,'Can add company config',31,'add_companyconfig'),(124,'Can change company config',31,'change_companyconfig'),(125,'Can delete company config',31,'delete_companyconfig'),(126,'Can view company config',31,'view_companyconfig'),(127,'Can add claims',32,'add_claims'),(128,'Can change claims',32,'change_claims'),(129,'Can delete claims',32,'delete_claims'),(130,'Can view claims',32,'view_claims'),(131,'Can add beneficiaries',33,'add_beneficiaries'),(132,'Can change beneficiaries',33,'change_beneficiaries'),(133,'Can delete beneficiaries',33,'delete_beneficiaries'),(134,'Can view beneficiaries',33,'view_beneficiaries'),(135,'Can add bank account',34,'add_bankaccount'),(136,'Can change bank account',34,'change_bankaccount'),(137,'Can delete bank account',34,'delete_bankaccount'),(138,'Can view bank account',34,'view_bankaccount'),(139,'Can add advertisement',35,'add_advertisement'),(140,'Can change advertisement',35,'change_advertisement'),(141,'Can delete advertisement',35,'delete_advertisement'),(142,'Can view advertisement',35,'view_advertisement'),(143,'Can add user investment',36,'add_userinvestment'),(144,'Can change user investment',36,'change_userinvestment'),(145,'Can delete user investment',36,'delete_userinvestment'),(146,'Can view user investment',36,'view_userinvestment'),(147,'Can add transaction',37,'add_transaction'),(148,'Can change transaction',37,'change_transaction'),(149,'Can delete transaction',37,'delete_transaction'),(150,'Can view transaction',37,'view_transaction'),(151,'Can add staff',38,'add_staff'),(152,'Can change staff',38,'change_staff'),(153,'Can delete staff',38,'delete_staff'),(154,'Can view staff',38,'view_staff'),(155,'Can add insuree payment details',39,'add_insureepaymentdetails'),(156,'Can change insuree payment details',39,'change_insureepaymentdetails'),(157,'Can delete insuree payment details',39,'delete_insureepaymentdetails'),(158,'Can view insuree payment details',39,'view_insureepaymentdetails'),(159,'Can add template id',40,'add_templateid'),(160,'Can change template id',40,'change_templateid'),(161,'Can delete template id',40,'delete_templateid'),(162,'Can view template id',40,'view_templateid'),(163,'Can add user id',41,'add_userid'),(164,'Can change user id',41,'change_userid'),(165,'Can delete user id',41,'delete_userid'),(166,'Can view user id',41,'view_userid'),(167,'Can add wallet',42,'add_wallet'),(168,'Can change wallet',42,'change_wallet'),(169,'Can delete wallet',42,'delete_wallet'),(170,'Can view wallet',42,'view_wallet'),(171,'Can add contract',43,'add_contract'),(172,'Can change contract',43,'change_contract'),(173,'Can delete contract',43,'delete_contract'),(174,'Can view contract',43,'view_contract'),(175,'Can add certificate address',44,'add_certificateaddress'),(176,'Can change certificate address',44,'change_certificateaddress'),(177,'Can delete certificate address',44,'delete_certificateaddress'),(178,'Can view certificate address',44,'view_certificateaddress'),(179,'Can add transaction',45,'add_transaction'),(180,'Can change transaction',45,'change_transaction'),(181,'Can delete transaction',45,'delete_transaction'),(182,'Can view transaction',45,'view_transaction'),(183,'Can add token',46,'add_tokenproxy'),(184,'Can change token',46,'change_tokenproxy'),(185,'Can delete token',46,'delete_tokenproxy'),(186,'Can view token',46,'view_tokenproxy');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
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

-- Dump completed on 2021-07-28 10:44:39
