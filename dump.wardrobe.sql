-- MySQL dump 10.13  Distrib 5.5.47, for debian-linux-gnu (x86_64)
--
-- Host: mysql.server    Database: pg18$default
-- ------------------------------------------------------
-- Server version	5.5.42-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `pg18$default`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `pg18$default` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `pg18$default`;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `permission_id_refs_id_a7792de1` (`permission_id`),
  CONSTRAINT `group_id_refs_id_3cea63fe` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_a7792de1` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_message`
--

DROP TABLE IF EXISTS `auth_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id_refs_id_9af0b65a` (`user_id`),
  CONSTRAINT `user_id_refs_id_9af0b65a` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_message`
--

LOCK TABLES `auth_message` WRITE;
/*!40000 ALTER TABLE `auth_message` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  CONSTRAINT `content_type_id_refs_id_728de91f` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add message',5,'add_message'),(14,'Can change message',5,'change_message'),(15,'Can delete message',5,'delete_message');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pg18','','','paulgerard18@gmail.com','pbkdf2_sha256$24000$qQ6ERUT0N1qx$znmMExwwG1fbEzdvRhGGplbrTaSGjEABcOp5P8NJmNA=',1,1,1,'2016-03-03 14:16:39','2016-03-03 14:30:22');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `group_id_refs_id_f0ee9890` (`group_id`),
  CONSTRAINT `user_id_refs_id_831107f1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `group_id_refs_id_f0ee9890` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `permission_id_refs_id_67e79cb` (`permission_id`),
  CONSTRAINT `user_id_refs_id_f2045483` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `permission_id_refs_id_67e79cb` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id_refs_id_c8665aa` (`user_id`),
  KEY `content_type_id_refs_id_288599e6` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_288599e6` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_c8665aa` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2016-03-03 13:51:28',1,6,'4','débardeur',2,'Modification de name.'),(2,'2016-03-03 13:51:50',1,6,'17','col roulé',2,'Modification de name.'),(3,'2016-03-03 13:53:01',1,6,'21','combinaison 1 pièce',2,'Modification de name et warmth.'),(4,'2016-03-03 13:53:50',1,6,'47','talons compensés',2,'Modification de name.'),(5,'2016-03-03 13:54:23',1,6,'57','caleçon',2,'Modification de name.'),(6,'2016-03-03 13:54:43',1,6,'65','écharpe',2,'Modification de name.'),(7,'2016-03-03 13:55:17',1,6,'70','béret',2,'Modification de name.'),(8,'2016-03-03 13:55:32',1,6,'74','étole',2,'Modification de name.'),(9,'2016-03-03 13:55:47',1,6,'77','sac à main',2,'Modification de name.'),(10,'2016-03-03 13:55:56',1,6,'78','sac à dos',2,'Modification de name.');
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'log entry','admin','logentry'),(2,'permission','auth','permission'),(3,'group','auth','group'),(4,'user','auth','user'),(5,'message','auth','message'),(6,'','dressingManage','category');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dressingManage_category`
--

DROP TABLE IF EXISTS `dressingManage_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dressingManage_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `warmth` int(11) DEFAULT NULL,
  `area` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=80 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dressingManage_category`
--

