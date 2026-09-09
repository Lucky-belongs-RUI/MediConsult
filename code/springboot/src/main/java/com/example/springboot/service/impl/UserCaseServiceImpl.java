package com.example.springboot.service.impl;

import com.example.springboot.common.DataRequset.UserCasePageRequest;
import com.example.springboot.entity.UserCase;
import com.example.springboot.exception.ServiceException;
import com.example.springboot.mapper.UserCaseMapper;
import com.example.springboot.service.ItemService;
import com.example.springboot.service.UserCaseService;
import com.example.springboot.vo.ItemVO;
import com.example.springboot.vo.PageVo;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class UserCaseServiceImpl implements UserCaseService {
    @Autowired
    UserCaseMapper userCaseMapper;

    @Autowired
    ItemService itemService;

    private static final ObjectMapper OBJECT_MAPPER = new ObjectMapper();

    @Override
    public PageVo page(UserCasePageRequest request) {
        PageHelper.startPage(request.getCurrent(), request.getSize());
        List<UserCase> list = userCaseMapper.listByCondition(request);
        return new PageVo(new PageInfo<>(list));
    }

    @Override
    public void save(UserCase obj) {
        if (obj.getUserId() == null) {
            throw new ServiceException("用户ID不能为空");
        }
        if (obj.getTitle() == null || obj.getTitle().trim().isEmpty()) {
            throw new ServiceException("问诊名称不能为空");
        }
        if (obj.getIsPublic() == null) {
            obj.setIsPublic(0);
        }
        userCaseMapper.save(obj);
    }

    @Override
    public UserCase getById(Integer id) {
        UserCase obj = userCaseMapper.getById(id);
        if (obj == null) {
            throw new ServiceException("病例不存在");
        }
        return obj;
    }

    @Override
    public void update(UserCase obj) {
        if (obj.getId() == null) {
            throw new ServiceException("病例ID不能为空");
        }
        userCaseMapper.updateById(obj);

        // 若已发布到病例库，同步更新对应病例记录
        UserCase full = userCaseMapper.getById(obj.getId());
        if (full != null && full.getItemId() != null) {
            ItemVO item = buildItemVO(full);
            item.setId(full.getItemId().longValue());
            itemService.update(item);
        }
    }

    @Override
    public void deleteById(Integer id) {
        UserCase obj = userCaseMapper.getById(id);
        if (obj != null && obj.getItemId() != null) {
            // 已公开的病例同步从病例库下架删除
            itemService.deleteById(obj.getItemId());
        }
        userCaseMapper.deleteById(id);
    }

    @Override
    public void updateVisibility(Integer id, Integer isPublic) {
        if (id == null) {
            throw new ServiceException("病例ID不能为空");
        }
        if (isPublic == null || (isPublic != 0 && isPublic != 1)) {
            throw new ServiceException("公开状态不合法，仅支持0（私有）或1（公开）");
        }
        UserCase obj = userCaseMapper.getById(id);
        if (obj == null) {
            throw new ServiceException("病例不存在");
        }

        if (isPublic == 1) {
            // 公开：发布到病例库（item 表），与现有公开病例同界面展示
            if (obj.getItemId() == null) {
                ItemVO item = buildItemVO(obj);
                itemService.save(item);
                if (item.getId() != null) {
                    userCaseMapper.updateItemId(id, item.getId().intValue());
                }
            }
            userCaseMapper.updateVisibility(id, 1);
        } else {
            // 取消公开：从病例库下架对应病例记录
            if (obj.getItemId() != null) {
                itemService.deleteById(obj.getItemId());
                userCaseMapper.updateItemId(id, null);
            }
            userCaseMapper.updateVisibility(id, 0);
        }
    }

    /**
     * 组装病例库（item）记录：优先使用 AI 结构化摘要（ai_summary）中的
     * title/description/tags/category_id，并将完整结构化 JSON 写入 extra_data；
     * 缺失时回退到简洁基础信息，避免把原始问诊对话全文直接铺到病例库。
     */
    private ItemVO buildItemVO(UserCase obj) {
        ItemVO item = new ItemVO();
        item.setTitle(obj.getTitle());
        item.setCategoryId(obj.getCategoryId() == null ? null : obj.getCategoryId().longValue());
        item.setUserId(obj.getUserId() == null ? null : obj.getUserId().longValue());
        item.setTags("公开病例");

        StringBuilder fallback = new StringBuilder();
        fallback.append(obj.getTitle() == null ? "未命名病例" : obj.getTitle());
        if (obj.getPatientName() != null && !obj.getPatientName().trim().isEmpty()) {
            fallback.append("，患者").append(obj.getPatientName().trim());
        }
        if (obj.getAge() != null) {
            fallback.append("，").append(obj.getAge()).append("岁");
        }
        if (obj.getGender() != null && !obj.getGender().trim().isEmpty()) {
            fallback.append("，").append(obj.getGender().trim());
        }
        fallback.append("。详细问诊记录见原病例。");
        item.setDescription(fallback.toString());

        String summary = obj.getAiSummary();
        if (summary != null && !summary.trim().isEmpty()) {
            try {
                JsonNode node = OBJECT_MAPPER.readTree(summary);
                if (node.hasNonNull("title") && !node.get("title").asText().trim().isEmpty()) {
                    item.setTitle(node.get("title").asText().trim());
                }
                if (node.hasNonNull("description") && !node.get("description").asText().trim().isEmpty()) {
                    item.setDescription(node.get("description").asText().trim());
                }
                if (node.hasNonNull("tags") && !node.get("tags").asText().trim().isEmpty()) {
                    item.setTags(node.get("tags").asText().trim());
                }
                if (node.hasNonNull("category_id") && node.get("category_id").canConvertToInt()) {
                    item.setCategoryId(node.get("category_id").asLong());
                }
                // 完整结构化 JSON 一并存入 extra_data，供病例库详情页渲染病例详情表格
                item.setExtraData(summary);
            } catch (Exception e) {
                // AI 摘要解析失败时使用基础信息兜底
            }
        }
        return item;
    }
}
