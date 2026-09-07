package com.example.springboot.service.impl;


import com.example.springboot.dto.ChatMessageSendDTO;
import com.example.springboot.entity.ChatMessage;
import com.example.springboot.mapper.ChatMessageMapper;
import com.example.springboot.mapper.ChatSessionMapper;
import com.example.springboot.service.ChatMessageService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;


@Service
public class ChatMessageServiceImpl implements ChatMessageService {

    @Autowired
    private ChatMessageMapper chatMessageMapper;

    @Autowired
    private ChatSessionMapper chatSessionMapper;

    @Override
    public List<ChatMessage> listBySessionId(Long sessionId) {
        return chatMessageMapper.listBySessionId(sessionId);
    }

    @Override
    public ChatMessage createMessageWithAssistantReply(ChatMessageSendDTO request) {
        if (chatSessionMapper.getById(request.getSessionId().intValue()) == null) {
            return null;
        }

        LocalDateTime now = LocalDateTime.now();

        ChatMessage userMessage = new ChatMessage();
        userMessage.setSessionId(request.getSessionId());
        userMessage.setRole("user");
        userMessage.setContent(request.getContent());
        userMessage.setModel(request.getModel());
        userMessage.setExtraData(request.getExtraData());
        userMessage.setMessageTime(now);
        chatMessageMapper.save(userMessage);

        ChatMessage assistantMessage = new ChatMessage();
        assistantMessage.setSessionId(request.getSessionId());
        assistantMessage.setRole("assistant");
        assistantMessage.setContent("正在思考...");
        assistantMessage.setModel(request.getModel());
        assistantMessage.setExtraData(null);
        assistantMessage.setMessageTime(now);
        chatMessageMapper.save(assistantMessage);

        return assistantMessage;
    }

    @Override
    public void deleteById(Long id) {
        chatMessageMapper.deleteById(id);
    }

    @Override
    public void deleteBySessionId(Long sessionId) {
        chatMessageMapper.deleteBySessionId(sessionId);
    }

    @Override
    public void updateContent(Long id, String content) {
        chatMessageMapper.updateContent(id, content);
    }
}
