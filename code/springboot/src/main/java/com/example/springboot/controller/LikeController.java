package com.example.springboot.controller;


import com.example.springboot.common.DataRequset.FavoritePageRequest;
import com.example.springboot.common.Result;
import com.example.springboot.entity.Like;
import com.example.springboot.service.LikeService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;


@CrossOrigin
@RestController
@RequestMapping("/api/like")
public class LikeController {


    @Autowired
    LikeService likeService;

    


    @PostMapping("")
    public Result save(@RequestBody Like obj){
        likeService.save(obj);
        return Result.success();
    }

    @GetMapping("/list")
    public Result list(){
        List<Like> users=likeService.list();
        return Result.success(users);
    }
    @GetMapping("/status/{itemId}/{userId}")
    public Result getByStatus(@PathVariable("itemId") Integer itemId, @PathVariable Integer userId
    ) {
        Integer  status=likeService.getByStatus(itemId, userId);
        return Result.success(status);
    }

    @GetMapping("/count/{ItemId}")
    public Result getByAllId(@PathVariable Integer ItemId){
        List<Like> obj=likeService.getByAllId(ItemId);
        return Result.success(obj.size());
    }
    @GetMapping("/user/items/{userId}")
    public Result getByuserId(@PathVariable Integer userId){
        List<Like> obj=likeService.getByUserId(userId);
        return Result.success(obj);
    }

    @GetMapping("/user/page")
    public Result page(FavoritePageRequest pageRequest){
        return Result.success(likeService.page(pageRequest));
    }
    @DeleteMapping("/{itemId}")
    public Result delete(@PathVariable Integer itemId, @RequestParam Integer userId){
        likeService.deleteById(itemId, userId);
        return Result.success();
    }



}