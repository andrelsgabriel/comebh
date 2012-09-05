-- MySQL dump 10.13  Distrib 5.5.25a, for Linux (x86_64)
--
-- Host: localhost    Database: comebh2
-- ------------------------------------------------------
-- Server version	5.5.25a

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
  UNIQUE KEY `group_id` (`group_id`,`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
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
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add content type',4,'add_contenttype'),(11,'Can change content type',4,'change_contenttype'),(12,'Can delete content type',4,'delete_contenttype'),(13,'Can add session',5,'add_session'),(14,'Can change session',5,'change_session'),(15,'Can delete session',5,'delete_session'),(16,'Can add site',6,'add_site'),(17,'Can change site',6,'change_site'),(18,'Can delete site',6,'delete_site'),(19,'Can add log entry',7,'add_logentry'),(20,'Can change log entry',7,'change_logentry'),(21,'Can delete log entry',7,'delete_logentry'),(22,'Can add juventude espirita',8,'add_juventudeespirita'),(23,'Can change juventude espirita',8,'change_juventudeespirita'),(24,'Can delete juventude espirita',8,'delete_juventudeespirita'),(25,'Can add coordenador',9,'add_coordenador'),(26,'Can change coordenador',9,'change_coordenador'),(27,'Can delete coordenador',9,'delete_coordenador'),(28,'Can add pagamento',10,'add_pagamento'),(29,'Can change pagamento',10,'change_pagamento'),(30,'Can delete pagamento',10,'delete_pagamento'),(31,'Can add confraternista',11,'add_confraternista'),(32,'Can change confraternista',11,'change_confraternista'),(33,'Can delete confraternista',11,'delete_confraternista'),(34,'Can add codigo cadastro',12,'add_codigocadastro'),(35,'Can change codigo cadastro',12,'change_codigocadastro'),(36,'Can delete codigo cadastro',12,'delete_codigocadastro');
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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'gpoesia','Gabriel','Poesia','gabriel.poesia@gmail.com','pbkdf2_sha256$10000$HOY1iz1UK5S0$qjSzAB8SHn847vC7YVxqo5gcozTbF1m46WRdM3o65eU=',1,1,1,'2012-09-02 12:11:44','2012-08-17 14:30:45'),(2,'fernandinha','Fernanda','Camila','cenanda@gmail.com','pbkdf2_sha256$10000$Xc71aKkpC4BF$W7WUqPn8bumxTxBX/hLUkLdCItOgCCwid/Jc3vIt7NQ=',0,1,0,'2012-09-02 05:23:55','2012-08-22 15:51:51'),(4,'doido','Mário','Oliveira Campos','jc@yahoo.com','pbkdf2_sha256$10000$nWkWw9LrM5m7$Yb+8C9aeIDSf9dTp8voJ3ZbeyB6SDMxlLJ3O7yD3p0E=',0,1,0,'2012-09-01 03:31:17','2012-08-23 13:04:21'),(5,'felipe','Felipe','Towers','','pbkdf2_sha256$10000$BUzYxmPigjaP$wnqMaqko0IMy/29Pgom9oGdPyIMRPFs/95W4zCr9pI8=',0,1,0,'2012-08-24 01:10:29','2012-08-24 00:18:37'),(6,'jose_alvés','José','Alves','jose@yahoo.com.br','pbkdf2_sha256$10000$yyN3miWTZoZK$vEpUPt3A5gQh/QpHNmQ1g2GfTr7RUFJhI31ccLeSXmQ=',0,1,0,'2012-08-24 00:30:20','2012-08-24 00:29:57'),(7,'joão_alves','João','Alves','joao@yahoo.com','pbkdf2_sha256$10000$pGQXuvx0gdZh$/mnCHHSI3Zs5Ou9eYiYbFYzgw/re2nG2mBnFVeGbqjs=',0,1,0,'2012-08-24 00:35:04','2012-08-24 00:33:27'),(8,'pessoa','Pessoa','','doido@teste.com.br','pbkdf2_sha256$10000$7z4fR4tgj9Kp$qy9enYvsfzrXRNSCN9hUCKC+cznx6jFpJnHXkQlOIxw=',0,1,0,'2012-08-30 13:03:29','2012-08-28 20:49:43'),(9,'juci','Jucelino','Dias','jd@google.com','pbkdf2_sha256$10000$Z3YO9podVOhW$enxmSeTITlYtgw7YHKDfPWA9TDjfWYUUp0BpqgNw9tk=',0,1,0,'2012-09-02 04:58:59','2012-09-02 04:58:54'),(10,'doidasso','Doidão','','doido@teste.com.br','pbkdf2_sha256$10000$x10m2S6m5ygr$8x7prd4pAJ5vxom8LA1/w5ug6aJQLfeKAUHwA/4+fhc=',0,1,0,'2012-09-02 05:27:31','2012-09-02 05:27:25');
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
  KEY `auth_user_groups_fbfc09f1` (`user_id`),
  KEY `auth_user_groups_bda51c3c` (`group_id`),
  CONSTRAINT `group_id_refs_id_f0ee9890` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_id_refs_id_831107f1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
  UNIQUE KEY `user_id` (`user_id`,`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
  KEY `django_admin_log_fbfc09f1` (`user_id`),
  KEY `django_admin_log_e4470c6e` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_288599e6` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_c8665aa` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2012-08-22 15:51:03',1,8,'1','José Campos',1,''),(2,'2012-08-22 15:51:15',1,8,'1','José Campos',2,'Nenhum campo modificado.'),(3,'2012-08-22 15:51:51',1,3,'2','fernandinha',1,''),(4,'2012-08-22 15:52:40',1,3,'2','fernandinha',2,'Modificado password, first_name, last_name e email.'),(5,'2012-08-22 15:53:55',1,9,'2','Fernanda (coordenador da juventude José Campos)',1,''),(6,'2012-08-22 17:18:24',1,3,'3','larissa',1,''),(7,'2012-08-22 17:21:26',1,3,'3','larissa',3,''),(8,'2012-08-24 00:16:25',1,8,'2','Os Mensageiros',1,''),(9,'2012-08-24 00:17:09',1,8,'2','Os Mensageiros',2,'Nenhum campo modificado.'),(10,'2012-08-24 00:18:37',1,3,'5','felipe',1,''),(11,'2012-08-24 00:18:49',1,9,'3',' (coordena a juventude Os Mensageiros)',1,''),(12,'2012-08-24 00:19:14',1,3,'5','felipe',2,'Modificado password, first_name e last_name.'),(13,'2012-08-24 01:10:16',1,8,'2','Os Mensageiros',2,'Modificado limite_confraternistas.'),(14,'2012-08-24 01:14:17',1,10,'1','Pagamento object',1,''),(15,'2012-09-02 12:12:20',1,8,'1','José Campos',3,''),(16,'2012-09-02 12:12:20',1,8,'2','Os Mensageiros',3,'');
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
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'permission','auth','permission'),(2,'group','auth','group'),(3,'user','auth','user'),(4,'content type','contenttypes','contenttype'),(5,'session','sessions','session'),(6,'site','sites','site'),(7,'log entry','admin','logentry'),(8,'juventude espirita','inscricao','juventudeespirita'),(9,'coordenador','inscricao','coordenador'),(10,'pagamento','inscricao','pagamento'),(11,'confraternista','inscricao','confraternista'),(12,'codigo cadastro','inscricao','codigocadastro');
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
  PRIMARY KEY (`session_key`),
  KEY `django_session_c25c2c28` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('2eac3eb86e1b2841275c205d3497b330','OWM4ZWE0Mzc5MGJkYmVkMmM2NmJmN2ZhZDQxOWY0NzEwZDg5ZTI2NTqAAn1xAVUKdGVzdGNvb2tp\nZVUGd29ya2VkcQJzLg==\n','2012-09-16 05:13:28'),('9cda50affffee74ced30cfe7c59c0fff','ZmZlZGYzMjkyZjdkM2VlNjhhNTRmZDkxOGY0ZDQwZWY0OWVjZTAzMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==\n','2012-09-16 12:11:44');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inscricao_codigocadastro`
--

DROP TABLE IF EXISTS `inscricao_codigocadastro`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inscricao_codigocadastro` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codigo` int(11) NOT NULL,
  `juventude_id` int(11) NOT NULL,
  `coordenador` tinyint(1) NOT NULL,
  `email` varchar(75) DEFAULT NULL,
  `nome` varchar(255) DEFAULT NULL,
  `confraternista` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `inscricao_codigocadastro_42efd821` (`juventude_id`),
  CONSTRAINT `juventude_id_refs_id_f9452d37` FOREIGN KEY (`juventude_id`) REFERENCES `inscricao_juventudeespirita` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inscricao_codigocadastro`
