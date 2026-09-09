package com.example.springboot.mapper;


import com.example.springboot.common.DataRequset.BaseRequest;
import com.example.springboot.entity.Favorite;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;


@Mapper
public  interface FavoriteMapper {
    List<Favorite> list();

    List<Favorite>  listByCondition(BaseRequest baseRequest);

    void save(Favorite user);

    Favorite getById(Integer id);

    void deleteById(@Param("itemId") Integer itemId, @Param("userId") Integer userId);


    List<Favorite> getByAllId(Integer itemId);

    Integer  getByStatus(Integer itemId, Integer userId);

    List<Favorite> getByUserId(Integer userId);
}
