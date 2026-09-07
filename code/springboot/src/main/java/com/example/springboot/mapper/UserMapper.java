package com.example.springboot.mapper;



import com.example.springboot.common.DataRequset.BaseRequest;
import com.example.springboot.common.DataRequset.PasswordRequest;
import com.example.springboot.dto.UserLoginDTO;
import com.example.springboot.entity.User;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;


@Mapper
public  interface UserMapper {
    List<User> list();

    List<User>  listByCondition(BaseRequest baseRequest);

    void save(User user);

    User getById(Integer id);

    void updateById(User user);

    void deleteById(Integer id);

    User getByUandP(UserLoginDTO request);

    int updatePasswordById(@Param("userId") Integer userId, @Param("newPassword") String newPassword);

    int updateUserStatusById(Integer userId, Integer status);


    User selectByUsername(@Param("username") String username);

    int updataPassword(PasswordRequest request);

    User getByPass(Integer id ,String oldPassword);

}
