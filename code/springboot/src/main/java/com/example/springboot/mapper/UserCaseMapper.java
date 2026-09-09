package com.example.springboot.mapper;


import com.example.springboot.common.DataRequset.UserCasePageRequest;
import com.example.springboot.entity.UserCase;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

@Mapper
public interface UserCaseMapper {
    List<UserCase> listByCondition(UserCasePageRequest request);

    void save(UserCase obj);

    UserCase getById(Integer id);

    void updateById(UserCase obj);

    void deleteById(Integer id);

    void updateVisibility(@Param("id") Integer id, @Param("isPublic") Integer isPublic);

    void updateItemId(@Param("id") Integer id, @Param("itemId") Integer itemId);
}
