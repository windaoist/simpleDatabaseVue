-- MySQL dump 10.13  Distrib 9.0.1, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: myDatabase
-- ------------------------------------------------------
-- Server version	9.0.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `project`
--

DROP TABLE IF EXISTS `project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project` (
  `project_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '项目编号',
  `project_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '项目名称',
  `project_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '项目内容',
  `project_application_status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '未申报',
  `project_approval_status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '未审批',
  `project_acceptance_status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '未验收',
  PRIMARY KEY (`project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project`
--

LOCK TABLES `project` WRITE;
/*!40000 ALTER TABLE `project` DISABLE KEYS */;
INSERT INTO `project` VALUES ('PJT20250001','创意文化关键技术研究与应用','本项目围绕智能制造领域的关键问题，开展深入研究，推动成果转化。','未申报','未审批','未验收'),('PJT20250002','新型显示关键技术研究与应用','本项目围绕现代服务业领域的关键问题，开展深入研究，推动成果转化。','未申报','未审批','未验收'),('PJT20250003','聚变能源关键技术研究与应用','本项目围绕网络与信息安全领域的关键问题，开展深入研究，推动成果转化。','申报通过','审批通过','未验收'),('PJT20250004','高端装备关键技术研究与应用','本项目围绕大消费领域领域的关键问题，开展深入研究，推动成果转化。','未申报','未审批','未验收'),('PJT20250005','新材料关键技术研究与应用','本项目围绕人工智能领域的关键问题，开展深入研究，推动成果转化。','申报通过','未审批','未验收'),('PJT20250006','新能源汽车和智能网联汽车关键技术研究与应用','本项目围绕新能源汽车和智能网联汽车领域的关键问题，开展深入研究，推动成果转化。','未申报','未审批','未验收'),('PJT20250007','新一代信息技术关键技术研究与应用','本项目围绕大消费领域领域的关键问题，开展深入研究，推动成果转化。','未申报','未审批','未验收'),('PJT20250008','光伏及新能源关键技术研究与应用','本项目围绕人工智能领域的关键问题，开展深入研究，推动成果转化。','申报通过','未审批','未验收'),('PJT20250009','高端装备关键技术研究与应用','本项目围绕绿色食品及现代种业领域的关键问题，开展深入研究，推动成果转化。','未申报','未审批','未验收'),('PJT20250010','半导体关键技术研究与应用','本项目围绕聚变能源领域的关键问题，开展深入研究，推动成果转化。','申报通过','未审批','未验收'),('PJT20250011','半导体关键技术研究与应用','本项目围绕高端装备领域的关键问题，开展深入研究，推动成果转化。','申报通过','未审批','未验收'),('PJT20250012','城市安全关键技术研究与应用','本项目围绕现代服务业领域的关键问题，开展深入研究，推动成果转化。','申报通过','审批通过','验收通过'),('PJT20250013','医疗健康关键技术研究与应用','本项目围绕量子信息领域的关键问题，开展深入研究，推动成果转化。','申报通过','未审批','未验收'),('PJT20250014','新材料关键技术研究与应用','本项目围绕量子信息领域的关键问题，开展深入研究，推动成果转化。','申报通过','未审批','未验收'),('PJT20250015','高端装备关键技术研究与应用','本项目围绕新能源汽车和智能网联汽车领域的关键问题，开展深入研究，推动成果转化。','未申报','未审批','未验收'),('PJT20250016','大消费领域关键技术研究与应用','本项目围绕集成电路领域的关键问题，开展深入研究，推动成果转化。','申报通过','审批通过','未验收'),('PJT20250017','智能家电关键技术研究与应用','本项目围绕现代农业领域的关键问题，开展深入研究，推动成果转化。','未申报','未审批','未验收'),('PJT20250018','城市安全关键技术研究与应用','本项目围绕大消费领域领域的关键问题，开展深入研究，推动成果转化。','未申报','未审批','未验收'),('PJT20250020','光伏及新能源关键技术研究与应用','本项目围绕城市安全领域的关键问题，开展深入研究，推动成果转化。','未申报','未审批','未验收'),('PJT20250021','空天信息关键技术研究与应用','本项目围绕新材料领域的关键问题，开展深入研究，推动成果转化。','申报通过','审批通过','未验收'),('PJT20250022','人工智能关键技术研究与应用','本项目围绕网络与信息安全领域的关键问题，开展深入研究，推动成果转化。','未申报','未审批','未验收'),('PJT20250023','半导体关键技术研究与应用','本项目围绕创意文化领域的关键问题，开展深入研究，推动成果转化。','申报通过','审批通过','验收通过'),('PJT20250024','绿色食品及现代种业关键技术研究与应用','本项目围绕空天信息领域的关键问题，开展深入研究，推动成果转化。','申报通过','审批通过','未验收'),('PJT20250025','智能家电关键技术研究与应用','本项目围绕现代农业领域的关键问题，开展深入研究，推动成果转化。','申报通过','未审批','未验收'),('PJT20250026','新一代信息技术关键技术研究与应用','本项目围绕网络与信息安全领域的关键问题，开展深入研究，推动成果转化。','申报通过','未审批','未验收'),('PJT20250029','新能源汽车和智能网联汽车关键技术研究与应用','本项目围绕创意文化领域的关键问题，开展深入研究，推动成果转化。','申报通过','未审批','未验收'),('PJT20250031','量子信息关键技术研究与应用','本项目围绕量子信息领域的关键问题，开展深入研究，推动成果转化。','申报通过','未审批','未验收'),('PJT20250032','现代农业关键技术研究与应用','本项目围绕新一代信息技术领域的关键问题，开展深入研究，推动成果转化。','申报通过','审批通过','未验收'),('PJT20250033','创意文化关键技术研究与应用','本项目围绕生物医药领域的关键问题，开展深入研究，推动成果转化。','申报通过','审批通过','未验收'),('PJT20250034','高端装备关键技术研究与应用','本项目围绕空天信息领域的关键问题，开展深入研究，推动成果转化。','申报通过','未审批','未验收'),('PJT20250036','新型显示关键技术研究与应用','本项目围绕新一代信息技术领域的关键问题，开展深入研究，推动成果转化。','申报通过','未审批','未验收'),('PJT20250038','新材料关键技术研究与应用','本项目围绕光伏及新能源领域的关键问题，开展深入研究，推动成果转化。','未申报','未审批','未验收'),('PJT20250040','智能家电关键技术研究与应用','本项目围绕网络与信息安全领域的关键问题，开展深入研究，推动成果转化。','未申报','未审批','未验收'),('PJT20250041','空天信息关键技术研究与应用','本项目围绕医疗健康领域的关键问题，开展深入研究，推动成果转化。','未申报','未审批','未验收'),('PJT20250042','网络与信息安全关键技术研究与应用','本项目围绕集成电路领域的关键问题，开展深入研究，推动成果转化。','未申报','未审批','未验收'),('PJT20250043','空天信息关键技术研究与应用','本项目围绕网络与信息安全领域的关键问题，开展深入研究，推动成果转化。','申报通过','审批通过','未验收'),('PJT20250045','光伏及新能源关键技术研究与应用','本项目围绕现代服务业领域的关键问题，开展深入研究，推动成果转化。','申报通过','审批通过','未验收'),('PJT20250046','新型显示关键技术研究与应用','本项目围绕医疗健康领域的关键问题，开展深入研究，推动成果转化。','申报通过','未审批','未验收'),('PJT20250047','新材料关键技术研究与应用','本项目围绕人工智能领域的关键问题，开展深入研究，推动成果转化。','未申报','未审批','未验收'),('PJT20250048','人工智能关键技术研究与应用','本项目围绕新一代信息技术领域的关键问题，开展深入研究，推动成果转化。','未申报','未审批','未验收');
/*!40000 ALTER TABLE `project` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trg_project_application` BEFORE UPDATE ON `project` FOR EACH ROW BEGIN
    IF NEW.project_application_status != OLD.project_application_status AND NEW.project_application_status IS NOT NULL THEN
        SET NEW.project_application_status = '申报通过';
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trg_project_approval` BEFORE UPDATE ON `project` FOR EACH ROW BEGIN
    IF NEW.project_approval_status != OLD.project_approval_status AND NEW.project_approval_status IS NOT NULL THEN
        SET NEW.project_approval_status = '审批通过';
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trg_project_acceptance` BEFORE UPDATE ON `project` FOR EACH ROW BEGIN
    IF NEW.project_acceptance_status != OLD.project_acceptance_status AND NEW.project_acceptance_status IS NOT NULL THEN
        SET NEW.project_acceptance_status = '验收通过';
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `projectresearchfield`
--

DROP TABLE IF EXISTS `projectresearchfield`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `projectresearchfield` (
  `project_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '项目编号',
  `research_field` int NOT NULL COMMENT '研究领域',
  PRIMARY KEY (`project_id`,`research_field`),
  KEY `research_field` (`research_field`),
  CONSTRAINT `projectresearchfield_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `project` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `projectresearchfield_ibfk_2` FOREIGN KEY (`research_field`) REFERENCES `researchfields` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projectresearchfield`
--

LOCK TABLES `projectresearchfield` WRITE;
/*!40000 ALTER TABLE `projectresearchfield` DISABLE KEYS */;
INSERT INTO `projectresearchfield` VALUES ('PJT20250016',1),('PJT20250038',1),('PJT20250001',2),('PJT20250033',2),('PJT20250010',3),('PJT20250012',3),('PJT20250029',3),('PJT20250046',3),('PJT20250014',4),('PJT20250047',4),('PJT20250007',5),('PJT20250009',5),('PJT20250015',5),('PJT20250016',5),('PJT20250032',5),('PJT20250043',5),('PJT20250045',5),('PJT20250017',6),('PJT20250033',6),('PJT20250001',7),('PJT20250005',7),('PJT20250011',7),('PJT20250034',7),('PJT20250042',7),('PJT20250043',7),('PJT20250003',8),('PJT20250023',8),('PJT20250007',9),('PJT20250047',9),('PJT20250009',10),('PJT20250013',10),('PJT20250020',10),('PJT20250045',10),('PJT20250002',11),('PJT20250003',12),('PJT20250006',12),('PJT20250020',12),('PJT20250026',12),('PJT20250012',13),('PJT20250025',13),('PJT20250048',13),('PJT20250008',14),('PJT20250012',14),('PJT20250021',14),('PJT20250026',14),('PJT20250005',15),('PJT20250038',15),('PJT20250003',16),('PJT20250016',16),('PJT20250041',16),('PJT20250046',16),('PJT20250001',17),('PJT20250021',17),('PJT20250023',17),('PJT20250024',17),('PJT20250025',17),('PJT20250029',17),('PJT20250047',17),('PJT20250022',18),('PJT20250026',18),('PJT20250034',18),('PJT20250038',18),('PJT20250048',18),('PJT20250004',19),('PJT20250015',19),('PJT20250008',20),('PJT20250015',20),('PJT20250022',20),('PJT20250025',20),('PJT20250011',21),('PJT20250040',21),('PJT20250018',22),('PJT20250032',22),('PJT20250011',23),('PJT20250018',23),('PJT20250034',23),('PJT20250006',24),('PJT20250031',24),('PJT20250036',24),('PJT20250040',24),('PJT20250048',24),('PJT20250042',25);
/*!40000 ALTER TABLE `projectresearchfield` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `researchfields`
--

DROP TABLE IF EXISTS `researchfields`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `researchfields` (
  `id` int NOT NULL,
  `research_field` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '研究领域',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `researchfields`
--

LOCK TABLES `researchfields` WRITE;
/*!40000 ALTER TABLE `researchfields` DISABLE KEYS */;
INSERT INTO `researchfields` VALUES (1,'生物医药'),(2,'集成电路'),(3,'新能源汽车和智能网联汽车'),(4,'人工智能'),(5,'高端装备'),(6,'新材料'),(7,'光伏及新能源'),(8,'新型显示'),(9,'城市安全'),(10,'网络与信息安全'),(11,'节能环保'),(12,'智能家电'),(13,'空天信息'),(14,'绿色食品及现代种业'),(15,'量子信息'),(16,'创意文化'),(17,'新一代信息技术'),(18,'智能制造'),(19,'医疗健康'),(20,'半导体'),(21,'聚变能源'),(22,'合成生物'),(23,'现代农业'),(24,'现代服务业'),(25,'大消费领域');
/*!40000 ALTER TABLE `researchfields` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student` (
  `student_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '学生学号',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '姓名',
  `gender` enum('男','女') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '性别',
  `grade` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '年级',
  `major` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '专业',
  `class` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '班级',
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '联系电话',
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '电子邮箱',
  PRIMARY KEY (`student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES ('202410001','尤二','女','2023','自动化','2023级自动化1班','13445964883','尤二84@univ.edu'),('202410002','张三','男','2023','生物工程','2023级生物工程1班','13240362052','张三75@univ.edu'),('202410003','张三','女','2021','空天信息工程','2021级空天信息工程2班','13531821323','张三37@school.edu'),('202410004','朱十','男','2022','通信工程','2022级通信工程2班','13478349330','朱十59@edu.cn'),('202410005','张三','男','2022','集成电路设计与集成系统','2022级集成电路设计与集成系统3班','13571235982','张三82@edu.cn'),('202410006','孙七','女','2023','空天信息工程','2023级空天信息工程3班','13022878648','孙七8@edu.cn'),('202410007','卫五','女','2023','智能制造工程','2023级智能制造工程1班','13634343141','卫五82@univ.edu'),('202410008','郑十','男','2023','测控技术与仪器','2023级测控技术与仪器3班','13826055530','郑十47@school.edu'),('202410009','李四','男','2023','光电信息科学与工程','2023级光电信息科学与工程1班','13964841404','李四83@univ.edu'),('202410010','褚四','女','2021','电子信息工程','2021级电子信息工程2班','13725875639','褚四50@univ.edu'),('202410011','冯二','女','2021','生物工程','2021级生物工程2班','13286178086','冯二54@univ.edu'),('202410012','冯二','男','2023','生物技术','2023级生物技术2班','13065717739','冯二21@edu.cn'),('202410013','尤二','女','2022','光电信息科学与工程','2022级光电信息科学与工程3班','13716325231','尤二65@school.edu'),('202410014','朱十','女','2022','集成电路设计与集成系统','2022级集成电路设计与集成系统3班','13143695344','朱十64@edu.cn'),('202410015','赵六','男','2022','通信工程','2022级通信工程2班','13972856238','赵六15@school.edu'),('202410016','钱一','女','2023','软件工程','2023级软件工程1班','13697795517','钱一72@univ.edu'),('202410017','郑十','男','2023','空天信息工程','2023级空天信息工程1班','13099370773','郑十72@edu.cn'),('202410018','陈三','男','2021','现代农业工程','2021级现代农业工程1班','13858025622','陈三42@school.edu'),('202410019','蒋六','男','2021','新材料与智能结构','2021级新材料与智能结构2班','13274028658','蒋六43@univ.edu'),('202410020','卫五','女','2021','空天信息工程','2021级空天信息工程1班','13241553891','卫五53@univ.edu'),('202410021','孙七','女','2022','机械工程','2022级机械工程3班','13713131777','孙七46@school.edu'),('202410022','冯二','女','2023','电子信息工程','2023级电子信息工程2班','13797557738','冯二5@school.edu'),('202410023','李四','女','2022','机械工程','2022级机械工程1班','13662027415','李四99@edu.cn'),('202410024','孙七','男','2021','食品科学与工程','2021级食品科学与工程1班','13943408929','孙七84@school.edu'),('202410025','褚四','男','2022','城市安全工程','2022级城市安全工程3班','13188691124','褚四43@univ.edu'),('202410026','韩八','男','2021','食品科学与工程','2021级食品科学与工程2班','13628103527','韩八12@edu.cn'),('202410027','张三','男','2021','生物工程','2021级生物工程3班','13185779949','张三80@school.edu'),('202410028','李四','男','2021','通信工程','2021级通信工程3班','13035508784','李四30@edu.cn'),('202410029','陈三','男','2023','软件工程','2023级软件工程1班','13981032180','陈三52@edu.cn'),('202410030','沈七','女','2021','机械工程','2021级机械工程1班','13343865277','沈七8@edu.cn'),('202410031','韩八','男','2021','自动化','2021级自动化2班','13059228476','韩八25@univ.edu'),('202410032','秦一','女','2021','现代农业工程','2021级现代农业工程3班','13055377860','秦一65@school.edu'),('202410033','杨九','女','2021','生物技术','2021级生物技术1班','13968410143','杨九64@school.edu'),('202410034','赵六','男','2022','光电信息科学与工程','2022级光电信息科学与工程1班','13395035748','赵六67@edu.cn'),('202410035','王五','女','2023','通信工程','2023级通信工程2班','13390124799','王五59@edu.cn'),('202410036','张三','女','2022','自动化','2022级自动化1班','13565648262','张三61@univ.edu'),('202410037','陈三','男','2021','生物工程','2021级生物工程3班','13398360812','陈三65@school.edu'),('202410038','韩八','男','2021','集成电路设计与集成系统','2021级集成电路设计与集成系统2班','13871878901','韩八74@edu.cn'),('202410039','张三','男','2021','新能源汽车工程','2021级新能源汽车工程3班','13986785868','张三55@edu.cn'),('202410040','冯二','女','2021','空天信息工程','2021级空天信息工程3班','13565728083','冯二32@univ.edu'),('202410041','赵六','女','2023','测控技术与仪器','2023级测控技术与仪器2班','13525000902','赵六7@school.edu'),('202410042','赵六','男','2022','智能车辆工程','2022级智能车辆工程3班','13366911094','赵六70@edu.cn'),('202410043','周八','女','2021','软件工程','2021级软件工程3班','13593857583','周八13@univ.edu'),('202410044','李四','女','2022','智能车辆工程','2022级智能车辆工程1班','13397122125','李四7@univ.edu'),('202410045','卫五','女','2023','现代农业工程','2023级现代农业工程3班','13692771518','卫五53@univ.edu'),('202410046','朱十','女','2023','通信工程','2023级通信工程2班','13098222805','朱十67@school.edu'),('202410047','杨九','女','2023','智能制造工程','2023级智能制造工程1班','13580777426','杨九71@univ.edu'),('202410048','卫五','男','2021','城市安全工程','2021级城市安全工程2班','13684630259','卫五57@edu.cn'),('202410049','冯二','男','2021','测控技术与仪器','2021级测控技术与仪器2班','13258101657','冯二53@edu.cn'),('202410050','冯二','男','2023','生物工程','2023级生物工程1班','13753375098','冯二83@univ.edu');
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `studentproject`
--

DROP TABLE IF EXISTS `studentproject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `studentproject` (
  `student_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '学生学号',
  `project_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '项目编号',
  `role` enum('负责人','成员') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '在项目中的角色',
  PRIMARY KEY (`student_id`,`project_id`),
  KEY `project_id` (`project_id`),
  CONSTRAINT `studentproject_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`student_id`),
  CONSTRAINT `studentproject_ibfk_2` FOREIGN KEY (`project_id`) REFERENCES `project` (`project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `studentproject`
--

LOCK TABLES `studentproject` WRITE;
/*!40000 ALTER TABLE `studentproject` DISABLE KEYS */;
INSERT INTO `studentproject` VALUES ('202410001','PJT20250018','负责人'),('202410001','PJT20250038','成员'),('202410002','PJT20250003','负责人'),('202410002','PJT20250014','成员'),('202410002','PJT20250047','成员'),('202410003','PJT20250009','成员'),('202410003','PJT20250017','成员'),('202410003','PJT20250045','负责人'),('202410004','PJT20250008','成员'),('202410004','PJT20250015','成员'),('202410004','PJT20250034','负责人'),('202410005','PJT20250007','负责人'),('202410005','PJT20250047','成员'),('202410006','PJT20250020','成员'),('202410006','PJT20250046','负责人'),('202410007','PJT20250009','成员'),('202410007','PJT20250010','成员'),('202410007','PJT20250015','负责人'),('202410008','PJT20250047','负责人'),('202410009','PJT20250034','成员'),('202410010','PJT20250004','负责人'),('202410010','PJT20250015','成员'),('202410011','PJT20250010','成员'),('202410011','PJT20250012','成员'),('202410011','PJT20250029','负责人'),('202410012','PJT20250001','成员'),('202410012','PJT20250008','成员'),('202410012','PJT20250022','负责人'),('202410013','PJT20250001','成员'),('202410013','PJT20250041','成员'),('202410013','PJT20250042','负责人'),('202410014','PJT20250006','成员'),('202410014','PJT20250017','负责人'),('202410014','PJT20250026','成员'),('202410015','PJT20250006','成员'),('202410015','PJT20250031','负责人'),('202410015','PJT20250048','成员'),('202410016','PJT20250005','成员'),('202410016','PJT20250022','成员'),('202410016','PJT20250026','负责人'),('202410017','PJT20250038','成员'),('202410018','PJT20250038','负责人'),('202410019','PJT20250006','负责人'),('202410019','PJT20250036','成员'),('202410019','PJT20250040','成员'),('202410020','PJT20250005','负责人'),('202410020','PJT20250043','成员'),('202410020','PJT20250046','成员'),('202410021','PJT20250036','负责人'),('202410021','PJT20250048','成员'),('202410022','PJT20250010','负责人'),('202410022','PJT20250018','成员'),('202410022','PJT20250020','成员'),('202410023','PJT20250023','负责人'),('202410023','PJT20250038','成员'),('202410024','PJT20250021','负责人'),('202410024','PJT20250024','成员'),('202410025','PJT20250031','成员'),('202410025','PJT20250048','负责人'),('202410026','PJT20250009','成员'),('202410026','PJT20250032','负责人'),('202410026','PJT20250043','成员'),('202410028','PJT20250023','成员'),('202410028','PJT20250040','负责人'),('202410028','PJT20250042','成员'),('202410029','PJT20250002','负责人'),('202410029','PJT20250014','成员'),('202410030','PJT20250011','负责人'),('202410030','PJT20250042','成员'),('202410030','PJT20250043','成员'),('202410032','PJT20250001','负责人'),('202410032','PJT20250043','成员'),('202410033','PJT20250005','成员'),('202410033','PJT20250038','成员'),('202410033','PJT20250041','负责人'),('202410034','PJT20250008','成员'),('202410034','PJT20250012','负责人'),('202410034','PJT20250021','成员'),('202410035','PJT20250014','负责人'),('202410035','PJT20250047','成员'),('202410036','PJT20250008','成员'),('202410036','PJT20250012','成员'),('202410036','PJT20250025','负责人'),('202410037','PJT20250020','负责人'),('202410037','PJT20250026','成员'),('202410038','PJT20250005','成员'),('202410038','PJT20250011','成员'),('202410039','PJT20250003','成员'),('202410039','PJT20250033','负责人'),('202410040','PJT20250008','负责人'),('202410040','PJT20250022','成员'),('202410040','PJT20250025','成员'),('202410041','PJT20250007','成员'),('202410041','PJT20250009','成员'),('202410041','PJT20250016','负责人'),('202410042','PJT20250016','成员'),('202410042','PJT20250032','成员'),('202410042','PJT20250043','负责人'),('202410043','PJT20250042','成员'),('202410044','PJT20250009','负责人'),('202410044','PJT20250016','成员'),('202410044','PJT20250020','成员'),('202410045','PJT20250002','成员'),('202410045','PJT20250013','负责人'),('202410045','PJT20250031','成员'),('202410046','PJT20250021','成员'),('202410046','PJT20250023','成员'),('202410046','PJT20250024','负责人'),('202410047','PJT20250003','成员'),('202410047','PJT20250020','成员'),('202410048','PJT20250012','成员'),('202410048','PJT20250025','成员'),('202410049','PJT20250002','成员'),('202410049','PJT20250006','成员'),('202410050','PJT20250006','成员'),('202410050','PJT20250013','成员');
/*!40000 ALTER TABLE `studentproject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `studentresearchfield`
--

DROP TABLE IF EXISTS `studentresearchfield`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `studentresearchfield` (
  `student_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '学生学号',
  `research_field` int NOT NULL COMMENT '研究领域',
  PRIMARY KEY (`student_id`,`research_field`),
  KEY `research_field` (`research_field`),
  CONSTRAINT `studentresearchfield_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`student_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `studentresearchfield_ibfk_2` FOREIGN KEY (`research_field`) REFERENCES `researchfields` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `studentresearchfield`
--

LOCK TABLES `studentresearchfield` WRITE;
/*!40000 ALTER TABLE `studentresearchfield` DISABLE KEYS */;
INSERT INTO `studentresearchfield` VALUES ('202410017',1),('202410023',1),('202410034',1),('202410049',1),('202410039',2),('202410044',2),('202410007',3),('202410011',3),('202410022',3),('202410002',4),('202410029',4),('202410035',4),('202410003',5),('202410007',5),('202410026',5),('202410041',5),('202410042',5),('202410044',5),('202410003',6),('202410014',6),('202410012',7),('202410013',7),('202410020',7),('202410030',7),('202410032',7),('202410002',8),('202410019',8),('202410023',8),('202410028',8),('202410039',8),('202410041',8),('202410005',9),('202410007',9),('202410008',9),('202410029',10),('202410044',10),('202410045',10),('202410050',10),('202410029',11),('202410045',11),('202410049',11),('202410006',12),('202410014',12),('202410022',12),('202410037',12),('202410047',12),('202410049',12),('202410050',12),('202410036',13),('202410037',13),('202410048',13),('202410034',14),('202410001',15),('202410016',15),('202410018',15),('202410033',15),('202410038',15),('202410006',16),('202410013',16),('202410019',16),('202410020',16),('202410033',16),('202410024',17),('202410046',17),('202410004',18),('202410016',18),('202410010',19),('202410004',20),('202410012',20),('202410036',20),('202410040',20),('202410003',21),('202410009',21),('202410013',21),('202410028',21),('202410031',21),('202410037',21),('202410004',22),('202410014',22),('202410021',22),('202410034',22),('202410001',23),('202410009',23),('202410010',23),('202410022',23),('202410027',23),('202410030',23),('202410038',23),('202410015',24),('202410019',24),('202410021',24),('202410025',24),('202410045',24),('202410002',25),('202410028',25),('202410043',25),('202410048',25),('202410050',25);
/*!40000 ALTER TABLE `studentresearchfield` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teacher`
--

DROP TABLE IF EXISTS `teacher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teacher` (
  `teacher_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '教职工号',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '姓名',
  `gender` enum('男','女') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '性别',
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '职称',
  `college` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '所属学院',
  `department` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '所属专业',
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '联系电话',
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '电子邮箱',
  `office_location` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '办公地点',
  `introduction` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '个人简介',
  PRIMARY KEY (`teacher_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacher`
--

LOCK TABLES `teacher` WRITE;
/*!40000 ALTER TABLE `teacher` DISABLE KEYS */;
INSERT INTO `teacher` VALUES ('20230001','李四','男','研究员','食品与农业工程学院','食品科学与工程','13981223241','李四16@school.edu','实验楼B211','李四，研究员，专注于智能制造方向的研究与教学工作。'),('20230002','秦一','男','高级工程师','机械与车辆工程学院','新能源汽车工程','13544782595','秦一89@edu.cn','教学楼A101','秦一，高级工程师，专注于半导体方向的研究与教学工作。'),('20230003','陈三','男','副教授','生命科学学院','生物技术','13883161917','陈三65@edu.cn','教学楼A101','陈三，副教授，专注于创意文化方向的研究与教学工作。'),('20230004','朱十','女','教授','物理与信息工程学院','空天信息工程','13342531923','朱十1@edu.cn','实验楼B211','朱十，教授，专注于智能制造方向的研究与教学工作。'),('20230005','褚四','女','研究员','食品与农业工程学院','现代农业工程','13592494780','褚四18@univ.edu','实验楼B211','褚四，研究员，专注于现代农业方向的研究与教学工作。'),('20230006','朱十','男','高级工程师','环境与安全工程学院','环境工程','13917126811','朱十97@univ.edu','实验楼B211','朱十，高级工程师，专注于现代服务业方向的研究与教学工作。'),('20230007','王五','男','副教授','机械与车辆工程学院','机械工程','13777305239','王五54@school.edu','教学楼A101','王五，副教授，专注于半导体方向的研究与教学工作。'),('20230008','秦一','女','副教授','环境与安全工程学院','环境工程','13157800476','秦一40@univ.edu','教学楼A101','秦一，副教授，专注于生物医药方向的研究与教学工作。'),('20230009','张三','女','教授','电子工程学院','通信工程','13255500845','张三80@univ.edu','实验楼B211','张三，教授，专注于聚变能源方向的研究与教学工作。'),('20230010','杨九','女','副教授','材料科学与工程学院','材料科学与工程','13555182363','杨九43@edu.cn','教学楼A101','杨九，副教授，专注于集成电路方向的研究与教学工作。'),('20230011','朱十','女','讲师','物理与信息工程学院','光电信息科学与工程','13763981761','朱十43@edu.cn','实验楼B211','朱十，讲师，专注于生物医药方向的研究与教学工作。'),('20230012','杨九','女','讲师','食品与农业工程学院','食品科学与工程','13181274251','杨九99@univ.edu','教学楼A101','杨九，讲师，专注于集成电路方向的研究与教学工作。'),('20230013','周八','女','高级工程师','生命科学学院','生物工程','13577653535','周八39@school.edu','教学楼A101','周八，高级工程师，专注于创意文化方向的研究与教学工作。'),('20230014','蒋六','女','助教','环境与安全工程学院','环境工程','13932986063','蒋六37@school.edu','教学楼A101','蒋六，助教，专注于新材料方向的研究与教学工作。'),('20230015','朱十','女','教授','环境与安全工程学院','城市安全工程','13697502430','朱十59@edu.cn','教学楼A101','朱十，教授，专注于合成生物方向的研究与教学工作。'),('20230016','李四','女','讲师','计算机与信息学院','数据科学与大数据技术','13730098818','李四20@school.edu','教学楼A101','李四，讲师，专注于合成生物方向的研究与教学工作。'),('20230017','钱一','女','高级工程师','生命科学学院','生物工程','13241895223','钱一58@univ.edu','教学楼A101','钱一，高级工程师，专注于现代农业方向的研究与教学工作。'),('20230018','李四','女','副教授','材料科学与工程学院','新材料与智能结构','13283072868','李四16@univ.edu','教学楼A101','李四，副教授，专注于智能家电方向的研究与教学工作。'),('20230019','陈三','男','教授','材料科学与工程学院','材料科学与工程','13295719679','陈三93@univ.edu','教学楼A101','陈三，教授，专注于创意文化方向的研究与教学工作。'),('20230020','尤二','男','高级工程师','环境与安全工程学院','城市安全工程','13586766957','尤二16@univ.edu','教学楼A101','尤二，高级工程师，专注于城市安全方向的研究与教学工作。'),('20230021','卫五','女','教授','自动化学院','测控技术与仪器','13043477110','卫五86@edu.cn','实验楼B211','卫五，教授，专注于量子信息方向的研究与教学工作。'),('20230022','杨九','女','讲师','生命科学学院','生物工程','13581262493','杨九81@edu.cn','教学楼A101','杨九，讲师，专注于城市安全方向的研究与教学工作。'),('20230023','钱一','男','副教授','材料科学与工程学院','材料科学与工程','13824435177','钱一18@edu.cn','教学楼A101','钱一，副教授，专注于现代服务业方向的研究与教学工作。'),('20230024','郑十','女','研究员','食品与农业工程学院','现代农业工程','13019967657','郑十38@edu.cn','实验楼B211','郑十，研究员，专注于新型显示方向的研究与教学工作。'),('20230025','朱十','男','研究员','机械与车辆工程学院','智能车辆工程','13487057277','朱十91@school.edu','实验楼B211','朱十，研究员，专注于生物医药方向的研究与教学工作。'),('20230026','韩八','男','助教','电子工程学院','电子信息工程','13565582791','韩八59@edu.cn','教学楼A101','韩八，助教，专注于医疗健康方向的研究与教学工作。'),('20230027','孙七','女','副教授','食品与农业工程学院','食品科学与工程','13052311058','孙七90@univ.edu','实验楼B211','孙七，副教授，专注于高端装备方向的研究与教学工作。'),('20230028','赵六','女','高级工程师','材料科学与工程学院','新材料与智能结构','13842363071','赵六55@edu.cn','教学楼A101','赵六，高级工程师，专注于量子信息方向的研究与教学工作。'),('20230029','朱十','女','讲师','环境与安全工程学院','城市安全工程','13265722019','朱十12@school.edu','实验楼B211','朱十，讲师，专注于量子信息方向的研究与教学工作。'),('20230030','吴九','女','讲师','自动化学院','智能制造工程','13483524914','吴九18@edu.cn','实验楼B211','吴九，讲师，专注于绿色食品及现代种业方向的研究与教学工作。'),('20230031','卫五','女','讲师','电子工程学院','电子信息工程','13392953327','卫五18@univ.edu','教学楼A101','卫五，讲师，专注于现代农业方向的研究与教学工作。'),('20230032','张三','男','研究员','物理与信息工程学院','空天信息工程','13934390662','张三62@edu.cn','实验楼B211','张三，研究员，专注于合成生物方向的研究与教学工作。'),('20230033','李四','男','讲师','环境与安全工程学院','城市安全工程','13195094225','李四71@school.edu','实验楼B211','李四，讲师，专注于现代农业方向的研究与教学工作。'),('20230034','朱十','女','副教授','材料科学与工程学院','材料科学与工程','13814330597','朱十10@school.edu','教学楼A101','朱十，副教授，专注于城市安全方向的研究与教学工作。'),('20230035','韩八','男','高级工程师','材料科学与工程学院','新材料与智能结构','13852966654','韩八19@univ.edu','实验楼B211','韩八，高级工程师，专注于智能制造方向的研究与教学工作。'),('20230036','冯二','男','副教授','环境与安全工程学院','城市安全工程','13430343485','冯二20@univ.edu','教学楼A101','冯二，副教授，专注于智能制造方向的研究与教学工作。'),('20230037','卫五','男','研究员','计算机与信息学院','网络工程','13776288950','卫五59@edu.cn','教学楼A101','卫五，研究员，专注于网络与信息安全方向的研究与教学工作。'),('20230038','吴九','女','副教授','物理与信息工程学院','光电信息科学与工程','13631953015','吴九42@edu.cn','教学楼A101','吴九，副教授，专注于聚变能源方向的研究与教学工作。'),('20230039','王五','男','教授','电子工程学院','集成电路设计与集成系统','13463212248','王五40@edu.cn','教学楼A101','王五，教授，专注于生物医药方向的研究与教学工作。'),('20230040','张三','女','助教','计算机与信息学院','数据科学与大数据技术','13324699335','张三6@edu.cn','实验楼B211','张三，助教，专注于绿色食品及现代种业方向的研究与教学工作。'),('20230041','钱一','女','副教授','机械与车辆工程学院','新能源汽车工程','13370111256','钱一99@school.edu','实验楼B211','钱一，副教授，专注于绿色食品及现代种业方向的研究与教学工作。'),('20230042','尤二','女','副教授','机械与车辆工程学院','机械工程','13213322764','尤二64@school.edu','教学楼A101','尤二，副教授，专注于量子信息方向的研究与教学工作。'),('20230043','周八','男','副教授','机械与车辆工程学院','新能源汽车工程','13397153379','周八84@edu.cn','实验楼B211','周八，副教授，专注于高端装备方向的研究与教学工作。'),('20230044','杨九','女','研究员','材料科学与工程学院','新材料与智能结构','13767635744','杨九71@edu.cn','实验楼B211','杨九，研究员，专注于生物医药方向的研究与教学工作。'),('20230045','李四','男','高级工程师','食品与农业工程学院','食品科学与工程','13182835459','李四66@univ.edu','实验楼B211','李四，高级工程师，专注于创意文化方向的研究与教学工作。'),('20230046','卫五','男','教授','环境与安全工程学院','城市安全工程','13217618194','卫五60@school.edu','教学楼A101','卫五，教授，专注于人工智能方向的研究与教学工作。'),('20230047','冯二','女','副教授','物理与信息工程学院','光电信息科学与工程','13827159069','冯二45@school.edu','教学楼A101','冯二，副教授，专注于新一代信息技术方向的研究与教学工作。'),('20230048','秦一','女','研究员','材料科学与工程学院','新材料与智能结构','13680475565','秦一91@univ.edu','实验楼B211','秦一，研究员，专注于新型显示方向的研究与教学工作。'),('20230049','吴九','男','助教','环境与安全工程学院','环境工程','13689569867','吴九82@edu.cn','教学楼A101','吴九，助教，专注于聚变能源方向的研究与教学工作。'),('20230050','杨九','男','副教授','计算机与信息学院','软件工程','13589451364','杨九51@edu.cn','教学楼A101','杨九，副教授，专注于绿色食品及现代种业方向的研究与教学工作。');
/*!40000 ALTER TABLE `teacher` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teacherproject`
--

DROP TABLE IF EXISTS `teacherproject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teacherproject` (
  `teacher_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '教职工号',
  `project_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '项目编号',
  PRIMARY KEY (`teacher_id`,`project_id`),
  KEY `project_id` (`project_id`),
  CONSTRAINT `teacherproject_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`teacher_id`),
  CONSTRAINT `teacherproject_ibfk_2` FOREIGN KEY (`project_id`) REFERENCES `project` (`project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacherproject`
--

LOCK TABLES `teacherproject` WRITE;
/*!40000 ALTER TABLE `teacherproject` DISABLE KEYS */;
INSERT INTO `teacherproject` VALUES ('20230044','PJT20250001'),('20230042','PJT20250002'),('20230036','PJT20250003'),('20230042','PJT20250003'),('20230006','PJT20250004'),('20230011','PJT20250005'),('20230044','PJT20250005'),('20230019','PJT20250006'),('20230011','PJT20250007'),('20230032','PJT20250008'),('20230021','PJT20250009'),('20230009','PJT20250010'),('20230012','PJT20250011'),('20230047','PJT20250011'),('20230026','PJT20250012'),('20230041','PJT20250012'),('20230015','PJT20250013'),('20230016','PJT20250013'),('20230005','PJT20250014'),('20230007','PJT20250014'),('20230021','PJT20250015'),('20230010','PJT20250016'),('20230018','PJT20250016'),('20230007','PJT20250017'),('20230023','PJT20250017'),('20230006','PJT20250018'),('20230019','PJT20250020'),('20230018','PJT20250021'),('20230041','PJT20250021'),('20230032','PJT20250022'),('20230025','PJT20250023'),('20230033','PJT20250023'),('20230026','PJT20250024'),('20230049','PJT20250024'),('20230002','PJT20250025'),('20230035','PJT20250026'),('20230036','PJT20250026'),('20230009','PJT20250029'),('20230031','PJT20250031'),('20230040','PJT20250031'),('20230003','PJT20250032'),('20230030','PJT20250033'),('20230034','PJT20250034'),('20230035','PJT20250034'),('20230031','PJT20250036'),('20230010','PJT20250038'),('20230022','PJT20250040'),('20230037','PJT20250040'),('20230047','PJT20250041'),('20230001','PJT20250042'),('20230022','PJT20250042'),('20230050','PJT20250043'),('20230015','PJT20250045'),('20230034','PJT20250046'),('20230045','PJT20250047'),('20230012','PJT20250048'),('20230040','PJT20250048');
/*!40000 ALTER TABLE `teacherproject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teacherresearchfield`
--

DROP TABLE IF EXISTS `teacherresearchfield`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teacherresearchfield` (
  `teacher_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '教师工号',
  `research_field` int NOT NULL COMMENT '研究领域',
  PRIMARY KEY (`teacher_id`,`research_field`),
  KEY `research_field` (`research_field`),
  CONSTRAINT `teacherresearchfield_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`teacher_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `teacherresearchfield_ibfk_2` FOREIGN KEY (`research_field`) REFERENCES `researchfields` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacherresearchfield`
--

LOCK TABLES `teacherresearchfield` WRITE;
/*!40000 ALTER TABLE `teacherresearchfield` DISABLE KEYS */;
INSERT INTO `teacherresearchfield` VALUES ('20230010',1),('20230018',1),('20230012',2),('20230027',2),('20230029',2),('20230030',2),('20230009',3),('20230026',3),('20230005',4),('20230007',4),('20230009',4),('20230020',4),('20230045',4),('20230003',5),('20230011',5),('20230021',5),('20230007',6),('20230023',6),('20230035',6),('20230034',7),('20230036',7),('20230044',7),('20230047',7),('20230050',7),('20230006',8),('20230007',8),('20230033',8),('20230042',8),('20230004',9),('20230019',9),('20230036',9),('20230039',9),('20230050',9),('20230005',10),('20230008',10),('20230015',10),('20230016',10),('20230002',11),('20230005',11),('20230038',11),('20230042',11),('20230019',12),('20230021',12),('20230036',12),('20230012',13),('20230018',13),('20230041',13),('20230042',13),('20230018',14),('20230027',14),('20230011',15),('20230014',15),('20230017',16),('20230034',16),('20230047',16),('20230011',17),('20230025',17),('20230026',17),('20230041',17),('20230049',17),('20230035',18),('20230006',19),('20230021',19),('20230028',19),('20230029',19),('20230037',19),('20230043',19),('20230050',19),('20230002',20),('20230003',20),('20230029',20),('20230032',20),('20230035',20),('20230037',20),('20230038',20),('20230022',21),('20230031',21),('20230006',22),('20230046',22),('20230012',23),('20230020',23),('20230046',23),('20230048',23),('20230026',24),('20230031',24),('20230037',24),('20230040',24),('20230001',25),('20230013',25),('20230014',25),('20230022',25),('20230024',25);
/*!40000 ALTER TABLE `teacherresearchfield` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户名',
  `password` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '密码',
  `role` enum('Admin','Teacher','Student') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户角色',
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('20230001','20230001','Teacher'),('20230002','20230002','Teacher'),('20230003','20230003','Teacher'),('20230004','20230004','Teacher'),('20230005','20230005','Teacher'),('20230006','20230006','Teacher'),('20230007','20230007','Teacher'),('20230008','20230008','Teacher'),('20230009','20230009','Teacher'),('20230010','20230010','Teacher'),('20230011','20230011','Teacher'),('20230012','20230012','Teacher'),('20230013','20230013','Teacher'),('20230014','20230014','Teacher'),('20230015','20230015','Teacher'),('20230016','20230016','Teacher'),('20230017','20230017','Teacher'),('20230018','20230018','Teacher'),('20230019','20230019','Teacher'),('20230020','20230020','Teacher'),('20230021','20230021','Teacher'),('20230022','20230022','Teacher'),('20230023','20230023','Teacher'),('20230024','20230024','Teacher'),('20230025','20230025','Teacher'),('20230026','20230026','Teacher'),('20230027','20230027','Teacher'),('20230028','20230028','Teacher'),('20230029','20230029','Teacher'),('20230030','20230030','Teacher'),('20230031','20230031','Teacher'),('20230032','20230032','Teacher'),('20230033','20230033','Teacher'),('20230034','20230034','Teacher'),('20230035','20230035','Teacher'),('20230036','20230036','Teacher'),('20230037','20230037','Teacher'),('20230038','20230038','Teacher'),('20230039','20230039','Teacher'),('20230040','20230040','Teacher'),('20230041','20230041','Teacher'),('20230042','20230042','Teacher'),('20230043','20230043','Teacher'),('20230044','20230044','Teacher'),('20230045','20230045','Teacher'),('20230046','20230046','Teacher'),('20230047','20230047','Teacher'),('20230048','20230048','Teacher'),('20230049','20230049','Teacher'),('20230050','20230050','Teacher'),('202410001','202410001','Student'),('202410002','202410002','Student'),('202410003','202410003','Student'),('202410004','202410004','Student'),('202410005','202410005','Student'),('202410006','202410006','Student'),('202410007','202410007','Student'),('202410008','202410008','Student'),('202410009','202410009','Student'),('202410010','202410010','Student'),('202410011','202410011','Student'),('202410012','202410012','Student'),('202410013','202410013','Student'),('202410014','202410014','Student'),('202410015','202410015','Student'),('202410016','202410016','Student'),('202410017','202410017','Student'),('202410018','202410018','Student'),('202410019','202410019','Student'),('202410020','202410020','Student'),('202410021','202410021','Student'),('202410022','202410022','Student'),('202410023','202410023','Student'),('202410024','202410024','Student'),('202410025','202410025','Student'),('202410026','202410026','Student'),('202410027','202410027','Student'),('202410028','202410028','Student'),('202410029','202410029','Student'),('202410030','202410030','Student'),('202410031','202410031','Student'),('202410032','202410032','Student'),('202410033','202410033','Student'),('202410034','202410034','Student'),('202410035','202410035','Student'),('202410036','202410036','Student'),('202410037','202410037','Student'),('202410038','202410038','Student'),('202410039','202410039','Student'),('202410040','202410040','Student'),('202410041','202410041','Student'),('202410042','202410042','Student'),('202410043','202410043','Student'),('202410044','202410044','Student'),('202410045','202410045','Student'),('202410046','202410046','Student'),('202410047','202410047','Student'),('202410048','202410048','Student'),('202410049','202410049','Student'),('202410050','202410050','Student');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `view_project`
--

DROP TABLE IF EXISTS `view_project`;
/*!50001 DROP VIEW IF EXISTS `view_project`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `view_project` AS SELECT 
 1 AS `project_id`,
 1 AS `project_name`,
 1 AS `research_field`,
 1 AS `leader`,
 1 AS `member`,
 1 AS `teacher`,
 1 AS `project_application_status`,
 1 AS `project_approval_status`,
 1 AS `project_acceptance_status`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `view_student`
--

DROP TABLE IF EXISTS `view_student`;
/*!50001 DROP VIEW IF EXISTS `view_student`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `view_student` AS SELECT 
 1 AS `student_id`,
 1 AS `name`,
 1 AS `gender`,
 1 AS `grade`,
 1 AS `major`,
 1 AS `class`,
 1 AS `phone`,
 1 AS `email`,
 1 AS `research_field`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `view_teacher`
--

DROP TABLE IF EXISTS `view_teacher`;
/*!50001 DROP VIEW IF EXISTS `view_teacher`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `view_teacher` AS SELECT 
 1 AS `teacher_id`,
 1 AS `name`,
 1 AS `gender`,
 1 AS `title`,
 1 AS `college`,
 1 AS `department`,
 1 AS `phone`,
 1 AS `email`,
 1 AS `office_location`,
 1 AS `introduction`,
 1 AS `research_field`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `view_project`
--

/*!50001 DROP VIEW IF EXISTS `view_project`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `view_project` AS select `p`.`project_id` AS `project_id`,`p`.`project_name` AS `project_name`,group_concat(distinct `rf`.`research_field` separator '、') AS `research_field`,(select group_concat(concat(`s`.`name`,'(',`s`.`student_id`,')') separator '、') from (`studentproject` `sp` join `student` `s` on((`sp`.`student_id` = `s`.`student_id`))) where ((`sp`.`project_id` = `p`.`project_id`) and (`sp`.`role` = '负责人'))) AS `leader`,(select group_concat(concat(`s`.`name`,'(',`s`.`student_id`,')') separator '、') from (`studentproject` `sp` join `student` `s` on((`sp`.`student_id` = `s`.`student_id`))) where ((`sp`.`project_id` = `p`.`project_id`) and (`sp`.`role` = '成员'))) AS `member`,(select group_concat(concat(`t`.`name`,'(',`t`.`teacher_id`,')') separator '、') from (`teacherproject` `tp` join `teacher` `t` on((`tp`.`teacher_id` = `t`.`teacher_id`))) where (`tp`.`project_id` = `p`.`project_id`)) AS `teacher`,`p`.`project_application_status` AS `project_application_status`,`p`.`project_approval_status` AS `project_approval_status`,`p`.`project_acceptance_status` AS `project_acceptance_status` from ((`project` `p` left join `projectresearchfield` `prf` on((`p`.`project_id` = `prf`.`project_id`))) left join `researchfields` `rf` on((`prf`.`research_field` = `rf`.`id`))) group by `p`.`project_id` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `view_student`
--

/*!50001 DROP VIEW IF EXISTS `view_student`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `view_student` AS select `s`.`student_id` AS `student_id`,`s`.`name` AS `name`,`s`.`gender` AS `gender`,`s`.`grade` AS `grade`,`s`.`major` AS `major`,`s`.`class` AS `class`,`s`.`phone` AS `phone`,`s`.`email` AS `email`,group_concat(distinct `rf`.`research_field` separator '、') AS `research_field` from ((`student` `s` left join `studentresearchfield` `srf` on((`s`.`student_id` = `srf`.`student_id`))) left join `researchfields` `rf` on((`srf`.`research_field` = `rf`.`id`))) group by `s`.`student_id` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `view_teacher`
--

/*!50001 DROP VIEW IF EXISTS `view_teacher`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `view_teacher` AS select `t`.`teacher_id` AS `teacher_id`,`t`.`name` AS `name`,`t`.`gender` AS `gender`,`t`.`title` AS `title`,`t`.`college` AS `college`,`t`.`department` AS `department`,`t`.`phone` AS `phone`,`t`.`email` AS `email`,`t`.`office_location` AS `office_location`,`t`.`introduction` AS `introduction`,group_concat(distinct `rf`.`research_field` separator '、') AS `research_field` from ((`teacher` `t` left join `teacherresearchfield` `trf` on((`t`.`teacher_id` = `trf`.`teacher_id`))) left join `researchfields` `rf` on((`trf`.`research_field` = `rf`.`id`))) group by `t`.`teacher_id` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-16  0:10:54
