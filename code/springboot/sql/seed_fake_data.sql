-- =============================================================
-- 测试假数据 seed（仅新增，不动已有数据）
-- 执行方式：mysql --default-character-set=utf8mb4 -uroot -proot medical < seed_fake_data.sql
-- =============================================================

START TRANSACTION;

-- ---------- user（新增 5 个测试用户，username 唯一） ----------
INSERT INTO user (username, password, real_name, phone, email, avatar_bucket, avatar_object_key, role, status) VALUES
('test_user01', '123456', '王小明', '13800138001', 'xiaoming@test.com', 'avatars', '20260908084409-2914b1574d04407895e5c1c0e3d7ef10.jpg', 0, 1),
('test_user02', '123456', '李小红', '13800138002', 'xiaohong@test.com', 'avatars', '20260625030335-5832a793c6734783a263746bdce4d8dc.jpg', 0, 1),
('test_user03', '123456', '赵建国', '13800138003', 'jianguo@test.com', 'avatars', '20260316152234-70139b968d8746c599211ac32a8f9025.png', 0, 1),
('test_user04', '123456', '孙丽娟', '13800138004', 'lijuan@test.com', 'avatars', '20260315055008-1feba02e38b245a697cc0c83c27152c6.png', 0, 1),
('test_user05', '123456', '周海燕', '13800138005', 'haiyan@test.com', 'avatars', '20251120075554-23dc2bc547ea41b5b173df0f293052d8.jpg', 0, 1);

-- ---------- category（新增 3 个科室，name 唯一） ----------
INSERT INTO category (name, description) VALUES
('中医科', '运用中医理论进行辨证论治，涵盖中药、针灸、推拿等疗法'),
('全科医学科', '提供常见病、多发病的综合诊疗与健康管理服务'),
('重症医学科', '集中收治各类急危重症患者，提供生命支持与监护');

-- ---------- item（新增 4 个病例，引用已有科室与医生用户） ----------
INSERT INTO item (title, description, category_id, user_id, cover_bucket, cover_object_key, tags) VALUES
('45岁男性2型糖尿病随访', '患者糖尿病史3年，近期空腹血糖偏高，伴口渴、多尿，建议规范用药并控制饮食。', 9, 2, 'item-cover', '20251118132927-07ebe897ff954fdbb4bab63dc166a31e.png', '糖尿病,口渴,多尿'),
('28岁女性荨麻疹病例', '接触过敏原后全身出现风团伴剧烈瘙痒，夜间加重，给予抗组胺药物后缓解。', 5, 3, 'item-cover', '20260314124920-471072ae0c02433b9ccd5887a0b7b2fb.png', '荨麻疹,瘙痒,风团'),
('50岁男性胃溃疡病例', '上腹部规律性疼痛伴反酸烧心，胃镜示胃窦溃疡，Hp阳性，予四联疗法根除。', 7, 2, 'item-cover', '20251118132927-07ebe897ff954fdbb4bab63dc166a31e.png', '胃痛,反酸,胃溃疡'),
('33岁女性甲状腺结节病例', '体检发现甲状腺右叶结节，超声TI-RADS 3类，甲功正常，建议定期随访。', 9, 3, 'item-cover', '20260314124920-471072ae0c02433b9ccd5887a0b7b2fb.png', '甲状腺结节,颈部肿物');

-- ---------- favorite（新增 6 条，避免与现有组合重复） ----------
INSERT INTO favorite (user_id, item_id, status) VALUES
(4, 3, 1), (10, 1, 1), (11, 3, 1), (2, 1, 1), (3, 2, 1), (6, 1, 1);

-- ---------- like（新增 5 条，避免与现有组合重复） ----------
INSERT INTO `like` (user_id, item_id, status) VALUES
(10, 3, 1), (2, 1, 1), (3, 1, 1), (4, 3, 1), (11, 1, 1);

