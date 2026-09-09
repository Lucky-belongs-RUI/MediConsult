package com.example.springboot.service;

import com.example.springboot.common.DataRequset.UserCasePageRequest;
import com.example.springboot.entity.UserCase;
import com.example.springboot.vo.PageVo;

public interface UserCaseService {
    PageVo page(UserCasePageRequest request);

    void save(UserCase obj);

    UserCase getById(Integer id);

    void update(UserCase obj);

    void deleteById(Integer id);

    void updateVisibility(Integer id, Integer isPublic);
}
