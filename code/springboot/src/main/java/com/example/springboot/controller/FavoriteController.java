package com.example.springboot.controller;


import com.example.springboot.common.DataRequset.FavoritePageRequest;
import com.example.springboot.common.Result;
import com.example.springboot.entity.Favorite;
import com.example.springboot.service.FavoriteService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;


@CrossOrigin
@RestController
@RequestMapping("/api/favorite")
public class FavoriteController {


    @Autowired
    FavoriteService favoriteService;

    


    @PostMapping("")
    public Result save(@RequestBody Favorite obj){
        favoriteService.save(obj);
        return Result.success();
    }

    @GetMapping("/list")
    public Result list(){
        List<Favorite> users=favoriteService.list();
        return Result.success(users);
    }
    @GetMapping("/status/{itemId}/{userId}")
    public Result getByStatus(@PathVariable("itemId") Integer itemId, @PathVariable Integer userId
    ) {
        Integer  status=favoriteService.getByStatus(itemId, userId);
        return Result.success(status);
    }

    @GetMapping("/count/{ItemId}")
    public Result getByAllId(@PathVariable Integer ItemId){
        List<Favorite> obj=favoriteService.getByAllId(ItemId);
        return Result.success(obj.size());
    }
    @GetMapping("/user/items/{userId}")
    public Result getByuserId(@PathVariable Integer userId){
        List<Favorite> obj=favoriteService.getByUserId(userId);
        return Result.success(obj);
    }

    @GetMapping("/user/page")
    public Result page(FavoritePageRequest pageRequest){


        return Result.success(favoriteService.page(pageRequest));
    }
    @DeleteMapping("/{itemId}")
    public Result delete(@PathVariable Integer itemId, @RequestParam Integer userId){
        favoriteService.deleteById(itemId, userId);
        return Result.success();
    }



}