-- ---------- comment（新增 6 条：4 条顶级 + 2 条回复） ----------
INSERT INTO comment (user_id, username, avatar, item_id, content, parent_id, reply_to_comment_id, reply_to_user_id, reply_to_username) VALUES
(4, 'patient_wang', NULL, 1, '这个病例很典型，和我父亲的症状一样，学习了！', NULL, NULL, NULL, NULL),
(10, '123456', NULL, 1, '请问这种情况需要长期服药吗？', NULL, NULL, NULL, NULL),
(2, 'zhangsan', NULL, 1, '建议遵医嘱长期管理血压，定期复查，不可自行停药。', 2, 2, 10, '123456'),
(11, '321', NULL, 2, '偏头痛发作时有什么缓解办法吗？', NULL, NULL, NULL, NULL),
(3, 'dr_li', NULL, 2, '发作时建议在安静暗室休息，必要时遵医嘱使用止痛药物。', 4, 4, 11, '321'),
(6, '123', NULL, 3, '膝盖疼痛的理疗方案很实用，收藏了！', NULL, NULL, NULL, NULL);

-- ---------- user_action（新增 10 条，0=查看 1=咨询） ----------
INSERT INTO user_action (user_id, item_id, action_type, extra_data) VALUES
(4, 1, 0, NULL), (4, 1, 1, NULL), (10, 2, 0, NULL), (10, 3, 0, NULL),
(11, 3, 1, NULL), (2, 1, 0, NULL), (3, 2, 0, NULL), (3, 2, 1, NULL),
(4, 2, 1, NULL), (11, 1, 1, NULL);

-- ---------- chat_session（新增 5 个问诊会话） ----------
INSERT INTO chat_session (user_id, session_name) VALUES (4, '高血压复诊咨询');
SET @s1 = LAST_INSERT_ID();
INSERT INTO chat_session (user_id, session_name) VALUES (11, '感冒咳嗽问诊');
SET @s2 = LAST_INSERT_ID();
INSERT INTO chat_session (user_id, session_name) VALUES (2, '膝盖疼痛复诊');
SET @s3 = LAST_INSERT_ID();
INSERT INTO chat_session (user_id, session_name) VALUES (4, '儿童发烧咨询');
SET @s4 = LAST_INSERT_ID();
INSERT INTO chat_session (user_id, session_name) VALUES (11, '糖尿病饮食咨询');
SET @s5 = LAST_INSERT_ID();

-- ---------- chat_message（新增 12 条，user/assistant 交替） ----------
INSERT INTO chat_message (session_id, role, content, model) VALUES
(@s1, 'user', '最近早上量血压总是偏高，145/95左右，需要调整药量吗？', 'qwen-turbo'),
(@s1, 'assistant', '建议先连续监测一周血压并记录，若持续高于140/90请及时就诊，不要自行调整药量。', 'qwen-turbo'),
(@s1, 'user', '好的，那饮食上有什么要注意的？', 'qwen-turbo'),
(@s1, 'assistant', '低盐低脂饮食，每日食盐不超过5克，戒烟限酒，适量运动，规律作息。', 'qwen-turbo'),
(@s2, 'user', '感冒咳嗽三天了，晚上咳得厉害，吃什么药好？', 'qwen-turbo'),
(@s2, 'assistant', '建议多喝温水、注意休息。若咳嗽影响睡眠可对症使用止咳药，症状加重或发热请及时就医。', 'qwen-turbo'),
(@s3, 'user', '膝盖上下楼梯疼，拍了片子说是退行性病变，怎么锻炼合适？', 'qwen-turbo'),
(@s3, 'assistant', '建议减少爬山爬楼等负重活动，可进行直腿抬高、靠墙静蹲等无负重训练，必要时理疗。', 'qwen-turbo'),
(@s4, 'user', '孩子3岁发烧38.5度，精神还可以，需要去医院吗？', 'qwen-turbo'),
(@s4, 'assistant', '体温38.5度以下可先物理降温并观察，若超过38.5度或精神差、呕吐等症状请立即就医。', 'qwen-turbo'),
(@s5, 'user', '得了糖尿病，主食应该怎么吃？', 'qwen-turbo'),
(@s5, 'assistant', '主食粗细搭配，控制总量，少食多餐，避免含糖饮料和甜食，配合规律监测血糖。', 'qwen-turbo');

