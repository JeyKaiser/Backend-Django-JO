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
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add custom user',6,'add_customuser'),(22,'Can change custom user',6,'change_customuser'),(23,'Can delete custom user',6,'delete_customuser'),(24,'Can view custom user',6,'view_customuser'),(25,'Can add color_ referencia',7,'add_color_referencia'),(26,'Can change color_ referencia',7,'change_color_referencia'),(27,'Can delete color_ referencia',7,'delete_color_referencia'),(28,'Can view color_ referencia',7,'view_color_referencia'),(29,'Can add creativo',8,'add_creativo'),(30,'Can change creativo',8,'change_creativo'),(31,'Can delete creativo',8,'delete_creativo'),(32,'Can view creativo',8,'view_creativo'),(33,'Can add foto',9,'add_foto'),(34,'Can change foto',9,'change_foto'),(35,'Can delete foto',9,'delete_foto'),(36,'Can view foto',9,'view_foto'),(37,'Can add linea',10,'add_linea'),(38,'Can change linea',10,'change_linea'),(39,'Can delete linea',10,'delete_linea'),(40,'Can view linea',10,'view_linea'),(41,'Can add status',11,'add_status'),(42,'Can change status',11,'change_status'),(43,'Can delete status',11,'delete_status'),(44,'Can view status',11,'view_status'),(45,'Can add sublinea',12,'add_sublinea'),(46,'Can change sublinea',12,'change_sublinea'),(47,'Can delete sublinea',12,'delete_sublinea'),(48,'Can view sublinea',12,'view_sublinea'),(49,'Can add tecnico',13,'add_tecnico'),(50,'Can change tecnico',13,'change_tecnico'),(51,'Can delete tecnico',13,'delete_tecnico'),(52,'Can view tecnico',13,'view_tecnico'),(53,'Can add tela',14,'add_tela'),(54,'Can change tela',14,'change_tela'),(55,'Can delete tela',14,'delete_tela'),(56,'Can view tela',14,'view_tela'),(57,'Can add tipo',15,'add_tipo'),(58,'Can change tipo',15,'change_tipo'),(59,'Can delete tipo',15,'delete_tipo'),(60,'Can view tipo',15,'view_tipo'),(61,'Can add variacion',16,'add_variacion'),(62,'Can change variacion',16,'change_variacion'),(63,'Can delete variacion',16,'delete_variacion'),(64,'Can view variacion',16,'view_variacion'),(65,'Can add linea sublinea',17,'add_lineasublinea'),(66,'Can change linea sublinea',17,'change_lineasublinea'),(67,'Can delete linea sublinea',17,'delete_lineasublinea'),(68,'Can view linea sublinea',17,'view_lineasublinea'),(69,'Can add collection',18,'add_collection'),(70,'Can change collection',18,'change_collection'),(71,'Can delete collection',18,'delete_collection'),(72,'Can view collection',18,'view_collection');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-10-20  0:10:24
