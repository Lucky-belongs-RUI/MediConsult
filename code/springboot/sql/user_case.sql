-- =============================================================
-- 个人病例表（user_case）
-- 用途：保存用户在「智能医生」AI问诊中记录的个人病例，
--       与用户ID绑定；支持公开/私有切换，公开后在公开病例界面展示。
-- 说明：执行前请确认已连接 medical 数据库。
--   mysql -uroot -proot medical < user_case.sql
-- =============================================================

CREATE TABLE IF NOT EXISTS `user_case` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` INT NOT NULL COMMENT '所属用户ID（关联user.id）',
  `title` VARCHAR(100) NOT NULL COMMENT '问诊名称/病例标题',
  `patient_name` VARCHAR(50) DEFAULT NULL COMMENT '患者姓名',
  `age` INT DEFAULT NULL COMMENT '年龄',
  `gender` VARCHAR(10) DEFAULT NULL COMMENT '性别',
  `category_id` INT DEFAULT NULL COMMENT '问诊科室ID（关联category.id）',
  `remark` VARCHAR(500) DEFAULT NULL COMMENT '特殊情况备注',
  `content` TEXT COMMENT '问诊记录内容（含基础信息与对话记录）',
  `is_public` TINYINT NOT NULL DEFAULT 0 COMMENT '是否公开：0私有 1公开',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_category_id` (`category_id`),
  KEY `idx_is_public` (`is_public`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='个人病例表';
