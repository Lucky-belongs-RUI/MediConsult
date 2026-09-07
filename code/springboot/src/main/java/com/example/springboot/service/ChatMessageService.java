package com.example.springboot.service;

import com.example.springboot.entity.ChatMessage;
import com.example.springboot.dto.ChatMessageSendDTO;

import java.util.List;


public interface ChatMessageService {

    List<ChatMessage> listBySessionId(Long sessionId);

    ChatMessage createMessageWithAssistantReply(ChatMessageSendDTO request);

    void deleteById(Long id);

    void deleteBySessionId(Long sessionId);

    void updateContent(Long id, String content);
}