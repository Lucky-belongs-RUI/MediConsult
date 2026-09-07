package com.example.springboot.service;


import com.example.springboot.common.DataRequset.BaseRequest;
import com.example.springboot.entity.Favorite;
import com.example.springboot.vo.PageVo;

import java.util.List;

public interface FavoriteService {
    List<Favorite> list();
    PageVo page(BaseRequest baseRequest);

    void save(Favorite obj);

    Favorite getById(Integer id);


    void deleteById(Integer id);


    List<Favorite> getByAllId(Integer itemId);


    Integer getByStatus(Integer itemId, Integer userId);

    List<Favorite> getByUserId(Integer userId);

}
