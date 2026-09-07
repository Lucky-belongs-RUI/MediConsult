package com.example.springboot.service.impl;


import com.example.springboot.common.DataRequset.BaseRequest;
import com.example.springboot.config.FileServiceConfig;

import com.example.springboot.entity.Category;
import com.example.springboot.exception.ServiceException;
import com.example.springboot.mapper.CategoryMapper;

import com.example.springboot.service.CategoryService;

import com.example.springboot.vo.PageVo;
import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class CategoryServiceImpl implements CategoryService {
    @Autowired
    CategoryMapper categoryMapper;

    @Autowired
    FileServiceConfig fileServiceConfig;

    private String buildFileUrl(String bucket, String objectKey) {
        if (bucket == null || bucket.isEmpty() || objectKey == null || objectKey.isEmpty()) {
            return null;
        }
        return fileServiceConfig.getUrl() + "/file/" + bucket + "/" + objectKey;
    }

    @Override
    public List<Category> list(){
        List<Category> list = categoryMapper.list();
        list.forEach(c -> c.setIconUrl(buildFileUrl(c.getIconBucket(), c.getIconObjectKey())));
        return list;
    }

    @Override
    public PageVo page(BaseRequest baseRequest) {
        PageHelper.startPage(baseRequest.getCurrent(), baseRequest.getSize());
        List<Category> users = categoryMapper.listByCondition(baseRequest);
        users.forEach(c -> c.setIconUrl(buildFileUrl(c.getIconBucket(), c.getIconObjectKey())));
        PageInfo<Category> userPageInfo = new PageInfo<>(users);

        return new PageVo(userPageInfo);
    }



    @Override
    public Category getById(Integer id) {
        Category category = categoryMapper.getById(id);
        if (category != null) {
            category.setIconUrl(buildFileUrl(category.getIconBucket(), category.getIconObjectKey()));
        }
        return category;
    }

    @Override
    public void update(Category obj) {
        categoryMapper.updateById(obj);

    }

    @Override
    public void deleteById(Integer id) {
        int relatedCount = categoryMapper.countRelatedItem(id);

        if (relatedCount > 0) {
            throw new ServiceException("该科室下有关联的病例，将无法删除");
        }

        categoryMapper.deleteById(id);

    }



    @Override
    public void save(Category obj) {
        String username = obj.getName();
        Category existingUser = categoryMapper.selectByCategoryname(username);
        if (existingUser != null) {
            throw new ServiceException("科室名【" + username + "】已存在，请更换其他用户名");
        }



        categoryMapper.save( obj);
    }

}
