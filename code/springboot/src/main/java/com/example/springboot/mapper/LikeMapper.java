package com.example.springboot.mapper;


import com.example.springboot.common.DataRequset.BaseRequest;
import com.example.springboot.entity.Like;
import org.apache.ibatis.annotations.Mapper;

import java.util.List;


@Mapper
public  interface LikeMapper {
    List<Like> list();

    List<Like>  listByCondition(BaseRequest baseRequest);

    void save(Like user);

    Like getById(Integer id);

    void deleteById(Integer id);


    List<Like> getByAllId(Integer itemId);

    Integer  getByStatus(Integer itemId, Integer userId);

    List<Like> getByUserId(Integer userId);
}
