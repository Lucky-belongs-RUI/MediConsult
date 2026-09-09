package com.example.springboot.service.impl;


import com.example.springboot.common.DataRequset.BaseRequest;
import com.example.springboot.entity.Category;
import com.example.springboot.entity.Item;
import com.example.springboot.entity.UserAction;
import com.example.springboot.mapper.UserActionMapper;
import com.example.springboot.service.CategoryService;
import com.example.springboot.service.ItemService;
import com.example.springboot.service.UserActionService;
import com.example.springboot.vo.PageVo;
import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Arrays;
import java.util.List;

@Service
public class UserActionServiceImpl implements UserActionService {
    @Autowired
    UserActionMapper userActionMapper;
    @Autowired
    ItemService itemService;
    @Autowired
    CategoryService categoryService;

    @Override
    public List<UserAction> list(){
        return userActionMapper.list();
    }

    @Override
    public PageVo page(BaseRequest baseRequest) {
        PageHelper.startPage(baseRequest.getCurrent(), baseRequest.getSize());
        List<UserAction> users = userActionMapper.listByCondition(baseRequest);
        for (UserAction user:users
             ) {
            Item item=itemService.getById2(user.getItemId());
            if (item != null) {
                Category category= categoryService.getById(item.getCategoryId());
                user.setCategory(category);
            }
        }


        PageInfo<UserAction> userPageInfo = new PageInfo(users);

        return new PageVo(userPageInfo);
    }

    @Override
    public UserAction getById(Integer id) {
        return userActionMapper.getById(id);
    }

    @Override
    public void update(UserAction obj) {
        userActionMapper.updateById(obj);

    }

    @Override
    public void deleteById(Integer id) {

        userActionMapper.deleteById(id);

    }

    @Override
    public void deleteByIds(Integer[] ids) {
        if (ids == null || ids.length == 0) {
            return;
        }
        List<Integer> idList = Arrays.asList(ids);
        userActionMapper.deleteByIds(idList);
    }

    @Override
    public List<UserAction> getByitemId(Integer itemId) {
        return userActionMapper.getByitemId(itemId);
    }


    @Override
    public void save(UserAction obj) {


        userActionMapper.save( obj);
    }

}
