package com.example.springboot.service.impl;



import com.example.springboot.common.DataRequset.BaseRequest;
import com.example.springboot.common.DataRequset.PasswordRequest;
import com.example.springboot.dto.UserLoginDTO;
import com.example.springboot.entity.User;
import com.example.springboot.exception.ServiceException;
import com.example.springboot.mapper.UserMapper;
import com.example.springboot.service.UserService;

import com.example.springboot.vo.PageVo;
import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class UserServiceImpl implements UserService {
    @Autowired
    UserMapper userMapper;

    @Override
    public List<User> list(){
        return userMapper.list();
    }

    @Override
    public PageVo page(BaseRequest baseRequest) {
        PageHelper.startPage(baseRequest.getCurrent(), baseRequest.getSize());
        List<User> users = userMapper.listByCondition(baseRequest);
        PageInfo<User> userPageInfo = new PageInfo<>(users);
        return new PageVo(userPageInfo);
    }



    @Override
    public User getById(Integer id) {
        return userMapper.getById(id);
    }

    @Override
    public void update(User user) {
        User user1=userMapper.getById(user.getId());
        user1.setAvatarBucket(user.getAvatarBucket());
        user1.setAvatarObjectKey(user.getAvatarObjectKey());
        userMapper.updateById(user1);

    }

    @Override
    public void deleteById(Integer id) {
        userMapper.deleteById(id);

    }

    @Override
    public User login(UserLoginDTO request) {
        User User = userMapper.getByUandP(request);
        if (User==null){
            throw new ServiceException("用户名或密码错误");
        }
        return User;

    }

    @Override
    public void changePass(Integer id) {
        if (id == null) {
            throw new ServiceException("用户ID不能为空");
        }

        String newPassword = "123456";

        int rows = userMapper.updatePasswordById(id, newPassword);

        if (rows <= 0) {
            throw new ServiceException("修改密码失败，用户ID不存在或未更新");
        }
    }


    @Override
    public void updateUserStatus(Integer userId, Integer status) {

        User existingUser = userMapper.getById(userId);
        if (existingUser == null) {
            throw new ServiceException("用户不存在，无法修改状态");
        }


        if (status != 0 && status != 1) {
            throw new ServiceException("用户状态不合法，仅支持0（正常）或1（禁用）");
        }


        int rows = userMapper.updateUserStatusById(userId, status);
        if (rows <= 0) {
            throw new ServiceException("用户状态修改失败");
        }
    }

    @Override
    public void updatePassword(PasswordRequest request) {
        int i = userMapper.updataPassword(request);
        User admin = userMapper.getByPass(request.getId(),request.getOldPassword());
        if (admin==null){
            throw new ServiceException("原密码错误");
        }
        if (i<=0){
            throw new ServiceException("修改密码失败");
        }

    }

    @Override
    public void save(User user) {
        String username = user.getUsername();
        User existingUser = userMapper.selectByUsername(username);
        if (existingUser != null) {
            throw new ServiceException("用户名【" + username + "】已存在，请更换其他用户名");
        }

        if (user.getStatus() == null) {
            user.setStatus(0);
        }


        userMapper.save( user);
    }

}
