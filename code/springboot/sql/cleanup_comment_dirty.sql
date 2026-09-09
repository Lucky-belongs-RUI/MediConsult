-- 清理评论脏数据：删除指向不存在用户/空内容的测试垃圾评论（保留有效评论）
-- 先统计再删除，便于核对
SELECT CONCAT('待清理-无主评论: ', COUNT(*)) AS note FROM comment WHERE user_id NOT IN (SELECT id FROM user);
SELECT CONCAT('待清理-验证评论: ', COUNT(*)) AS note FROM comment WHERE content = '接口逻辑验证-测试评论';

DELETE FROM comment WHERE user_id NOT IN (SELECT id FROM user);
DELETE FROM comment WHERE content = '接口逻辑验证-测试评论';
DELETE FROM comment WHERE content IS NULL OR TRIM(content) = '';

SELECT CONCAT('清理后剩余评论: ', COUNT(*)) AS note FROM comment;
