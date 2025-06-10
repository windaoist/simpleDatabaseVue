CREATE DATABASE IF NOT EXISTS `myDatabase` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `myDatabase`;

SET NAMES utf8mb4;
SET character_set_client = 'utf8mb4';
SET character_set_connection = 'utf8mb4';
SET character_set_results = 'utf8mb4';

-- 重点产业链表
CREATE TABLE IF NOT EXISTS KeyIndustries (
    id INT PRIMARY KEY,
    industry_name VARCHAR(255) NOT NULL UNIQUE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 预先插入重点产业链数据
INSERT INTO KeyIndustries (id, industry_name) VALUES
(1, '生物医药'),
(2, '集成电路'),
(3, '新能源汽车和智能网联汽车'),
(4, '人工智能'),
(5, '高端装备'),
(6, '新材料'),
(7, '光伏及新能源'),
(8, '新型显示'),
(9, '城市安全'),
(10, '网络与信息安全'),
(11, '节能环保'),
(12, '智能家电'),
(13, '空天信息'),
(14, '绿色食品及现代种业'),
(15, '量子信息'),
(16, '创意文化'),
(17, '新一代信息技术'),
(18, '智能制造'),
(19, '医疗健康'),
(20, '半导体'),
(21, '聚变能源'),
(22, '合成生物'),
(23, '现代农业'),
(24, '现代服务业'),
(25, '大消费领域');

-- 基金库表
CREATE TABLE IF NOT EXISTS Fund (
    fund_name VARCHAR(255) NOT NULL,
    investment_area INT NOT NULL,
    management_agency VARCHAR(255),
    contact_person VARCHAR(255),
    phone VARCHAR(255),
    fundraising_amount DECIMAL(15, 2),
    total_investment DECIMAL(15, 4),
    PRIMARY KEY (fund_name, investment_area),
    FOREIGN KEY (investment_area) REFERENCES KeyIndustries(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 项目库表
CREATE TABLE IF NOT EXISTS Project (
    project_name VARCHAR(255) NOT NULL,
    industry_chain INT NOT NULL,
    project_status VARCHAR(255),
    project_content TEXT,
    investor VARCHAR(255),
    investment_amount DECIMAL(15, 2),
    financing_amount DECIMAL(15, 2),
    equity_financing DECIMAL(15, 2),
    debt_financing DECIMAL(15, 2),
    project_progress TEXT,
    location VARCHAR(255),
    contact_person VARCHAR(255),
    contact_phone VARCHAR(255),
    PRIMARY KEY (project_name, industry_chain),
    FOREIGN KEY (industry_chain) REFERENCES KeyIndustries(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 专家库表
CREATE TABLE IF NOT EXISTS Expert (
    expert_name VARCHAR(255) NOT NULL,
    specific_industry INT NOT NULL,
    industry_category VARCHAR(255),
    fund_name VARCHAR(255),
    agency_name VARCHAR(255),
    PRIMARY KEY (expert_name, specific_industry),
    FOREIGN KEY (specific_industry) REFERENCES KeyIndustries(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
