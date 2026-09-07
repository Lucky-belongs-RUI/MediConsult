package com.example.springboot.service.impl;


import com.example.springboot.common.DataRequset.BaseRequest;
import com.example.springboot.entity.Like;
import com.example.springboot.mapper.LikeMapper;
import com.example.springboot.service.LikeService;
import com.example.springboot.vo.PageVo;
import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class LikeServiceImpl implements LikeService {
    @Autowired
    LikeMapper likeMapper;

    @Override
    public List<Like> list(){
        return likeMapper.list();
    }

    @Override
    public PageVo page(BaseRequest baseRequest) {
        PageHelper.startPage(baseRequest.getCurrent(), baseRequest.getSize());
        List<Like> users = likeMapper.listByCondition(baseRequest);
        PageInfo<Like> userPageInfo = new PageInfo<>(users);

        return new PageVo(userPageInfo);
    }



    @Override
    public Like getById(Integer id) {
        return likeMapper.getById(id);
    }



    @Override
    public void deleteById(Integer id) {

        likeMapper.deleteById(id);

    }

    @Override
    public List<Like> getByAllId(Integer itemId) {
        return likeMapper.getByAllId(itemId);
    }

    @Override
    public Integer  getByStatus(Integer itemId, Integer userId) {
        return likeMapper.getByStatus( itemId,  userId);
    }

    @Override
    public List<Like> getByUserId(Integer userId) {
        return likeMapper.getByUserId(userId);
    }


    @Override
    public void save(Like obj) {


        likeMapper.save( obj);
    }

}
