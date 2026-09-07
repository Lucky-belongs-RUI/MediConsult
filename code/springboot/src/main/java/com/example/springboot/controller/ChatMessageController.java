package com.example.springboot.controller;

import com.example.springboot.common.Result;
import com.example.springboot.dto.ChatMessageSendDTO;
import com.example.springboot.dto.ChatMessageUpdateContentDTO;
import com.example.springboot.entity.ChatMessage;
import com.example.springboot.service.ChatMessageService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@CrossOrigin
@RestController
@RequestMapping("/api/chat")
public class ChatMessageController {

    @Autowired
    private ChatMessageService chatMessageService;

    @GetMapping("/messages")
    public Result listMessages(@RequestParam("sessionId") Long sessionId) {
        List<ChatMessage> data = chatMessageService.listBySessionId(sessionId);
        return Result.success(data);
    }

    @PostMapping("/messages")
    public Result sendMessage(@Validated @RequestBody ChatMessageSendDTO request) {
        ChatMessage assistantMessage = chatMessageService.createMessageWithAssistantReply(request);
        if (assistantMessage == null) {
            return Result.error("会话不存在");
        }
        return Result.success(assistantMessage);
    }

    @DeleteMapping("/messages/{id}")
    public Result deleteMessage(@PathVariable("id") Long id) {
        chatMessageService.deleteById(id);
        return Result.success();
    }

    @PutMapping("/messages/{id}/content")
    public Result updateMessageContent(@PathVariable("id") Long id,
                                       @Validated @RequestBody ChatMessageUpdateContentDTO request) {
        chatMessageService.updateContent(id, request.getContent());
        return Result.success();
    }
}
