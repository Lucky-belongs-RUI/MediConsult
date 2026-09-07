package com.example.springboot.mapper;


import com.example.springboot.entity.ChatMessage;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

@Mapper
public interface ChatMessageMapper {
    List<ChatMessage> listBySessionId(@Param("sessionId") Long sessionId);

    void save(ChatMessage message);

    ChatMessage getById(@Param("id") Long id);

    void deleteById(@Param("id") Long id);

    void deleteBySessionId(@Param("sessionId") Long sessionId);

    void updateContent(@Param("id") Long id, @Param("content") String content);
}
