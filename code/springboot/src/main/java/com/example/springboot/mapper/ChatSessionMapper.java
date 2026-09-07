package com.example.springboot.mapper;


import com.example.springboot.common.DataRequset.BaseRequest;
import com.example.springboot.entity.ChatSession;
import org.apache.ibatis.annotations.Mapper;

import java.util.List;


@Mapper
public  interface ChatSessionMapper {
    List<ChatSession> list(Integer userId);
    List<ChatSession>  listByCondition(BaseRequest baseRequest);
    void save(ChatSession user);
    ChatSession getById(Integer id);
    void deleteById(Integer id);
    void updateById(ChatSession obj);

    void deleteBysessionId(Integer sessionId);
}
