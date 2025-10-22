-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: project_jo
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.20-MariaDB

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

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('e7pgyqgdv8exoeqc70bbba5vrb2d0amu','.eJxVjMsOwiAQRf-FtSHTKTDo0n2_gfAYpGogKe3K-O_apAvd3nPOfQnnt7W4rfPi5iQuYkBx-h2Djw-uO0l3X29NxlbXZQ5yV-RBu5xa4uf1cP8Oiu_lW0dLgBwpgbZoABJS1gqI8EykTQSNo8kqKNIj8GgsWraDIR0sU8hKvD_JITZt:1sxdZT:yArElSEnwdZ-p--lv_LmpsxlVI7Zu78QvRZq92R89dc','2024-10-21 02:34:03.865553'),('i3z1x2vdk7lyzfcnouodtzeqw4qcc3kd','.eJxVjDsOwjAQBe_iGlnx30tJnzNYXnuNA8iR4qRC3J1ESgHtm5n3ZiFuaw1bpyVMmV2ZZJffDWN6UjtAfsR2n3ma27pMyA-Fn7Tzcc70up3u30GNve519Aq1sJAtJF-oyKKNMsppJNDRWUQjkxqwoPS0q1qBcAII0GdANbDPF-LFN7c:1swvmg:wihu_vTQPhCx1WbHzSTnqRXHerFoUiZJpVwldqgIdOQ','2024-10-19 03:48:46.493548'),('qqq14cqk4xnwbesxny97eydht25p421y','.eJxVjEEOwiAQRe_C2hCngDAu3XsGAjODVA1NSrsy3l2bdKHb_977LxXTutS4dpnjyOqsQB1-t5zoIW0DfE_tNmma2jKPWW-K3mnX14nledndv4Oaev3WeDSCwJYYfMjeA4JxCATEnEsImchlbwOBhEIF_SkNQiVhMMXZgdX7A-gNOH4:1szne6:fIUzpSJmkS_TNsuqCUIALKrIRJMWh-PuARJbZnuz_b0','2024-10-27 01:43:46.121496'),('xizc76q3zb8bgtggavlo62jy7pyfm8l2','.eJxVjEsOwjAMBe-SNYqapE1sluw5Q-TaLi2gROpnhbg7VOoCtm9m3stk2tYxb4vOeRJzNq4xp9-xJ35o2Yncqdyq5VrWeertrtiDLvZaRZ-Xw_07GGkZv3XySKIDNBgDEyt7iBCS84xKnBwNAUB837mEIimKtKDQaWgRQxqieX8AFP44MQ:1sxdVL:ug2kjqocgFePh313eG1VE1No0NWjJqoSFyr8YtXRp1I','2024-10-21 02:29:47.411754');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-10-20  0:10:20
