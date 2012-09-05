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
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_bda51c3c` (`group_id`),
  KEY `auth_group_permissions_1e014c8f` (`permission_id`),
  CONSTRAINT `group_id_refs_id_3cea63fe` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_a7792de1` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
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
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_e4470c6e` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_728de91f` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add content type',4,'add_contenttype'),(11,'Can change content type',4,'change_contenttype'),(12,'Can delete content type',4,'delete_contenttype'),(13,'Can add session',5,'add_session'),(14,'Can change session',5,'change_session'),(15,'Can delete session',5,'delete_session'),(16,'Can add site',6,'add_site'),(17,'Can change site',6,'change_site'),(18,'Can delete site',6,'delete_site'),(19,'Can add log entry',7,'add_logentry'),(20,'Can change log entry',7,'change_logentry'),(21,'Can delete log entry',7,'delete_logentry'),(22,'Can add Juventude Espírita',8,'add_juventudeespirita'),(23,'Can change Juventude Espírita',8,'change_juventudeespirita'),(24,'Can delete Juventude Espírita',8,'delete_juventudeespirita'),(25,'Can add coordenador',9,'add_coordenador'),(26,'Can change coordenador',9,'change_coordenador'),(27,'Can delete coordenador',9,'delete_coordenador'),(28,'Can add pagamento',10,'add_pagamento'),(29,'Can change pagamento',10,'change_pagamento'),(30,'Can delete pagamento',10,'delete_pagamento'),(31,'Can add confraternista',11,'add_confraternista'),(32,'Can change confraternista',11,'change_confraternista'),(33,'Can delete confraternista',11,'delete_confraternista'),(34,'Can add codigo cadastro',12,'add_codigocadastro'),(35,'Can change codigo cadastro',12,'change_codigocadastro'),(36,'Can delete codigo cadastro',12,'delete_codigocadastro');
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'admin','','','admin@admin.admin.admin','pbkdf2_sha256$10000$XaxvHhw12wvI$x8YQnPjgDgTPo9EY80UN6JxJah0nEown38n8oahdbes=',1,1,1,'2012-09-05 04:50:52','2012-09-02 17:32:31'),(2,'thiago','Thiago','Simões','thiago_snake@yahoo.com.br','pbkdf2_sha256$10000$AMdpXAlKigk1$C8wwZ+KfZBQSIltBlNSeonx2hTmMdayLndctwUZCuew=',1,1,1,'2012-09-03 22:19:55','2012-09-02 17:34:34'),(3,'arlen','Arlen','','arlen@gmail.com','pbkdf2_sha256$10000$0bBcPItWg59O$WC3Xsg+UFtN0hv8d59T3BQe0/5hc0w4nMd9kuEhE0GM=',0,1,0,'2012-09-03 21:14:06','2012-09-02 17:40:03'),(4,'felipe','Felipe','Torres','felizpetorres@gmail.com','pbkdf2_sha256$10000$OzXYbnFjHBYB$y/buDc2D4MC5wrMHKjIA4alPEJW7SZr5mqfkO+OWoJ8=',0,1,0,'2012-09-02 18:14:28','2012-09-02 18:14:15'),(5,'jose','José','Campos','jc@gmail.com','pbkdf2_sha256$10000$5K3Z1pTRZCIJ$lv22hJHMemMF+qFtn+hh2AI/9XQpGpvZp9r/4ec0WD4=',0,1,0,'2012-09-02 19:16:53','2012-09-02 18:32:37');
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
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_fbfc09f1` (`user_id`),
  KEY `auth_user_user_permissions_1e014c8f` (`permission_id`),
  CONSTRAINT `permission_id_refs_id_67e79cb` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_id_refs_id_f2045483` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
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
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2012-09-02 17:34:35',1,3,'2','thiago',1,''),(2,'2012-09-02 17:35:18',1,3,'2','thiago',2,'Modificado password, first_name, last_name, email, is_staff e is_superuser.'),(3,'2012-09-02 17:36:32',2,8,'1','Caravana de Luz',1,''),(4,'2012-09-02 18:31:31',2,11,'2','Felipe Torres (Caravana de Luz)',3,''),(5,'2012-09-02 19:28:48',2,11,'1','Arlen (Caravana de Luz)',2,'Modificado voluntario_manutencao.'),(6,'2012-09-02 19:30:29',2,8,'2','Os Mensageiros',1,''),(7,'2012-09-02 19:38:17',2,10,'26','Pago',1,''),(8,'2012-09-02 19:38:20',2,11,'3','José Campos (Caravana de Luz)',2,'Modificado pagamento_inscricao.'),(9,'2012-09-02 19:43:17',2,11,'3','José Campos (Caravana de Luz)',2,'Nenhum campo modificado.');
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
INSERT INTO `django_content_type` VALUES (1,'permission','auth','permission'),(2,'group','auth','group'),(3,'user','auth','user'),(4,'content type','contenttypes','contenttype'),(5,'session','sessions','session'),(6,'site','sites','site'),(7,'log entry','admin','logentry'),(8,'Juventude Espírita','inscricao','juventudeespirita'),(9,'coordenador','inscricao','coordenador'),(10,'pagamento','inscricao','pagamento'),(11,'confraternista','inscricao','confraternista'),(12,'codigo cadastro','inscricao','codigocadastro');
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
INSERT INTO `django_session` VALUES ('e5698e1ee5cc00e16d6e3a294f24d878','ZGQ0ZDI1YjMyMTE5YTdmODM0MTA1NzQ5ZWE0NjY4MjQ2NGYzODUxNTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-09-16 17:32:48'),('edbee52ffea2670af6a558298ee335b1','ZGQ0ZDI1YjMyMTE5YTdmODM0MTA1NzQ5ZWE0NjY4MjQ2NGYzODUxNTqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-09-16 17:44:56'),('f905b43fb6d91aa7145981d0d012a216','ZmZlZGYzMjkyZjdkM2VlNjhhNTRmZDkxOGY0ZDQwZWY0OWVjZTAzMzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==\n','2012-09-19 04:50:52');
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
  `confraternista` tinyint(1) NOT NULL,
  `nome` varchar(255) NOT NULL,
  `email` varchar(75) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `codigo` (`codigo`),
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
  `identidade` varchar(255) NOT NULL,
  `nome_cracha` varchar(255) NOT NULL,
  `juventude_id` int(11) NOT NULL,
  `data_nascimento` date DEFAULT NULL,
  `voluntario_manutencao` tinyint(1) DEFAULT '0',
  `autorizado` tinyint(1) NOT NULL,
  `sexo` varchar(1) DEFAULT NULL,
  `logradouro` varchar(255) DEFAULT NULL,
  `bairro` varchar(255) DEFAULT NULL,
  `cidade` varchar(255) DEFAULT NULL,
  `telefone` varchar(20) DEFAULT NULL,
  `contato_urgencia` varchar(255) DEFAULT NULL,
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
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario_id` (`usuario_id`),
  KEY `inscricao_confraternista_42efd821` (`juventude_id`),
  KEY `inscricao_confraternista_58e04385` (`pagamento_inscricao_id`),
  CONSTRAINT `juventude_id_refs_id_fa0cefe8` FOREIGN KEY (`juventude_id`) REFERENCES `inscricao_juventudeespirita` (`id`),
  CONSTRAINT `pagamento_inscricao_id_refs_id_4264dba1` FOREIGN KEY (`pagamento_inscricao_id`) REFERENCES `inscricao_pagamento` (`id`),
  CONSTRAINT `usuario_id_refs_id_57124cf9` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inscricao_confraternista`
