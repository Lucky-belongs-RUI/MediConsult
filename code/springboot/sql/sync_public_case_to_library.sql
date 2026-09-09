-- =============================================================
-- 个人病例"公开=发布到病例库"逻辑的数据同步
-- 1. user_case 表增加 item_id 列（记录公开后对应的病例库记录ID）
-- 2. 将已公开(is_public=1)但尚未发布的病例发布到 item 表并回填 item_id
-- =============================================================

ALTER TABLE `user_case`
  ADD COLUMN `item_id` INT DEFAULT NULL COMMENT '公开后对应的病例库记录ID（item.id），未公开为空' AFTER `user_id`;

-- 为已公开病例生成病例库记录（tags 标记为“公开病例”便于回填与识别）
INSERT INTO item (title, description, category_id, user_id, tags)
SELECT uc.title, uc.content, uc.category_id, uc.user_id, '公开病例'
FROM user_case uc
WHERE uc.is_public = 1 AND uc.item_id IS NULL;

-- 回填 item_id（按 用户+标题 匹配本次生成的病例库记录）
UPDATE user_case uc
JOIN item i ON i.user_id = uc.user_id AND i.title = uc.title AND i.tags = '公开病例'
SET uc.item_id = i.id
WHERE uc.is_public = 1 AND uc.item_id IS NULL;
