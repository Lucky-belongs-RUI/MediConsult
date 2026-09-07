package com.example.springboot.service;


import com.example.springboot.common.DataRequset.BaseRequest;
import com.example.springboot.entity.Like;
import com.example.springboot.vo.PageVo;

import java.util.List;

public interface LikeService {
    List<Like> list();
    PageVo page(BaseRequest baseRequest);

    void save(Like obj);

    Like getById(Integer id);


    void deleteById(Integer id);


    List<Like> getByAllId(Integer itemId);


    Integer getByStatus(Integer itemId, Integer userId);

    List<Like> getByUserId(Integer userId);

}
