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
-- Table structure for table `digiinsurance_user`
--

DROP TABLE IF EXISTS `digiinsurance_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `digiinsurance_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `email` varchar(128) NOT NULL,
  `role` varchar(2) NOT NULL,
  `photo` varchar(100) DEFAULT NULL,
  `step` smallint unsigned NOT NULL,
  `info_submitted` tinyint(1) NOT NULL,
  `is_verified` tinyint(1) NOT NULL,
  `country_code` varchar(5) DEFAULT NULL,
  `mobile_number` varchar(16) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  CONSTRAINT `digiinsurance_user_chk_1` CHECK ((`step` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=145 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digiinsurance_user`
--

LOCK TABLES `digiinsurance_user` WRITE;
/*!40000 ALTER TABLE `digiinsurance_user` DISABLE KEYS */;
INSERT INTO `digiinsurance_user` VALUES (1,'pbkdf2_sha256$216000$lA9XEyqaaEIP$+A5xatHRZcLTpVSCm1NS5aGWsO8NaIQWH5RLgu2kazI=','2021-07-27 06:42:21.730458',1,'admin','','',1,1,'2021-07-14 15:46:26.923252','developer@questronix.com.ph','','',1,0,0,'+63','09174523145'),(2,'pbkdf2_sha256$216000$kHNoj65yovpX$8FT9foT97okd4JWDE3m+bIKC1t174vx0NNByDLD2Y7c=','2021-07-28 02:36:13.818047',1,'gojosatoru','Gojo','Satoru',0,1,'2021-07-15 00:56:04.827752','gojo@example.com','IN','users/2_0jOwWHY.jpg',1,1,1,'+63','09667633011'),(4,'pbkdf2_sha256$216000$92dy8xwiHSgI$2XOzM2c09MPWIf2OTt6jXlYWixaVPQbetCNfDl3LMbs=','2021-07-28 02:39:01.785344',1,'vankeith','','',1,1,'2021-07-15 03:23:45.362855','q@q.com','AD','',1,1,1,'+63','09174526356'),(5,'pbkdf2_sha256$216000$mtgI1hG5XHKC$bgS8IKkt1Fg0NTQPZtHpYdog/cJ4w6NCIy3biUbIHdc=','2021-07-28 00:47:51.764455',1,'Alloybronya','','',1,1,'2021-07-15 03:25:41.849119','qq@qq.com','AD','',1,1,1,'+63','09174523699'),(6,'pbkdf2_sha256$216000$C9mRwzu4rKjI$VgxWU575fCIlu08RvKa1TveSqNmuWqmN8bYixmUnPSI=','2021-07-28 02:37:26.927581',1,'caloycoste1','','',1,1,'2021-07-15 03:39:25.078875','caloycoste@gmail.com','AD','',1,0,1,'+63','09976583355'),(7,'pbkdf2_sha256$216000$0XTTGkyE4E63$UDPF0evnQNak809rkohXCPi18O4T7t+gIP7ywJQ8pvo=',NULL,0,'johnnysins','johnny','sins',1,1,'2021-07-15 03:56:43.870698','v@v.com','IN','',1,0,0,'+63','09175214563'),(16,'pbkdf2_sha256$260000$RqrGDk7JR5ksC0BHYZWKCh$2UURc39TzqC3jbl8qG2fSNmVpbTYNGHrzfk/RDkXoz0=','2021-07-21 05:38:10.217937',1,'2ndcabrera23','LEXTER KING','CABRERA',1,1,'2021-07-15 05:56:32.690516','2ndcabrera23@gmail.com','AD','',1,0,1,'+63','09954532847'),(17,'pbkdf2_sha256$260000$7VMvQzTEzD7pnNRKDv5xVz$foi5nBq4pCWGVHyb3JSTOJSZw6MXIk2PhBSKSMxKkIM=','2021-07-20 06:14:45.077242',0,'2ndcabrera24','LEXTER KING','CABRERA',0,1,'2021-07-15 06:07:38.519260','2ndcabrera24@gmail.com','IN','',1,0,0,'+63','09954532848'),(18,'pbkdf2_sha256$260000$1TTA7xAaRYty9GgIYvXsvN$7iwVmmeRWLGmPl8cnr4t2N+uJFKFGDZHHgPo3l/gAME=','2021-07-21 05:21:31.728939',0,'2ndcabrera25','lex','cabrera',0,1,'2021-07-15 07:04:24.342505','2ndcabrera25@gmail.com','IN','',1,0,0,'+63','09954532849'),(23,'pbkdf2_sha256$260000$iqm6wnRE9m2gnGrM6SICHX$UAe2+eDC3xy2OVyhWIEXZjDOqGzX/F7JY7KMJfYJTiU=',NULL,0,'2ndcabrera26','lex','cabrera',0,1,'2021-07-15 07:28:51.757046','2ndcabrera26@gmail.com','IN','',1,0,0,'+63','09954532850'),(34,'pbkdf2_sha256$216000$f4n4ljYptQjH$b8L3N1bf9IMMyRPO9zzKx5Kp+n+vB7/J8YNg7maVu4w=',NULL,0,'loriviii','Lorenzo','Valentino',0,1,'2021-07-15 08:22:20.678570','renz.valentino@gmail.com','IN','',1,0,0,'+63','09267326782'),(80,'pbkdf2_sha256$216000$Pmn5Rw2SwXrg$6rqO6XjouRLelGWH2I8NRo6x+f6lTmIR1Yt7hfhspmg=','2021-07-15 14:46:59.858668',0,'loriviii2','Lorenzo','Valentino',0,1,'2021-07-15 14:00:31.510469','renz.valentino3@gmail.com','IN','',1,0,0,'+63','09267326782'),(81,'pbkdf2_sha256$216000$xbOrIgkc01Fo$A07d1HQ5h7ONl9SQeKsYfMekkRsJlBetw3y1POw254I=',NULL,0,'loriviii3','Lorenzo','Valentino',0,1,'2021-07-15 14:05:58.038956','renz.valentino+1@gmail.com','IN','',1,0,0,'+63','09267326782'),(82,'pbkdf2_sha256$216000$gWELZ4z2ZBym$ubdS70WOciFzUCgjNXW9nXHZYUCkHhQrp6T/JB7p89c=',NULL,0,'loriviii4','Lorenzo','Valentino',0,1,'2021-07-15 14:07:17.131987','renz.valentino+2@gmail.com','IN','',1,0,0,'+63','09267326782'),(83,'pbkdf2_sha256$216000$xzbSNdPU27Du$p2J7U9qzbvpwRyxWW65hvrSTD8+fQ0Ovsk7zNB19Q0U=',NULL,0,'loriviii5','Lorenzo','Valentino',0,1,'2021-07-15 14:16:27.245811','renz.valentino+3@gmail.com','IN','',1,0,0,'+63','09267326782'),(84,'pbkdf2_sha256$216000$uY0BWIyUN0Qc$3lkeEnGoTXqnEWFuXFY2OkjOFJInXaPTMkDzpnrm3IM=',NULL,0,'loriviii6','Lorenzo','Valentino',0,1,'2021-07-15 14:22:36.309084','renz.valentino+4@gmail.com','IN','',1,0,0,'+63','09267326782'),(85,'pbkdf2_sha256$216000$lZ1GAR8jRRA2$mlzPy8xFeQqCRpQL0/o3tUX1s/k7mRsIktl2TyoRe38=','2021-07-28 02:34:05.606942',0,'carlocoste','Caloy','Coste',0,1,'2021-07-16 01:11:59.007747','carlo_coste@questronix.com.ph','IN','',1,0,1,'+63','09976583355'),(86,'pbkdf2_sha256$260000$yzmw8gu41BvfLjT7z5kPPa$q2WUQwVyrC8SPaverIu3j5qNqePUzutrkw/i+ReXUis=',NULL,0,'2ndcabrera27','lex','cabrera',0,1,'2021-07-16 01:16:49.626679','2ndcabrera27@gmail.com','IN','',1,0,0,'+63','09954532851'),(90,'pbkdf2_sha256$216000$eAYPHQcUrifm$ybbhqBsno2UBfcM38ptrSkHVQpWHAlh25p9323JOBJ0=','2021-07-16 01:42:48.825014',0,'carmela_labiaga','','',0,1,'2021-07-16 01:34:05.983101','carmela@example.com','IN','users/90_wWTHTy7.jpg',1,1,1,'+63','09174523658'),(97,'pbkdf2_sha256$216000$nni2I36XPlaT$qGjpKaehqoIXykMZ3jA0xQYUlkSWXHr36SOrnf5gpOI=','2021-07-16 03:32:03.745123',0,'harvey2','Harvey','Specter',0,1,'2021-07-16 03:30:58.598521','vkalmazan@gmail.com','IN','',1,0,1,'+63','09145236545'),(98,'pbkdf2_sha256$216000$6AmsmA2xF967$kV28Focz7RnTG1IEmInCpaBlxp9oLYXd4+UF38HqvQo=','2021-07-27 06:45:36.338743',0,'Setsunasekai','Neill Elijah','Linga',0,1,'2021-07-16 03:50:23.940373','amenxd01@gmail.com','IN','',1,0,1,'+63','09772845842'),(99,'pbkdf2_sha256$216000$knhpFPbmFke8$QFNfim6xcUWgUlg69/PgJuHDp4n0VsoZQ37PwaIVOos=','2021-07-28 02:42:07.334506',0,'james123','James Andrew','Cornes',0,1,'2021-07-16 03:56:59.450701','rexcornes@yahoo.com','IN','',1,0,1,'+63','09274723934'),(100,'pbkdf2_sha256$216000$MVxlVYX12Oqp$+LqsGCt61vZNg/2xT9mnN5xUXL0HmTHRQna+tUDPPZg=','2021-07-26 06:44:35.840615',0,'neilchan','Neil','Chan',0,1,'2021-07-16 04:52:53.127719','chanbu0217@gmail.com','IN','',1,0,0,'+63','09996412591'),(102,'pbkdf2_sha256$216000$kJmJqeJC8D8o$16c7ZfpkekVwBFjkyUSdIpzRG3wbNuz0S0jRdQO02hU=','2021-07-22 08:04:01.179902',0,'nanaminn','I Am','Client',0,1,'2021-07-16 05:01:29.071429','iamclient@gmail.com','IN','',1,0,0,'+63','09987654321'),(103,'pbkdf2_sha256$216000$UvbNaptspudO$bAwJgK7AxJwQf7FooodeD895YHpji8GME28mXPrvsvI=','2021-07-26 03:36:53.224565',0,'jakeyperalta','Jacob','Peralta',0,1,'2021-07-16 06:06:04.759734','angel.dummy.test@gmail.com','IN','',1,0,1,'+63','09209746421'),(104,'',NULL,1,'jakeyadmin','','',1,1,'2021-07-16 06:13:36.999448','angel.maas360@gmail.com','AD','',1,0,0,'+63','09209746421'),(105,'',NULL,1,'sd','','',1,1,'2021-07-16 06:18:39.104202','angel.maas60@gmail.com','AD','',1,0,0,'+63','09209746421'),(106,'pbkdf2_sha256$216000$skxb8efYGLia$Didjqz243BAyUG1s1Fcyrwryi1E/9TOvY6jcWC4sSfU=','2021-07-27 13:44:54.291315',0,'algaringo','Angelu','Garingo',0,1,'2021-07-16 07:12:45.156166','algaringo@gmail.com','IN','',1,0,1,'+63','09876543210'),(107,'pbkdf2_sha256$216000$0uemHMZWB8aH$D2rUpDX/F8bnKkk9Hs2X7l2Bd8bLdeIihn5Yg5e1hHc=','2021-07-27 13:44:58.945654',0,'qwertyuiop','Angelu','Garingo',0,1,'2021-07-21 01:53:52.399631','angelugaringo@gmail.com','IN','',1,0,1,'+63','09876543211'),(108,'',NULL,1,'testuser','','',1,1,'2021-07-21 06:17:54.396911','potatopieces17@gmail.com','AD','',1,0,0,'+63','09213548312'),(109,'pbkdf2_sha256$216000$0U7QBoDTZxtE$kopSXzNJ6RMRpLdJd9A3JKcedotYONaT66L81/DtpAg=','2021-07-22 05:55:51.055227',0,'Osama911','Elijah Cephia','Bagio',0,1,'2021-07-21 06:18:21.335484','elijah.cephia_bagio@questronix.com.ph','IN','',1,0,0,'+63','097856432546'),(110,'pbkdf2_sha256$216000$ZUznHxuPTFVB$Xj2CJzENMU5X1w5Q/5eRnOO8t4Ttrvx7uBlOMnOa4P0=','2021-07-23 04:20:09.319243',0,'rmfquijada','rea','quijada',0,1,'2021-07-21 06:19:08.646060','rmfquijada@gmail.com','IN','',1,0,0,'+63','09267371300'),(111,'pbkdf2_sha256$216000$o0CgQUVG0Tv6$v9nOHwLyYTt3PXRKNnZIsoFmm5qD/E2e2lcJHBkkNzM=','2021-07-23 05:41:12.607500',0,'reenamyka','Reena','De Guzman',0,1,'2021-07-21 06:30:45.245130','rjdeguzman@upedu.ph','IN','',1,0,1,'+63','09213548312'),(112,'pbkdf2_sha256$216000$CamXzsvjhrhL$iK3Z0knIcFcxT/oswKeytVfvs39+La1Myjn2bhf7hCA=','2021-07-27 06:58:57.262999',0,'burazon','asdasdasdasdasdasd','asdasdasdasd',0,1,'2021-07-21 08:21:08.084089','burazon1@up.edu.ph','IN','',1,0,1,'+63','09667633015'),(114,'pbkdf2_sha256$216000$I7CBuhcOuhrL$DiKKOQ/Ie2NQPdMObc2qMTpldk1Qve12gGKGdpbYMPY=','2021-07-22 06:55:55.742659',0,'testuser@','Maria','Smith',0,1,'2021-07-21 08:30:10.585153','psylacantos.trial@gmail.com','IN','',1,0,0,'+63','09190745222'),(116,'pbkdf2_sha256$216000$12On5h2JGRbX$RqKJt05VwM+ZonIp9s1iejUREAW6wVib0FgBVYPqQi8=',NULL,0,'testuser123','Reena Myka','De Guzman',0,1,'2021-07-21 08:37:44.463736','reenamyka@yahoo.com','IN','',1,0,0,'+63','09213548312'),(121,'pbkdf2_sha256$216000$eA5yRHpY9qoo$7eu3eBumQ+Bifm8cWp15K00F7uHKaWcRXGIuZaOKtCQ=','2021-07-23 01:31:46.696196',0,'AllenDee','Allen','Denopol',0,1,'2021-07-22 04:23:39.819077','jpdenopol@up.edu.ph','IN','',1,0,1,'+63','09062755044'),(122,'pbkdf2_sha256$260000$zuTPflKX6a6bN3TM3gf61M$uqrDBl7fhVvt+Qc9GqMYd6ysp2D6GUM5XVLks6kTaxQ=',NULL,0,'2ndcabrera28','','',0,1,'2021-07-22 06:20:56.383577','2ndcabrera28@gmail.com','AD','',1,0,0,'+63','09174523655'),(123,'pbkdf2_sha256$216000$36SachIzXn4H$AKGt3x42XyHsP8wpStOwUNZbd+0RfeN0mfRVAQcg3Qk=','2021-07-22 06:57:54.716483',0,'testuser!','Test','User',0,1,'2021-07-22 06:56:56.897326','sample@gmail.com','','',1,0,0,'+63','09123457898'),(124,'pbkdf2_sha256$216000$WTZ7dxmEItnZ$N5UF7DcRyoUEpjbbvbYhdJAgq2+n0tuBRB/q63VoYhg=',NULL,0,'testuser#','Test','User',0,1,'2021-07-22 06:57:18.454357','sample2@gmail.com','','',1,0,0,'+63','09123457898'),(125,'pbkdf2_sha256$260000$fzrtYd6SG0Y9PP89kvJ85o$/ov8rTd4UNOswSXtURZe+wYNa7kCKDoqHpWbaPORo9g=',NULL,0,'lex','lex','lex',0,1,'2021-07-22 09:05:48.646533','lex@gmail.com','IN','',1,0,0,'+63','09954532847'),(126,'pbkdf2_sha256$216000$GT2yGZqFBFP6$02AtdrlXJwp4SW4hNW/xKEoXOFZ4pCDYxWqOjyfsg4g=',NULL,0,'user_test','gojo','satoru',0,1,'2021-07-23 02:11:28.979074','testuser@example.com','IN','',1,0,0,'+63','09667633015'),(127,'pbkdf2_sha256$216000$jJNsAqpBSIOh$R9q/Yrtlu/ZaeD/h/nITKCbLOyneF2UlP8vSTEbdQrk=','2021-07-23 02:16:24.970689',0,'usertest01','usertest','usertes',0,1,'2021-07-23 02:15:48.105079','bermylle@gmail.com','IN','',1,0,1,'+63','09667633015'),(128,'pbkdf2_sha256$260000$vbe2GmkIktAMIEwyAcr0kO$7JyfqFPodtzG81VFb3vovyCE8jKmmpRB7g9wqmtX8gk=',NULL,0,'2ndcabrera30@gmail.com','','',0,1,'2021-07-23 02:56:10.854086','2ndcabrera30@gmail.com','IN','',1,0,0,'+63','09959959595'),(129,'pbkdf2_sha256$216000$Edog5K7HyMsy$wi3rlFqJzMdscTRuOjJ6JAXsBK9drWOs4+XQGU49OkM=','2021-07-23 03:46:18.778713',0,'carmela_marie_labiaga','','',0,1,'2021-07-23 03:02:32.214824','carmela_marie@example.com','IN','',1,1,0,'+63','9295105094'),(130,'pbkdf2_sha256$216000$bzMjJZOKDUbJ$IAWKGvw89ev/B1StNmP3iO+Kd851YM19paq+mejVE6s=',NULL,0,'testuser05','gojo','satoru',0,1,'2021-07-23 03:35:12.560352','testuser05@example.com','IN','',1,0,0,'+63','09667633015'),(131,'pbkdf2_sha256$216000$Yyj9UPQEL8Ia$vKbkGNR1uI8NsLWwJXHjMDxn4Y9wNN/byLsuPQVZF+Y=',NULL,0,'testuser699','gojo','satoru',0,1,'2021-07-23 04:54:21.823644','testuser699@example.com','IN','',1,0,0,'+63','09667633015'),(132,'pbkdf2_sha256$216000$VwALWLODPo1y$NBFhhv66q+oJf9rQqlztwex6GNE+HSLM/sJQ4+IItjM=','2021-07-23 06:03:13.859565',0,'reenamyka1','Reena','De Guzman',0,1,'2021-07-23 06:00:43.163523','rjdeguzman@up.edu.ph','IN','',1,0,0,'+63','09213548312'),(133,'pbkdf2_sha256$216000$VeVEK1budQs1$daMrahC06LvAIKJ8bnHnDe7theE1hdWEywLrUVoPyIM=',NULL,0,'testuser69','gojo','satoru',0,1,'2021-07-23 07:13:15.100029','testuser69@example.com','IN','',1,0,0,'+63','09667633015'),(134,'pbkdf2_sha256$216000$3TyY7bITKsJu$J+PZGoaFO9g5TFAfCr4GCPODNzeNPFRzJCowjsVSNrM=',NULL,0,'testuser695','gojo','satoru',0,1,'2021-07-23 08:15:27.705986','testuser695@example.com','IN','',1,0,0,'+63','09667633015'),(135,'pbkdf2_sha256$216000$NjNEOIrLGLKX$Mz/HhO0G+qHvH5gY5y8xW7QK7/58vlY47gByINQvhr8=','2021-07-23 08:20:37.248715',0,'bermyller','bermylle','razon',0,1,'2021-07-23 08:18:40.995057','bermyllerazon@ymail.com','IN','',1,0,1,'+63','09667633015'),(136,'pbkdf2_sha256$216000$MAXQKy0kcWM6$M/ZT+nv/hmlR12vHqd3yf0njAAJtFlGrRBCmpSCAXV4=','2021-07-28 00:48:08.269296',0,'guest0101','Sample','Sample',0,1,'2021-07-25 22:59:15.972407','tatopi2092@britted.com','IN','',1,0,1,'+63','09876543210'),(137,'pbkdf2_sha256$216000$niEfBCb3Oa0g$8aTWJstZebK02F2tMMJ8awQXULtoeCztWyGrKBQnnr4=','2021-07-26 21:34:42.827655',0,'Sample1!','Sample','Sample',0,1,'2021-07-26 00:02:18.048669','xiviyog713@dmsdmg.com','IN','',1,0,1,'+63','09876543210'),(142,'pbkdf2_sha256$216000$dxgGjsmRiTkl$q613AVI3kQ6AvcfdSCZG4CGD5jK89E4wezUmeRwCGu0=','2021-07-26 06:44:41.186744',0,'testing123','Neilll','Lingaa',0,1,'2021-07-26 06:16:01.251379','neclinga001@gmail.com','IN','',1,0,1,'+63','09772845842'),(143,'pbkdf2_sha256$216000$h3aSFDc9Pgep$MUPvPlWfrQG+ZFmL4/eTX35/Vfd2cfjjjsFo9kApS8k=','2021-07-27 05:26:51.821150',0,'gojosss','gojo','satoru',0,1,'2021-07-27 05:06:42.950088','ggggggg@example.com','IN','',1,0,0,'+63','09667633015'),(144,'pbkdf2_sha256$216000$A8Aj6qeKMoyB$cvOI+TMHwM37rrjQh93OBM5pgpUCBoebYBM0kNsUY70=','2021-07-28 01:09:27.201797',0,'Guest0101!','Sample','Sample',0,1,'2021-07-28 00:51:18.245999','fulmegekni@biyac.com','','',1,0,0,'+63','09271376796');
/*!40000 ALTER TABLE `digiinsurance_user` ENABLE KEYS */;
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

-- Dump completed on 2021-07-28 10:44:07
