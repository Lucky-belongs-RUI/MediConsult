package com.example.springboot.service;


import com.example.springboot.common.DataRequset.BaseRequest;
import com.example.springboot.entity.UserAction;
import com.example.springboot.vo.PageVo;

import java.util.List;

public interface UserActionService {
    List<UserAction> list();
    PageVo page(BaseRequest baseRequest);

    void save(UserAction obj);
    UserAction getById(Integer id);
    void update(UserAction obj);
    void deleteById(Integer id);
    void deleteByIds(Integer[] ids);
    List<UserAction> getByitemId(Integer itemId);

}
