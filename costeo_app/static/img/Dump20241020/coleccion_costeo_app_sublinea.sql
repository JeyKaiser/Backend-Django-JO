-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: coleccion
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
-- Table structure for table `costeo_app_sublinea`
--

DROP TABLE IF EXISTS `costeo_app_sublinea`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `costeo_app_sublinea` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre_sublinea` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre_sublinea` (`nombre_sublinea`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `costeo_app_sublinea`
--

LOCK TABLES `costeo_app_sublinea` WRITE;
/*!40000 ALTER TABLE `costeo_app_sublinea` DISABLE KEYS */;
INSERT INTO `costeo_app_sublinea` VALUES (18,'ANKLE'),(2,'BIKINI BOTTOM'),(3,'BIKINI TOP'),(1,'BODYSUIT'),(7,'CARDIGAN'),(27,'COAT'),(17,'CROP TOP'),(22,'JACKET'),(4,'JUMPSUIT'),(26,'KIMONO'),(21,'MAXI'),(19,'MIDI'),(20,'MINI'),(10,'ONEPIECE'),(24,'PANT'),(12,'POLO'),(11,'PONCHO'),(16,'SHIRT'),(5,'SHIRTDRESS'),(9,'SHORT'),(13,'SWEATER'),(15,'T-SHIRT'),(14,'TOP'),(8,'TRENCHCOAT'),(23,'TUNIC'),(6,'VEST'),(25,'WRAP');
/*!40000 ALTER TABLE `costeo_app_sublinea` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-10-20  0:10:23
