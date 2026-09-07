package com.example.springboot.service;


import com.example.springboot.common.DataRequset.BaseRequest;
import com.example.springboot.entity.Category;
import com.example.springboot.vo.PageVo;

import java.util.List;

public interface CategoryService {
    List<Category> list();
    PageVo page(BaseRequest baseRequest);

    void save(Category obj);

    Category getById(Integer id);


    void update(Category obj);

    void deleteById(Integer id);




}
