-- 创建数据库及基本设置
CREATE DATABASE IF NOT EXISTS `myDatabase` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `myDatabase`;

SET NAMES utf8mb4;
SET character_set_client = 'utf8mb4';
SET character_set_connection = 'utf8mb4';
SET character_set_results = 'utf8mb4';


-- 科研领域表
CREATE TABLE IF NOT EXISTS ResearchFields (
    id INT PRIMARY KEY,
    research_field VARCHAR(100) NOT NULL COMMENT '研究领域'
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 插入科研领域表数据
INSERT INTO ResearchFields (id, research_field) VALUES
(1, '生物医药'), (2, '集成电路'), (3, '新能源汽车和智能网联汽车'), (4, '人工智能'),
(5, '高端装备'), (6, '新材料'), (7, '光伏及新能源'), (8, '新型显示'),
(9, '城市安全'), (10, '网络与信息安全'), (11, '节能环保'), (12, '智能家电'),
(13, '空天信息'), (14, '绿色食品及现代种业'), (15, '量子信息'), (16, '创意文化'),
(17, '新一代信息技术'), (18, '智能制造'), (19, '医疗健康'), (20, '半导体'),
(21, '聚变能源'), (22, '合成生物'), (23, '现代农业'), (24, '现代服务业'),
(25, '大消费领域');


-- 教职工表
CREATE TABLE IF NOT EXISTS Teacher (
    teacher_id VARCHAR(20) PRIMARY KEY COMMENT '教职工号',
    name VARCHAR(100) NOT NULL COMMENT '姓名',
    gender ENUM('男','女') COMMENT '性别',
    title VARCHAR(100) COMMENT '职称',
    college VARCHAR(100) COMMENT '所属学院',
    department VARCHAR(100) COMMENT '所属专业',
    phone VARCHAR(20) COMMENT '联系电话',
    email VARCHAR(100) COMMENT '电子邮箱',
    office_location VARCHAR(100) COMMENT '办公地点',
    introduction TEXT COMMENT '个人简介'
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


-- 学生表
CREATE TABLE IF NOT EXISTS Student (
    student_id VARCHAR(20) PRIMARY KEY COMMENT '学生学号',
    name VARCHAR(100) NOT NULL COMMENT '姓名',
    gender ENUM('男','女') COMMENT '性别',
    grade VARCHAR(10) COMMENT '年级',
    major VARCHAR(100) COMMENT '专业',
    class VARCHAR(100) COMMENT '班级',
    phone VARCHAR(20) COMMENT '联系电话',
    email VARCHAR(100) COMMENT '电子邮箱'
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


-- 科研项目表
CREATE TABLE IF NOT EXISTS Project (
    project_id VARCHAR(50) PRIMARY KEY COMMENT '项目编号',
    project_name VARCHAR(255) NOT NULL COMMENT '项目名称',
    project_content TEXT COMMENT '项目内容',
    project_application_status VARCHAR(20) DEFAULT '未申报',
    project_approval_status VARCHAR(20) DEFAULT '未审批',
    project_acceptance_status VARCHAR(20) DEFAULT '未验收'
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


-- 用户表
CREATE TABLE IF NOT EXISTS Users (
    username VARCHAR(50) PRIMARY KEY COMMENT '用户名',
    password VARCHAR(64) NOT NULL COMMENT '密码',
    role ENUM('Admin', 'Teacher', 'Student') NOT NULL COMMENT '用户角色'
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


-- 学生-科研项目关联表
CREATE TABLE IF NOT EXISTS StudentProject (
    student_id VARCHAR(20) NOT NULL COMMENT '学生学号',
    project_id VARCHAR(50) NOT NULL COMMENT '项目编号',
    role ENUM('负责人', '成员') NOT NULL COMMENT '在项目中的角色',
    PRIMARY KEY (student_id, project_id),
    FOREIGN KEY (student_id) REFERENCES Student(student_id),
    FOREIGN KEY (project_id) REFERENCES Project(project_id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


-- 教职工-科研项目关联表
CREATE TABLE IF NOT EXISTS TeacherProject (
    teacher_id VARCHAR(20) NOT NULL COMMENT '教职工号',
    project_id VARCHAR(50) NOT NULL COMMENT '项目编号',
    PRIMARY KEY (teacher_id, project_id),
    FOREIGN KEY (teacher_id) REFERENCES Teacher(teacher_id),
    FOREIGN KEY (project_id) REFERENCES Project(project_id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


-- 学生–研究领域关联表
CREATE TABLE IF NOT EXISTS StudentResearchField (
    student_id VARCHAR(20) NOT NULL COMMENT '学生学号',
    research_field INT NOT NULL COMMENT '研究领域',
    PRIMARY KEY (student_id, research_field),
    FOREIGN KEY (student_id) REFERENCES Student(student_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (research_field) REFERENCES ResearchFields(id) ON DELETE CASCADE ON UPDATE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


-- 教职工–研究领域关联表
CREATE TABLE IF NOT EXISTS TeacherResearchField (
    teacher_id VARCHAR(20) NOT NULL COMMENT '教师工号',
    research_field INT NOT NULL COMMENT '研究领域',
    PRIMARY KEY (teacher_id, research_field),
    FOREIGN KEY (teacher_id) REFERENCES Teacher(teacher_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (research_field) REFERENCES ResearchFields(id) ON DELETE CASCADE ON UPDATE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


-- 科研项目–研究领域关联表
CREATE TABLE IF NOT EXISTS ProjectResearchField (
    project_id VARCHAR(50) NOT NULL COMMENT '项目编号',
    research_field INT NOT NULL COMMENT '研究领域',
    PRIMARY KEY (project_id, research_field),
    FOREIGN KEY (project_id) REFERENCES Project(project_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (research_field) REFERENCES ResearchFields(id) ON DELETE CASCADE ON UPDATE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


-- 触发器设置（自动状态更新）

-- 申报状态自动置为“申报通过”
DELIMITER $$
CREATE TRIGGER trg_project_application
BEFORE UPDATE ON Project
FOR EACH ROW
BEGIN
    IF NEW.project_application_status != OLD.project_application_status AND NEW.project_application_status IS NOT NULL THEN
        SET NEW.project_application_status = '申报通过';
    END IF;
END$$
DELIMITER ;

-- 审批状态自动置为“审批通过”
DELIMITER $$
CREATE TRIGGER trg_project_approval
BEFORE UPDATE ON Project
FOR EACH ROW
BEGIN
    IF NEW.project_approval_status != OLD.project_approval_status AND NEW.project_approval_status IS NOT NULL THEN
        SET NEW.project_approval_status = '审批通过';
    END IF;
END$$
DELIMITER ;

-- 验收状态自动置为“验收通过”
DELIMITER $$
CREATE TRIGGER trg_project_acceptance
BEFORE UPDATE ON Project
FOR EACH ROW
BEGIN
    IF NEW.project_acceptance_status != OLD.project_acceptance_status AND NEW.project_acceptance_status IS NOT NULL THEN
        SET NEW.project_acceptance_status = '验收通过';
    END IF;
END$$
DELIMITER ;


-- 科研项目查询视图
CREATE OR REPLACE VIEW view_project AS
SELECT
    p.project_id,
    p.name AS project_name,
    -- 拼接多个研究领域名称（去重 + 顿号分隔）
    GROUP_CONCAT(DISTINCT rf.research_field SEPARATOR '、') AS research_field,
    -- 负责人（顿号拼接）
    GROUP_CONCAT(DISTINCT CASE WHEN sp.role = '负责人' THEN s.name END SEPARATOR '、') AS leader_names,
    -- 成员（顿号拼接）
    GROUP_CONCAT(DISTINCT CASE WHEN sp.role = '成员' THEN s.name END SEPARATOR '、') AS member_names,
    -- 指导老师（顿号拼接）
    GROUP_CONCAT(DISTINCT t.name SEPARATOR '、') AS teacher_names,
    -- 状态字段
    p.project_application_status,
    p.project_approval_status,
    p.project_acceptance_status
FROM Project p
-- 连接多研究领域关系表
LEFT JOIN ProjectResearchField prf ON p.project_id = prf.project_id
LEFT JOIN ResearchFields rf ON prf.research_field = rf.id
-- 关联逻辑
LEFT JOIN StudentProject sp ON p.project_id = sp.project_id
LEFT JOIN Student s ON sp.student_id = s.student_id
LEFT JOIN TeacherProject tp ON p.project_id = tp.project_id
LEFT JOIN Teacher t ON tp.teacher_id = t.teacher_id
GROUP BY p.project_id;


-- 学生查询视图
CREATE OR REPLACE VIEW view_student AS
SELECT
    s.student_id,
    s.name,
    s.gender,
    s.grade,
    s.major,
    s.class,
    s.phone,
    s.email,
    GROUP_CONCAT(DISTINCT rf.research_field SEPARATOR '、') AS research_field
FROM Student s
LEFT JOIN StudentResearchField srf ON s.student_id = srf.student_id
LEFT JOIN ResearchFields rf ON srf.research_field = rf.id
GROUP BY s.student_id;


-- 教职工查询视图
CREATE OR REPLACE VIEW view_teacher AS
SELECT
    t.teacher_id,
    t.name,
    t.gender,
    t.title,
    t.college,
    t.department,
    t.phone,
    t.email,
    t.office_location,
    t.introduction,
    GROUP_CONCAT(DISTINCT rf.research_field SEPARATOR '、') AS research_field
FROM Teacher t
LEFT JOIN TeacherResearchField trf ON t.teacher_id = trf.teacher_id
LEFT JOIN ResearchFields rf ON trf.research_field = rf.id
GROUP BY t.teacher_id;
