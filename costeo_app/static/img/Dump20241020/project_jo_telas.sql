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
-- Table structure for table `telas`
--

DROP TABLE IF EXISTS `telas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `telas` (
  `ï»¿id` int(11) DEFAULT NULL,
  `cod_color` int(11) DEFAULT NULL,
  `descripcion color` text DEFAULT NULL,
  `cod_tela` text DEFAULT NULL,
  `descripcion_tela` text DEFAULT NULL,
  `ancho_tela` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `telas`
--

LOCK TABLES `telas` WRITE;
/*!40000 ALTER TABLE `telas` DISABLE KEYS */;
INSERT INTO `telas` VALUES (1,1,'WHITE','TEN0007775','aaaa','1,5'),(2,2,'BLACK','TE00007866','bbbbb','1,6'),(3,3,'BPT','TE00007761','ccccc','1,35'),(4,4,'ANIS TRUFFLE','TE00007889','ddddd','1,53'),(5,5,'BEIGE','TE00007891','ffff','1,2'),(6,6,'AQUA/SALMON','TE00007886','eeee','1,55'),(7,7,'BLUE','TE00007820','gggg','1,47'),(8,8,'MALVA','TE00007867','hfghfghfgh','1,6'),(9,9,'SAND','TE00007785','hhhhh','1,48'),(10,10,'TAUPE','TE00007839','uiiii','1,46'),(11,11,'CAMEL','TEN0002704','jjjj','1,49'),(12,12,'CAOBA','TE00007837','kkk','1,46'),(13,13,'CAFE CLARO','TE00004332','llllllll','1,44'),(14,14,'CACAO','TE00006365','mmmmmmmm','1,39'),(15,15,'TABACO','TE00000328','nnnnnnnnnn','1,4'),(16,16,'CHOCOLATE','TE00007798','ooooooo','1,48'),(17,17,'MARRON','TE00007890','pppppppp','1,2'),(18,18,'CAFEE','TE00007975','qqqqqqqqq','1,2'),(19,19,'TERRACOTA','TE00007938','rrrrrrrr','1,2'),(20,20,'LADRILLO','TE00007912','sssss','1,48'),(21,21,'ROSADO','TE00007955','ttttttt','1,2'),(22,22,'PALO DE ROSA','TE00007974','uuuuuuuuu','1,2'),(23,23,'CORAL','TE00007907','vvvvvvvvvvv','1,48'),(24,24,'SALMON','TE00007250','qwwwwwwwwwwww','1,2'),(25,25,'ROSA VIEJO','TE00007897','xxxxxxxxxxxxxx','1,35'),(26,26,'NATURAL','TE00007921','yyyyyyyyyy','1,42'),(27,27,'MANDARINA','TE00007971','zzzzzzzzzzzzzzzasa','1,2'),(28,28,'NARANJA','TE00007929','aaaaaasssssssssss','1,44'),(29,29,'NARANJA OSCURO','TE00007916','ddddddddf','1,48'),(30,30,'MOSTAZA','TE00007913','fdfasdff','1,48');
/*!40000 ALTER TABLE `telas` ENABLE KEYS */;
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
