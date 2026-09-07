package com.example.springboot.controller;


import com.example.springboot.common.DataRequset.CommentPageRequest;
import com.example.springboot.common.Result;
import com.example.springboot.entity.Comment;
import com.example.springboot.service.CommentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;


@CrossOrigin
@RestController
@RequestMapping("/api/comment")
public class CommentController {


    @Autowired
    CommentService commentService;

    


    @PostMapping("")
    public Result save(@RequestBody Comment obj){

        commentService.save(obj);
        return Result.success();
    }

    @GetMapping("/list")
    public Result list(){
        List<Comment> users=commentService.list();
        return Result.success(users);
    }


    @GetMapping("/{commentId}")

    public Result getById(@PathVariable Integer commentId){
        Comment obj=commentService.getById(commentId);
        return Result.success(obj);
    }

    @GetMapping("/page")
    public Result page(CommentPageRequest pageRequest){

        return Result.success(commentService.page(pageRequest));
    }
    @DeleteMapping("/{id}")
    public Result delete(@PathVariable Integer id){
        commentService.deleteById(id);
        return Result.success();
    }
    @GetMapping("/tree/{itemId}")
    public Result getCommentTree(@PathVariable("itemId") Integer itemId) {
        List<Comment> commentTree = commentService.getCommentTree(itemId);
        return Result.success(commentTree);
    }



}