LOCK TABLES `dressingManage_category` WRITE;
/*!40000 ALTER TABLE `dressingManage_category` DISABLE KEYS */;
INSERT INTO `dressingManage_category` VALUES (1,'chemise manches courtes\r',1,1),(2,'chemise manches longues\r',2,1),(3,'t-shirt\r',1,1),(4,'débardeur',1,1),(5,'caraco\r',1,1),(6,'chemisier\r',1,1),(7,'pull\r',3,1),(8,'manteau\r',4,1),(9,'gilet\r',3,1),(10,'veste\r',3,1),(11,'robe\r',3,1),(12,'veste de costume\r',3,1),(13,'haut de pyjama\r',0,1),(14,'sweat\r',4,1),(15,'parka\r',5,1),(16,'sous-pull\r',2,1),(17,'col roulé',4,1),(18,'tunique\r',2,1),(19,'combinaison\r',3,1),(20,'combinaison haut\r',5,1),(21,'combinaison 1 pièce',5,1),(22,'combishort\r',2,1),(23,'anorak\r',4,1),(24,'doudoune\r',4,1),(25,'kway\r',2,1),(26,'short\r',1,2),(27,'bermuda\r',2,2),(28,'pantalon\r',3,2),(29,'pantacourt\r',2,2),(30,'jogging\r',3,2),(31,'jean\r',3,2),(32,'legging\r',2,2),(33,'jupe\r',1,2),(34,'pyjama\r',0,2),(35,'salopette\r',3,2),(36,'combinaison\r',5,2),(37,'bas de costume\r',3,2),(38,'baskets\r',3,3),(39,'mocassins\r',3,3),(40,'escarpins\r',2,3),(41,'sandales\r',1,3),(42,'ballerines\r',2,3),(43,'pantoufle\r',0,3),(44,'chaussons\r',0,3),(45,'bottes\r',5,3),(46,'bottines\r',4,3),(47,'talons compensés',2,3),(48,'claquettes\r',1,3),(49,'tongs\r',1,3),(50,'derby\r',4,3),(51,'rangers\r',4,3),(52,'santiag\r',4,3),(53,'culotte\r',NULL,4),(54,'tanga\r',NULL,4),(55,'string\r',NULL,4),(56,'slip\r',NULL,4),(57,'caleçon',NULL,4),(58,'boxer\r',NULL,4),(59,'soutien-gorge\r',NULL,4),(60,'chaussettes\r',NULL,4),(61,'bas\r',NULL,4),(62,'collants\r',NULL,4),(63,'socquettes\r',NULL,4),(64,'bustier',NULL,4),(65,'écharpe',4,5),(66,'gants\r',3,5),(67,'bonnet\r',4,5),(68,'chapeau\r',2,5),(69,'casquette\r',1,5),(70,'béret',2,5),(71,'cagoule\r',5,5),(72,'mitaines\r',4,5),(73,'foulard\r',1,5),(74,'étole',2,5),(75,'noeud papillon\r',NULL,5),(76,'cravate\r',NULL,5),(77,'sac à main',NULL,5),(78,'sac à dos',NULL,5),(79,'pochette',NULL,5);
/*!40000 ALTER TABLE `dressingManage_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dressingManage_clothe`
--

DROP TABLE IF EXISTS `dressingManage_clothe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dressingManage_clothe` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `warmth` int(10) unsigned NOT NULL,
  `photo` varchar(30) DEFAULT NULL,
  `state` int(10) unsigned NOT NULL,
  `nbreUse` int(10) unsigned NOT NULL,
  `category_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `category_id_refs_id_a7b759a4` (`category_id`),
  KEY `user_id_refs_id_a028659f` (`user_id`),
  CONSTRAINT `user_id_refs_id_a028659f` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `category_id_refs_id_a7b759a4` FOREIGN KEY (`category_id`) REFERENCES `dressingManage_category` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dressingManage_clothe`
--

LOCK TABLES `dressingManage_clothe` WRITE;
/*!40000 ALTER TABLE `dressingManage_clothe` DISABLE KEYS */;
/*!40000 ALTER TABLE `dressingManage_clothe` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dressingManage_clothe_colors`
--

DROP TABLE IF EXISTS `dressingManage_clothe_colors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dressingManage_clothe_colors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `clothe_id` int(11) NOT NULL,
  `color_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `clothe_id` (`clothe_id`,`color_id`),
  KEY `color_id_refs_id_4e7446ea` (`color_id`),
  CONSTRAINT `color_id_refs_id_4e7446ea` FOREIGN KEY (`color_id`) REFERENCES `dressingManage_color` (`id`),
  CONSTRAINT `clothe_id_refs_id_ea787645` FOREIGN KEY (`clothe_id`) REFERENCES `dressingManage_clothe` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dressingManage_clothe_colors`
--

LOCK TABLES `dressingManage_clothe_colors` WRITE;
/*!40000 ALTER TABLE `dressingManage_clothe_colors` DISABLE KEYS */;
/*!40000 ALTER TABLE `dressingManage_clothe_colors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dressingManage_clothe_quantities`
--

DROP TABLE IF EXISTS `dressingManage_clothe_quantities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dressingManage_clothe_quantities` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `clothe_id` int(11) NOT NULL,
  `quantity_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `clothe_id` (`clothe_id`,`quantity_id`),
  KEY `quantity_id_refs_id_f9fca71c` (`quantity_id`),
  CONSTRAINT `quantity_id_refs_id_f9fca71c` FOREIGN KEY (`quantity_id`) REFERENCES `dressingManage_quantity` (`id`),
  CONSTRAINT `clothe_id_refs_id_d554eb70` FOREIGN KEY (`clothe_id`) REFERENCES `dressingManage_clothe` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dressingManage_clothe_quantities`
--

LOCK TABLES `dressingManage_clothe_quantities` WRITE;
/*!40000 ALTER TABLE `dressingManage_clothe_quantities` DISABLE KEYS */;
/*!40000 ALTER TABLE `dressingManage_clothe_quantities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dressingManage_clothe_themes`
--

DROP TABLE IF EXISTS `dressingManage_clothe_themes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dressingManage_clothe_themes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `clothe_id` int(11) NOT NULL,
  `theme_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `clothe_id` (`clothe_id`,`theme_id`),
  KEY `theme_id_refs_id_b3d971da` (`theme_id`),
  CONSTRAINT `theme_id_refs_id_b3d971da` FOREIGN KEY (`theme_id`) REFERENCES `dressingManage_theme` (`id`),
  CONSTRAINT `clothe_id_refs_id_77afb92b` FOREIGN KEY (`clothe_id`) REFERENCES `dressingManage_clothe` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dressingManage_clothe_themes`
--

LOCK TABLES `dressingManage_clothe_themes` WRITE;
/*!40000 ALTER TABLE `dressingManage_clothe_themes` DISABLE KEYS */;
/*!40000 ALTER TABLE `dressingManage_clothe_themes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dressingManage_color`
--

DROP TABLE IF EXISTS `dressingManage_color`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dressingManage_color` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `code` varchar(7) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dressingManage_color`
--

LOCK TABLES `dressingManage_color` WRITE;
/*!40000 ALTER TABLE `dressingManage_color` DISABLE KEYS */;
INSERT INTO `dressingManage_color` VALUES (1,'Blanc\r','#FFFFFF'),(2,'Noir\r','#000000'),(3,'Rouge\r','#FF0000'),(4,'Pourpre\r','#9E0E40'),(5,'Violet\r','#660099'),(6,'Indigo\r','#791CF8'),(7,'Bleu\r','#0000FF'),(8,'Turquoise\r','#25FDE9'),(9,'Vert\r','#00FF00'),(10,'Vert pomme\r','#34C924'),(11,'Jaune\r','#FFFF00'),(12,'Ocre\r','#DFAF2C'),(13,'Orange\r','#ED7F10'),(14,'Vert bouteille\r','#096A09'),(15,'Rose\r','#FD6C9E'),(16,'Marron\r','#582900'),(17,'Gris clair\r','#CECECE'),(18,'Gris\r','#606060'),(19,'Beige\r','#C8AD7F'),(20,'Kaki\r','#94812B'),(21,'Rouge carmin\r','#960018'),(22,'Saumon\r','#F88E55'),(23,'Ivoire\r','#FFFFD4'),(24,'Emeraude\r','#01D758');
/*!40000 ALTER TABLE `dressingManage_color` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dressingManage_parameter`
--

DROP TABLE IF EXISTS `dressingManage_parameter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dressingManage_parameter` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `weatherEnabled` tinyint(1) NOT NULL,
  `chilliness` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `user_id_refs_id_86383702` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dressingManage_parameter`
--

LOCK TABLES `dressingManage_parameter` WRITE;
/*!40000 ALTER TABLE `dressingManage_parameter` DISABLE KEYS */;
/*!40000 ALTER TABLE `dressingManage_parameter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dressingManage_pattern`
--

DROP TABLE IF EXISTS `dressingManage_pattern`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dressingManage_pattern` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dressingManage_pattern`
--

LOCK TABLES `dressingManage_pattern` WRITE;
/*!40000 ALTER TABLE `dressingManage_pattern` DISABLE KEYS */;
/*!40000 ALTER TABLE `dressingManage_pattern` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dressingManage_pattern_color`
--

DROP TABLE IF EXISTS `dressingManage_pattern_color`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dressingManage_pattern_color` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pattern_id` int(11) NOT NULL,
  `color_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `pattern_id` (`pattern_id`,`color_id`),
  KEY `color_id_refs_id_b112cc84` (`color_id`),
  CONSTRAINT `pattern_id_refs_id_6f13d3d5` FOREIGN KEY (`pattern_id`) REFERENCES `dressingManage_pattern` (`id`),
  CONSTRAINT `color_id_refs_id_b112cc84` FOREIGN KEY (`color_id`) REFERENCES `dressingManage_color` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dressingManage_pattern_color`
--

LOCK TABLES `dressingManage_pattern_color` WRITE;
/*!40000 ALTER TABLE `dressingManage_pattern_color` DISABLE KEYS */;
/*!40000 ALTER TABLE `dressingManage_pattern_color` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dressingManage_quantity`
--

DROP TABLE IF EXISTS `dressingManage_quantity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dressingManage_quantity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `quantity` int(10) unsigned NOT NULL,
  `color_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `color_id_refs_id_a407eb50` (`color_id`),
  CONSTRAINT `color_id_refs_id_a407eb50` FOREIGN KEY (`color_id`) REFERENCES `dressingManage_color` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dressingManage_quantity`
--

LOCK TABLES `dressingManage_quantity` WRITE;
/*!40000 ALTER TABLE `dressingManage_quantity` DISABLE KEYS */;
/*!40000 ALTER TABLE `dressingManage_quantity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dressingManage_theme`
--

DROP TABLE IF EXISTS `dressingManage_theme`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dressingManage_theme` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `userOwner_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `userOwner_id_refs_id_d2e5cc48` (`userOwner_id`),
  CONSTRAINT `userOwner_id_refs_id_d2e5cc48` FOREIGN KEY (`userOwner_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dressingManage_theme`
--

LOCK TABLES `dressingManage_theme` WRITE;
/*!40000 ALTER TABLE `dressingManage_theme` DISABLE KEYS */;
/*!40000 ALTER TABLE `dressingManage_theme` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-03-03 14:30:24
