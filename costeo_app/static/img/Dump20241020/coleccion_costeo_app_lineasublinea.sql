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
-- Table structure for table `costeo_app_lineasublinea`
--

DROP TABLE IF EXISTS `costeo_app_lineasublinea`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `costeo_app_lineasublinea` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `linea_id` bigint(20) NOT NULL,
  `sublinea_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `costeo_app_lineasubl_linea_id_18760dc2_fk_costeo_ap` (`linea_id`),
  KEY `costeo_app_lineasubl_sublinea_id_d25a9add_fk_costeo_ap` (`sublinea_id`),
  CONSTRAINT `costeo_app_lineasubl_linea_id_18760dc2_fk_costeo_ap` FOREIGN KEY (`linea_id`) REFERENCES `costeo_app_linea` (`id`),
  CONSTRAINT `costeo_app_lineasubl_sublinea_id_d25a9add_fk_costeo_ap` FOREIGN KEY (`sublinea_id`) REFERENCES `costeo_app_sublinea` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `costeo_app_lineasublinea`
--

LOCK TABLES `costeo_app_lineasublinea` WRITE;
/*!40000 ALTER TABLE `costeo_app_lineasublinea` DISABLE KEYS */;
INSERT INTO `costeo_app_lineasublinea` VALUES (1,1,5),(2,1,18),(3,1,19),(4,1,20),(5,1,21),(6,1,23),(7,1,25),(8,2,18),(9,2,19),(10,2,20),(11,2,21),(12,2,25),(13,3,1),(14,3,12),(15,3,14),(16,3,15),(17,3,16),(18,3,17),(19,4,6),(20,4,7),(21,4,8),(22,4,11),(23,4,13),(24,4,22),(25,4,26),(26,4,27),(27,5,1),(28,5,2),(29,5,3),(30,5,10),(31,6,9),(32,6,24),(33,7,4),(34,7,9);
/*!40000 ALTER TABLE `costeo_app_lineasublinea` ENABLE KEYS */;
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