-- ---------- user_case（新增 8 条个人病例，4 条公开用于公开病例页面测试） ----------
INSERT INTO user_case (user_id, title, patient_name, age, gender, category_id, remark, content, is_public) VALUES
(4, '高血压复诊记录', '王建国', 56, '男', 1, '高血压病史5年，正在服用降压药', '【问诊名称】高血压复诊记录\n【患者姓名】王建国\n【年龄】56\n【性别】男\n【问诊科室】心内科\n【特殊情况备注】高血压病史5年，正在服用降压药\n\n【问诊记录】\n用户：最近早上量血压总是偏高，145/95左右，需要调整药量吗？\nAI助手：建议先连续监测一周血压并记录，若持续高于140/90请及时就诊，不要自行调整药量。\n用户：好的，那饮食上有什么要注意的？\nAI助手：低盐低脂饮食，每日食盐不超过5克，戒烟限酒，适量运动，规律作息。', 1),
(4, '儿童发烧问诊记录', '张小雨', 6, '女', 4, '无', '【问诊名称】儿童发烧问诊记录\n【患者姓名】张小雨\n【年龄】6\n【性别】女\n【问诊科室】儿科\n\n【问诊记录】\n用户：孩子3岁发烧38.5度，精神还可以，需要去医院吗？\nAI助手：体温38.5度以下可先物理降温并观察，若超过38.5度或精神差、呕吐等症状请立即就医。', 1),
(11, '感冒咳嗽问诊记录', '陈强', 35, '男', 6, '有青霉素过敏史', '【问诊名称】感冒咳嗽问诊记录\n【患者姓名】陈强\n【年龄】35\n【性别】男\n【问诊科室】呼吸内科\n【特殊情况备注】有青霉素过敏史\n\n【问诊记录】\n用户：感冒咳嗽三天了，晚上咳得厉害，吃什么药好？\nAI助手：建议多喝温水、注意休息。若咳嗽影响睡眠可对症使用止咳药，症状加重或发热请及时就医。', 0),
(2, '膝盖疼痛复诊记录', '李明', 62, '男', 3, '退行性关节病变', '【问诊名称】膝盖疼痛复诊记录\n【患者姓名】李明\n【年龄】62\n【性别】男\n【问诊科室】骨科\n【特殊情况备注】退行性关节病变\n\n【问诊记录】\n用户：膝盖上下楼梯疼，拍了片子说是退行性病变，怎么锻炼合适？\nAI助手：建议减少爬山爬楼等负重活动，可进行直腿抬高、靠墙静蹲等无负重训练，必要时理疗。', 1),
(2, '糖尿病饮食咨询记录', '王芳', 48, '女', 9, '2型糖尿病3年', '【问诊名称】糖尿病饮食咨询记录\n【患者姓名】王芳\n【年龄】48\n【性别】女\n【问诊科室】内分泌科\n【特殊情况备注】2型糖尿病3年\n\n【问诊记录】\n用户：得了糖尿病，主食应该怎么吃？\nAI助手：主食粗细搭配，控制总量，少食多餐，避免含糖饮料和甜食，配合规律监测血糖。', 0),
(10, '荨麻疹问诊记录', '刘洋', 28, '男', 5, '接触花粉后发作', '【问诊名称】荨麻疹问诊记录\n【患者姓名】刘洋\n【年龄】28\n【性别】男\n【问诊科室】皮肤科\n【特殊情况备注】接触花粉后发作\n\n【问诊记录】\n用户：身上起风团很痒，越抓越多，怎么办？\nAI助手：避免搔抓，可冷敷缓解瘙痒，口服抗组胺药物，若伴呼吸困难需立即就医。', 0),
(11, '偏头痛咨询记录', '周敏', 32, '女', 2, '经期前后发作频繁', '【问诊名称】偏头痛咨询记录\n【患者姓名】周敏\n【年龄】32\n【性别】女\n【问诊科室】神经内科\n【特殊情况备注】经期前后发作频繁\n\n【问诊记录】\n用户：偏头痛发作时有什么缓解办法吗？\nAI助手：发作时建议在安静暗室休息，必要时遵医嘱使用止痛药物。', 1),
(4, '胃部不适问诊记录', '王建国', 56, '男', 7, '既往有胃溃疡史', '【问诊名称】胃部不适问诊记录\n【患者姓名】王建国\n【年龄】56\n【性别】男\n【问诊科室】消化内科\n【特殊情况备注】既往有胃溃疡史\n\n【问诊记录】\n用户：最近总反酸烧心，饭后胃胀，是什么原因？\nAI助手：建议规律饮食、少食多餐，避免辛辣刺激食物，症状持续建议胃镜检查。', 0);

COMMIT;
