package com.example.springboot.mapper;


import com.example.springboot.common.DataRequset.BaseRequest;
import com.example.springboot.entity.Category;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;


@Mapper
public  interface CategoryMapper {
    List<Category> list();

    List<Category>  listByCondition(BaseRequest baseRequest);

    void save(Category user);

    Category getById(Integer id);

    void updateById(Category user);

    void deleteById(Integer id);
    int countRelatedItem(@Param("categoryId") Integer categoryId);


    Category selectByCategoryname(@Param("name") String username);



}
