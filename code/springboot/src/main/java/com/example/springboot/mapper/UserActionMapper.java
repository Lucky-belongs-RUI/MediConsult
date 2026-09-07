package com.example.springboot.mapper;


import com.example.springboot.common.DataRequset.BaseRequest;
import com.example.springboot.entity.UserAction;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;


@Mapper
public  interface UserActionMapper {
    List<UserAction> list();

    List<UserAction>  listByCondition(BaseRequest baseRequest);

    void save(UserAction user);

    UserAction getById(Integer id);

    void updateById(UserAction user);

    void deleteById(Integer id);
    void deleteByIds(@Param("idList") List<Integer> ids);

    List<UserAction> getByitemId(Integer itemId);

}