--

LOCK TABLES `inscricao_confraternista` WRITE;
/*!40000 ALTER TABLE `inscricao_confraternista` DISABLE KEYS */;
INSERT INTO `inscricao_confraternista` VALUES (1,3,'MG15533263','Arlen',1,'1990-01-01',1,1,'M','Rua José Siqueira','Cidade Velha','Belo Horizonte','(23) 4234-2343','Pai','Pai','(29) 3487-2893','(23) 8947-8923',2005,'1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27',NULL,NULL,NULL,NULL,24),(3,5,'MG15533263','José Campos',1,'1998-11-16',0,1,'M','Rua José Siqueira','Cidade Velha','Belo Horizonte','(09) 3428-4098','Meu pai','Pai','(29) 3847-2893','(28) 9478-9234',2005,'30','','','','M',26);
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inscricao_coordenador`
--

LOCK TABLES `inscricao_coordenador` WRITE;
/*!40000 ALTER TABLE `inscricao_coordenador` DISABLE KEYS */;
INSERT INTO `inscricao_coordenador` VALUES (1,3,1);
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
  `nome_casa_espirita` varchar(80) NOT NULL,
  `logradouro` varchar(255) NOT NULL,
  `bairro` varchar(255) NOT NULL,
  `cidade` varchar(255) NOT NULL,
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
INSERT INTO `inscricao_juventudeespirita` VALUES (1,'Caravana de Luz','Pode falar com o Thiago em caso de dúvida\r\nTelefone: 9999-9999','Centro Espírita Caravana de Luz','Rua Bela Vista, 105','Padre Eustáquio','Belo Horizonte',10),(2,'Os Mensageiros','','','','','',3);
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
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inscricao_pagamento`
--

LOCK TABLES `inscricao_pagamento` WRITE;
/*!40000 ALTER TABLE `inscricao_pagamento` DISABLE KEYS */;
INSERT INTO `inscricao_pagamento` VALUES (1,NULL,'2012-09-02',2.50,NULL,0),(2,NULL,'2012-09-02',2.50,NULL,0),(3,NULL,'2012-09-02',2.50,NULL,0),(4,NULL,'2012-09-02',2.50,NULL,0),(5,NULL,'2012-09-02',2.50,NULL,0),(6,NULL,'2012-09-02',2.50,NULL,0),(7,NULL,'2012-09-02',2.50,NULL,0),(8,NULL,'2012-09-02',2.50,NULL,0),(9,NULL,'2012-09-02',2.50,NULL,0),(10,NULL,'2012-09-02',2.50,NULL,0),(11,NULL,'2012-09-02',2.50,NULL,0),(12,NULL,'2012-09-02',2.50,NULL,0),(13,NULL,'2012-09-02',2.50,NULL,0),(14,NULL,'2012-09-02',2.50,NULL,0),(15,NULL,'2012-09-02',2.50,NULL,0),(16,NULL,'2012-09-02',2.50,NULL,0),(17,NULL,'2012-09-02',2.50,NULL,0),(18,NULL,'2012-09-02',2.50,NULL,0),(19,NULL,'2012-09-02',2.50,NULL,0),(20,NULL,'2012-09-02',2.50,NULL,0),(21,NULL,'2012-09-02',2.50,NULL,0),(22,NULL,'2012-09-02',2.50,NULL,0),(23,NULL,'2012-09-02',2.50,NULL,0),(24,NULL,'2012-09-02',2.50,NULL,0),(25,NULL,'2012-09-02',1.50,NULL,0),(26,'0','2012-09-02',0.00,NULL,3);
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

-- Dump completed on 2012-09-05  1:51:29
