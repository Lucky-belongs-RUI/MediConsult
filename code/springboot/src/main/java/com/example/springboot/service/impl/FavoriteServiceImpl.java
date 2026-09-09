package com.example.springboot.service.impl;


import com.example.springboot.common.DataRequset.BaseRequest;
import com.example.springboot.entity.Favorite;
import com.example.springboot.mapper.FavoriteMapper;
import com.example.springboot.service.FavoriteService;
import com.example.springboot.vo.PageVo;
import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class FavoriteServiceImpl implements FavoriteService {
    @Autowired
    FavoriteMapper favoriteMapper;

    @Override
    public List<Favorite> list(){
        return favoriteMapper.list();
    }

    @Override
    public PageVo page(BaseRequest baseRequest) {
        PageHelper.startPage(baseRequest.getCurrent(), baseRequest.getSize());
        List<Favorite> users = favoriteMapper.listByCondition(baseRequest);
        PageInfo<Favorite> userPageInfo = new PageInfo<>(users);

        return new PageVo(userPageInfo);
    }



    @Override
    public Favorite getById(Integer id) {
        return favoriteMapper.getById(id);
    }



    @Override
    public void deleteById(Integer itemId, Integer userId) {

        favoriteMapper.deleteById(itemId, userId);

    }

    @Override
    public List<Favorite> getByAllId(Integer itemId) {
        return favoriteMapper.getByAllId(itemId);
    }

    @Override
    public Integer  getByStatus(Integer itemId, Integer userId) {
        return favoriteMapper.getByStatus( itemId,  userId);
    }

    @Override
    public List<Favorite> getByUserId(Integer userId) {
        return favoriteMapper.getByUserId(userId);
    }


    @Override
    public void save(Favorite obj) {


        favoriteMapper.save( obj);
    }

}
