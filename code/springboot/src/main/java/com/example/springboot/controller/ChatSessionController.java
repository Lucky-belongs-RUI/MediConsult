package com.example.springboot.controller;


import com.example.springboot.common.Result;
import com.example.springboot.entity.ChatSession;
import com.example.springboot.service.ChatSessionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.Date;
import java.util.List;


@CrossOrigin
@RestController
@RequestMapping("/api/chat")
public class ChatSessionController {


    @Autowired
    ChatSessionService chatSessionService;

    @PostMapping("/sessions")
    public Result save(@RequestBody ChatSession obj){
        chatSessionService.save(obj);
        return Result.success(obj);
    }

    @GetMapping("/user/{userId}")
    public Result list(@PathVariable Integer userId){
        List<ChatSession> users=chatSessionService.list(userId);
        return Result.success(users);
    }
    @PutMapping("/sessions/{id}")
    public Result update(@RequestBody ChatSession obj){
        obj.setUpdateTime(new Date());
        chatSessionService.update(obj);
        return Result.success();
    }

    @GetMapping("/sessions/{id}")

    public Result getById(@PathVariable Integer id){
        ChatSession obj=chatSessionService.getById(id);
        return Result.success(obj);
    }

    @DeleteMapping("/sessions/{id}")
    public Result delete(@PathVariable Integer id){
        chatSessionService.deleteById(id);
        return Result.success();
    }
    @DeleteMapping("/sessions/{sessionId}/messages")
    public Result deleteById(@PathVariable Integer sessionId){
        chatSessionService.deleteBysessionId(sessionId);
        return Result.success();
    }



}