-- 管理端测试账号（假数据，用于测试管理端页面，非项目逻辑修改）
INSERT INTO user (username, password, real_name, phone, email, avatar_bucket, avatar_object_key, role, status) VALUES
('admin', 'admin123', '系统管理员', '13800138999', 'admin@test.com', 'avatars', '20251120075554-23dc2bc547ea41b5b173df0f293052d8.jpg', 1, 1)
ON DUPLICATE KEY UPDATE role = 1, status = 1;
