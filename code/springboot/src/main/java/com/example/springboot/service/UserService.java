package com.example.springboot.service;


import com.example.springboot.common.DataRequset.BaseRequest;
import com.example.springboot.common.DataRequset.PasswordRequest;
import com.example.springboot.dto.UserLoginDTO;
import com.example.springboot.entity.User;
import com.example.springboot.vo.PageVo;

import java.util.List;

public interface UserService {
    List<User> list();
    PageVo page(BaseRequest baseRequest);

    void save(User obj);

    User getById(Integer id);


    void update(User obj);

    void deleteById(Integer id);

    User login(UserLoginDTO request);

    void changePass(Integer id);

    void updateUserStatus(Integer userId, Integer status);

    void updatePassword(PasswordRequest request);
}
