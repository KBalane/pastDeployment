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
-- Table structure for table `digiinsurance_insuree`
--

DROP TABLE IF EXISTS `digiinsurance_insuree`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `digiinsurance_insuree` (
  `created_at` datetime(6) NOT NULL,
  `modified_at` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  `first_name` varchar(64) DEFAULT NULL,
  `middle_name` varchar(32) DEFAULT NULL,
  `last_name` varchar(32) NOT NULL,
  `gender` varchar(1) DEFAULT NULL,
  `email` varchar(128) NOT NULL,
  `mobile_number` varchar(16) DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `age` int DEFAULT NULL,
  `current_add` varchar(555) DEFAULT NULL,
  `occupation` varchar(555) DEFAULT NULL,
  `civil_status` varchar(64) DEFAULT NULL,
  `nationality` varchar(16) DEFAULT NULL,
  `place_of_birth` varchar(64) DEFAULT NULL,
  `sss` varchar(16) DEFAULT NULL,
  `business` varchar(16) DEFAULT NULL,
  `tel_number` varchar(16) DEFAULT NULL,
  `home_add` varchar(555) DEFAULT NULL,
  `home_country` varchar(16) DEFAULT NULL,
  `home_zip_code` varchar(4) DEFAULT NULL,
  `current_country` varchar(16) DEFAULT NULL,
  `current_zip_code` varchar(4) DEFAULT NULL,
  `employer` varchar(16) DEFAULT NULL,
  `nature_of_business_of_employer` varchar(16) DEFAULT NULL,
  `isArchived` tinyint(1) NOT NULL,
  `type` varchar(1) DEFAULT NULL,
  `tin` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digiinsurance_insuree`
--

LOCK TABLES `digiinsurance_insuree` WRITE;
/*!40000 ALTER TABLE `digiinsurance_insuree` DISABLE KEYS */;
INSERT INTO `digiinsurance_insuree` VALUES ('2021-07-15 01:45:18.783406','2021-07-16 06:24:50.889707',1,'Lara','Croft','Croft','F','laracroft@example.com','09128378919','1992-02-14',29,'Croft Manor','Archaeologist','Single','English','Croft Manor','1273889','Croft Manor','1723988','Croft Manor','England','1175','England','1175','Jonah Maiava','Archaeologist',0,'N',NULL),('2021-07-15 00:56:04.975320','2021-07-27 03:24:33.635316',2,'Bermylle','John','Razon','M','gojo@example.com','09667633011','1999-12-30',21,'47 Ilang-Ilang St','Student','Single','Filipino','Manila City','0398712365','Corndogz69','29231231231','Manila','Philippines','1440','Philippines','1440','MAAAAAAAAAAAAAAA','<AAAAAAAAAAAAAAA',1,'E','0398712365'),('2021-07-15 03:39:25.263211','2021-07-15 03:39:25.263256',6,'Caloy','Geronimo','Coste',NULL,'caloycoste@gmail.com','09976583355',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-15 03:56:44.183780','2021-07-15 03:56:44.238826',7,'johnny','smith','sins','M','v@v.com','09175214563','1963-04-05',58,'Tenesse','Actor','Single','US','USA','1234','Film',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-15 05:56:33.065580','2021-07-15 05:56:33.110654',16,'LEXTER KING','ORGETA','CABRERA','m','2ndcabrera23@gmail.com','09954532847','1997-12-13',23,'cavite','tulog',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-15 06:07:38.775046','2021-07-15 06:07:38.810936',17,'LEXTER KING','ORGETA','CABRERA','m','2ndcabrera24@gmail.com','09954532848','1997-12-13',23,'cavite','tulog',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-15 07:04:24.623353','2021-07-15 07:04:24.659382',18,'lex',NULL,'cabrera','m','2ndcabrera25@gmail.com','09954532849','1997-12-13',23,'cavite','tulog',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-15 07:28:52.053339','2021-07-15 07:28:52.094808',23,'lex',NULL,'cabrera','m','2ndcabrera26@gmail.com','09954532850','1997-12-13',23,'cavite','tulog',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-15 08:22:20.929892','2021-07-15 08:22:20.962443',34,'Lorenzo','N','Valentino','M','renz.valentino@gmail.com','09267326782','1991-04-10',30,'stronkstreet','Student',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-16 01:11:59.156441','2021-07-26 05:42:45.094912',85,'Carlo','Geronimo','Coste','M','carlo.coste11@gmail.com','09976583355','1998-02-11',23,'San Pedro, Laguna','Software Developer','Single','Filipino','Muntinlupa City','350-26-3564','Employed',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-16 01:16:50.041513','2021-07-16 01:16:50.085506',86,'lex',NULL,'cabrera','m','2ndcabrera27@gmail.com','09954532851','1997-12-13',23,'cavite','tulog',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-16 01:41:13.829948','2021-07-16 05:43:42.148082',90,'CARMELA-MARIE','J.','LABIAGA','F','carmela@example.com','09295195094','1999-02-01',22,'Las Pinas','Intern','Single','Filipino','Las Pinas',NULL,NULL,NULL,'Las Pinas','Philippines',NULL,'Philippines',NULL,'RAAAAAAAAAAAAAAA','RAAAAAAAAAAAAAAA',0,'E',NULL),('2021-07-16 03:30:58.748658','2021-07-16 03:30:58.750690',97,'Harvey','','Specter','M','vkalmazan@gmail.com','09145236545','1998-04-05',23,'US','Lawyer',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-16 03:50:24.100210','2021-07-16 03:50:24.102472',98,'Neill Elijah','Cortez','Linga','M','amenxd01@gmail.com','09772845842','1998-09-01',22,'555 Tuna','software',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-16 03:56:59.597905','2021-07-16 03:56:59.599301',99,'James Andrew','Cruz','Cornes','M','rexcornes@yahoo.com','09274723934','1999-02-07',22,'268-A T. Bernardo st., Brgy. New Zaniga','Philippines',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-16 04:52:53.271304','2021-07-16 04:52:53.272405',100,'Neil','','Chan','M','chanbu0217@gmail.com','09996412591','2000-01-30',21,'Quezon City','Student',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-16 05:01:29.216425','2021-07-16 05:01:29.217842',102,'I Am','','Client','M','iamclient@gmail.com','09987654321','1996-05-14',25,'Manila, Philippines','College Dean',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-16 06:06:04.909224','2021-07-16 06:06:04.910561',103,'Jacob','Sherlock','Peralta','M','angel.dummy.test@gmail.com','09209746421','1998-07-16',23,'Hell\'s Kitchen, New York','Detective',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-16 06:13:37.307483','2021-07-16 06:13:37.307548',104,'Jake','','Peralta',NULL,'angel.maas360@gmail.com','09209746422',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-16 06:18:39.349321','2021-07-16 06:18:39.349360',105,'ds','ds','ds',NULL,'angel.maas60@gmail.com','09209746423',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-16 07:12:45.305342','2021-07-21 05:37:30.101704',106,'Angelu','','Garingo','F','algaringo@gmail.com','09876543210','1998-12-07',22,'arfffffffffffffffffff','arf',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-21 01:53:52.618442','2021-07-21 05:37:39.671075',107,'Angelu','','Garingo','F','angelugaringo@gmail.com','09876543211','1111-11-11',909,'asdfghjkl','arf',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-21 06:17:55.024856','2021-07-21 06:17:55.024900',108,'Potato','','Pieces',NULL,'potatopieces17@gmail.com','09999999990',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-21 06:18:21.489080','2021-07-21 06:18:21.490594',109,'Elijah Cephia','','Bagio','M','elijah.cephia_bagio@questronix.com.ph','09785643254','1997-09-03',23,'Secret','Applications Programmer',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-21 06:19:08.815142','2021-07-21 06:19:08.816450',110,'rea','fuentes','quijada','F','rmfquijada@gmail.com','09267371300','1998-01-15',23,'sinagtala st. batasan hills, quezon city','student',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-21 06:30:45.414860','2021-07-23 07:43:08.302827',111,'Reena','','De Guzman','F','rjdeguzman@upedu.ph','09213548313','2000-03-31',21,'Makati City','Tester',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-21 08:30:10.734845','2021-07-21 08:30:10.736295',114,'Maria','','Smith','F','psylacantos.trial@gmail.com','09190745222','1993-10-19',27,'Makati City','Employed',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-21 08:37:44.605304','2021-07-21 08:37:44.607760',116,'Reena Myka','Jorda','De Guzman','M','reenamyka@yahoo.com','09213548312','1998-04-14',23,'Malolos, Bulacan','Application Programmer',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-22 04:23:39.969450','2021-07-22 04:23:39.972081',121,'Allen','','Denopol','M','jpdenopol@up.edu.ph','09062755044','1999-07-12',22,'Cebu, Philippines','Student',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-22 09:05:49.063383','2021-07-22 09:05:49.100333',125,'lex','lex','lex','m','lex@gmail.com','09954532847','1999-12-12',21,'lex','lex','lex','lex','lex','lex','lex',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-23 02:11:29.171510','2021-07-23 02:11:29.206491',126,'gojo','sukuna','satoru','M','testuser@example.com','09667633015','1991-07-15',30,'1991-07-15','stringstring',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-23 02:15:48.255947','2021-07-23 02:15:48.259496',127,'usertest','usertest','usertes','M','bermylle@gmail.com','09667633015','1990-12-30',30,'StudentStudentStudentStudent','Student',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-23 03:04:15.443771','2021-07-23 05:12:16.026952',129,'CARMELA-MARIE','J.','LABIAGA','F','carmela_marie@example.com','09295105094','1999-05-31',22,'Las Pinas','Student','Single','Filipino','Las Pinas','1187','None','2393624','Las Pinas','Philippines','1785','Philippines','1785','RNAAAAAAA','RNAAAAAAA',0,'E',NULL),('2021-07-23 03:35:12.717754','2021-07-23 03:35:12.752301',130,'gojo','sukuna','satoru','M','testuser05@example.com','09667633015','1991-07-15',30,'1991-07-15','stringstring',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-23 04:54:21.998267','2021-07-23 04:54:22.031820',131,'gojo','sukuna','satoru','M','testuser699@example.com','09667633015','1991-07-15',30,'1991-07-15','stringstring',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-23 06:00:43.317117','2021-07-23 06:00:43.319261',132,'Reena','','De Guzman','F','rjdeguzman@up.edu.ph','09213548312','1998-04-14',23,'Makati City','Application Programmer',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-23 07:13:15.273030','2021-07-23 07:13:15.308750',133,'gojo','sukuna','satoru','M','testuser69@example.com','09667633015','1991-07-15',30,'1991-07-15','stringstring',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-23 08:15:27.864788','2021-07-23 08:15:27.897724',134,'gojo','sukuna','satoru','M','testuser695@example.com','09667633015','1991-07-15',30,'1991-07-15','stringstring',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-23 08:18:41.152509','2021-07-23 08:18:41.154390',135,'bermylle','john','razon','M','bermyllerazon@ymail.com','09667633015','1999-12-30',21,'ahuisgdkasghjdjkasd','student',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-25 22:59:16.123490','2021-07-25 22:59:16.125523',136,'Sample','Sample','Sample','M','tatopi2092@britted.com','09876543210','1111-11-11',909,'sample addresss eyyyy','sample',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-26 00:02:18.208894','2021-07-26 00:02:18.211129',137,'Sample','Sample','Sample','M','xiviyog713@dmsdmg.com','09876543210','1111-11-11',909,'sample adddressssss','sample',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL),('2021-07-26 06:16:01.420852','2021-07-26 06:16:01.424181',142,'Neilll','Elijahh','Lingaa','M','neclinga001@gmail.com','09772845842','1998-09-01',22,'525 B M. Gonzaga St. Brgy. Hagdang Bato Itaas','Philippines',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'N',NULL);
/*!40000 ALTER TABLE `digiinsurance_insuree` ENABLE KEYS */;
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

-- Dump completed on 2021-07-28 10:44:29
