package com.example.springboot.service.impl;


import com.example.springboot.common.DataRequset.BaseRequest;
import com.example.springboot.entity.ChatSession;
import com.example.springboot.mapper.ChatSessionMapper;
import com.example.springboot.service.ChatSessionService;
import com.example.springboot.vo.PageVo;
import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ChatSessionServiceImpl implements ChatSessionService {
    @Autowired
    ChatSessionMapper chatSessionMapper;

    @Override
    public List<ChatSession> list(Integer userId){
        return chatSessionMapper.list(userId);
    }

    @Override
    public PageVo page(BaseRequest baseRequest) {
        PageHelper.startPage(baseRequest.getCurrent(), baseRequest.getSize());
        List<ChatSession> users = chatSessionMapper.listByCondition(baseRequest);
        PageInfo<ChatSession> userPageInfo = new PageInfo<>(users);

        return new PageVo(userPageInfo);
    }



    @Override
    public ChatSession getById(Integer id) {
        return chatSessionMapper.getById(id);
    }



    @Override
    public void deleteById(Integer id) {

        chatSessionMapper.deleteById(id);

    }

    @Override
    public void update(ChatSession obj) {
        chatSessionMapper.updateById(obj);
    }

    @Override
    public void deleteBysessionId(Integer sessionId) {
        chatSessionMapper.deleteBysessionId(sessionId);
    }


    @Override
    public void save(ChatSession obj) {


        chatSessionMapper.save( obj);
    }

}