--

LOCK TABLES `inscricao_codigocadastro` WRITE;
/*!40000 ALTER TABLE `inscricao_codigocadastro` DISABLE KEYS */;
/*!40000 ALTER TABLE `inscricao_codigocadastro` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inscricao_confraternista`
--

DROP TABLE IF EXISTS `inscricao_confraternista`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inscricao_confraternista` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario_id` int(11) NOT NULL,
  `nome_cracha` varchar(255) NOT NULL,
  `juventude_id` int(11) NOT NULL,
  `data_nascimento` date DEFAULT NULL,
  `voluntario_manutencao` tinyint(1) NOT NULL,
  `autorizado` tinyint(1) NOT NULL,
  `sexo` varchar(1) DEFAULT NULL,
  `logradouro` varchar(255) DEFAULT NULL,
  `bairro` varchar(255) DEFAULT NULL,
  `cidade` varchar(255) DEFAULT NULL,
  `telefone` varchar(20) DEFAULT NULL,
  `parentesco_contato_urgencia` varchar(255) DEFAULT NULL,
  `telefone_contato_urgencia` varchar(255) DEFAULT NULL,
  `telefone2_contato_urgencia` varchar(255) DEFAULT NULL,
  `ano_ingresso_mocidade` int(10) unsigned DEFAULT NULL,
  `comebhs_anteriores` varchar(255) DEFAULT NULL,
  `dieta_especial` longtext,
  `uso_medicamento` longtext,
  `alergia` longtext,
  `tamanho_camisa` varchar(1) DEFAULT NULL,
  `pagamento_inscricao_id` int(11) DEFAULT NULL,
  `contato_urgencia` varchar(255) DEFAULT NULL,
  `identidade` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario_id` (`usuario_id`),
  KEY `inscricao_confraternista_42efd821` (`juventude_id`),
  KEY `inscricao_confraternista_58e04385` (`pagamento_inscricao_id`),
  CONSTRAINT `inscricao_confraternista_ibfk_1` FOREIGN KEY (`pagamento_inscricao_id`) REFERENCES `inscricao_pagamento` (`id`) ON DELETE SET NULL,
  CONSTRAINT `juventude_id_refs_id_fa0cefe8` FOREIGN KEY (`juventude_id`) REFERENCES `inscricao_juventudeespirita` (`id`),
  CONSTRAINT `usuario_id_refs_id_57124cf9` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inscricao_confraternista`
--

LOCK TABLES `inscricao_confraternista` WRITE;
/*!40000 ALTER TABLE `inscricao_confraternista` DISABLE KEYS */;
/*!40000 ALTER TABLE `inscricao_confraternista` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inscricao_coordenador`
--

DROP TABLE IF EXISTS `inscricao_coordenador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inscricao_coordenador` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario_id` int(11) NOT NULL,
  `juventude_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario_id` (`usuario_id`),
  KEY `inscricao_coordenador_42efd821` (`juventude_id`),
  CONSTRAINT `juventude_id_refs_id_d60e0f82` FOREIGN KEY (`juventude_id`) REFERENCES `inscricao_juventudeespirita` (`id`),
  CONSTRAINT `usuario_id_refs_id_99dae2eb` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inscricao_coordenador`
--

LOCK TABLES `inscricao_coordenador` WRITE;
/*!40000 ALTER TABLE `inscricao_coordenador` DISABLE KEYS */;
/*!40000 ALTER TABLE `inscricao_coordenador` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inscricao_juventudeespirita`
--

DROP TABLE IF EXISTS `inscricao_juventudeespirita`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inscricao_juventudeespirita` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(80) NOT NULL,
  `contato` longtext NOT NULL,
  `logradouro` varchar(255) NOT NULL,
  `bairro` varchar(255) NOT NULL,
  `cidade` varchar(255) NOT NULL,
  `nome_casa_espirita` varchar(80) NOT NULL,
  `limite_confraternistas` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nome` (`nome`),
  UNIQUE KEY `nome_casa_espirita` (`nome_casa_espirita`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inscricao_juventudeespirita`
--

LOCK TABLES `inscricao_juventudeespirita` WRITE;
/*!40000 ALTER TABLE `inscricao_juventudeespirita` DISABLE KEYS */;
/*!40000 ALTER TABLE `inscricao_juventudeespirita` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inscricao_pagamento`
--

DROP TABLE IF EXISTS `inscricao_pagamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inscricao_pagamento` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `transacao_pagseguro` varchar(255) DEFAULT NULL,
  `data` date NOT NULL,
  `valor_bruto` decimal(10,2) NOT NULL,
  `valor_liquido` decimal(10,2) DEFAULT NULL,
  `estado` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `transacao_pagseguro` (`transacao_pagseguro`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inscricao_pagamento`
--

LOCK TABLES `inscricao_pagamento` WRITE;
/*!40000 ALTER TABLE `inscricao_pagamento` DISABLE KEYS */;
INSERT INTO `inscricao_pagamento` VALUES (17,'9E884542-81B3-4419-9A75-BCC6FB495EF1','2012-08-30',140.00,136.65,3),(19,NULL,'2012-09-01',2.50,NULL,0),(20,NULL,'2012-09-01',1.50,NULL,0),(21,NULL,'2012-09-01',1.50,NULL,0),(22,NULL,'2012-09-01',1.50,NULL,0),(23,NULL,'2012-09-01',1.50,NULL,0);
/*!40000 ALTER TABLE `inscricao_pagamento` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-09-02 14:31:14
