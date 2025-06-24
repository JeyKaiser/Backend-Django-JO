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
-- Table structure for table `costeo_app_collection`
--

DROP TABLE IF EXISTS `costeo_app_collection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `costeo_app_collection` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `referencia` varchar(30) DEFAULT NULL,
  `codigoSapMD` varchar(30) DEFAULT NULL,
  `codigoSapPT` varchar(30) DEFAULT NULL,
  `nombreSistema` varchar(30) DEFAULT NULL,
  `descripcionColor` varchar(200) DEFAULT NULL,
  `codigoColor` varchar(20) DEFAULT NULL,
  `nombreReferente` varchar(20) DEFAULT NULL,
  `tallaje` varchar(50) DEFAULT NULL,
  `largo` varchar(50) DEFAULT NULL,
  `modista` varchar(100) DEFAULT NULL,
  `creativo_id` bigint(20) DEFAULT NULL,
  `fotoReferencia_id` bigint(20) DEFAULT NULL,
  `fotoTela_id` bigint(20) DEFAULT NULL,
  `linea_id` bigint(20) DEFAULT NULL,
  `status_id` bigint(20) DEFAULT NULL,
  `tecnico_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `costeo_app_collectio_creativo_id_1a28b307_fk_costeo_ap` (`creativo_id`),
  KEY `costeo_app_collectio_fotoReferencia_id_cca6def9_fk_costeo_ap` (`fotoReferencia_id`),
  KEY `costeo_app_collection_fotoTela_id_124b1eb2_fk_costeo_app_foto_id` (`fotoTela_id`),
  KEY `costeo_app_collection_linea_id_5f7e973f_fk_costeo_app_linea_id` (`linea_id`),
  KEY `costeo_app_collection_status_id_4af06b11_fk_costeo_app_status_id` (`status_id`),
  KEY `costeo_app_collectio_tecnico_id_8c21d6c3_fk_costeo_ap` (`tecnico_id`),
  CONSTRAINT `costeo_app_collectio_creativo_id_1a28b307_fk_costeo_ap` FOREIGN KEY (`creativo_id`) REFERENCES `costeo_app_creativo` (`id`),
  CONSTRAINT `costeo_app_collectio_fotoReferencia_id_cca6def9_fk_costeo_ap` FOREIGN KEY (`fotoReferencia_id`) REFERENCES `costeo_app_foto` (`id`),
  CONSTRAINT `costeo_app_collectio_tecnico_id_8c21d6c3_fk_costeo_ap` FOREIGN KEY (`tecnico_id`) REFERENCES `costeo_app_tecnico` (`id`),
  CONSTRAINT `costeo_app_collection_fotoTela_id_124b1eb2_fk_costeo_app_foto_id` FOREIGN KEY (`fotoTela_id`) REFERENCES `costeo_app_foto` (`id`),
  CONSTRAINT `costeo_app_collection_linea_id_5f7e973f_fk_costeo_app_linea_id` FOREIGN KEY (`linea_id`) REFERENCES `costeo_app_linea` (`id`),
  CONSTRAINT `costeo_app_collection_status_id_4af06b11_fk_costeo_app_status_id` FOREIGN KEY (`status_id`) REFERENCES `costeo_app_status` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `costeo_app_collection`
--

LOCK TABLES `costeo_app_collection` WRITE;
/*!40000 ALTER TABLE `costeo_app_collection` DISABLE KEYS */;
/*!40000 ALTER TABLE `costeo_app_collection` ENABLE KEYS */;
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
