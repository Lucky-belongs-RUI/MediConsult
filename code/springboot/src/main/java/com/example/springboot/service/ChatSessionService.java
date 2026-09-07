package com.example.springboot.service;


import com.example.springboot.common.DataRequset.BaseRequest;
import com.example.springboot.entity.ChatSession;
import com.example.springboot.vo.PageVo;

import java.util.List;

public interface ChatSessionService {
    List<ChatSession> list(Integer userId);
    PageVo page(BaseRequest baseRequest);

    void save(ChatSession obj);

    ChatSession getById(Integer id);


    void deleteById(Integer id);


    void update(ChatSession obj);

    void deleteBysessionId(Integer sessionId);
}
