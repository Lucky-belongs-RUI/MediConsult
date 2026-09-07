package com.example.springboot.controller;


import com.example.springboot.common.DataRequset.ItemPageRequest;
import com.example.springboot.common.Result;
import com.example.springboot.entity.Item;
import com.example.springboot.service.ItemService;
import com.example.springboot.vo.ItemVO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.Date;
import java.util.List;


@CrossOrigin
@RestController
@RequestMapping("/api/item")
public class ItemController {


    @Autowired
    ItemService itemService;


    @PostMapping("")
    public Result save(@RequestBody ItemVO obj){
        itemService.save(obj);
        return Result.success();
    }
    @PutMapping("")
    public Result update(@RequestBody ItemVO obj){
        obj.setUpdateTime(new Date());

        itemService.update(obj);
        return Result.success();
    }
    @GetMapping("/list")
    public Result list(){
        List<Item> users=itemService.list();
        return Result.success(users);
    }
    @GetMapping("/list/category/{id}")
    public Result listCategoryId(@PathVariable Integer id){
        List<ItemVO> users=itemService.listCategoryId(id);
        return Result.success(users);
    }
    @GetMapping("/{id}")
    public Result getById(@PathVariable Integer id){
        ItemVO obj=itemService.getById(id);
        return Result.success(obj);
    }

    @GetMapping("/page")
    public Result page(ItemPageRequest pageRequest){
        return Result.success(itemService.page(pageRequest));
    }
    @DeleteMapping("/{id}")
    public Result delete(@PathVariable Integer id){
        itemService.deleteById(id);
        return Result.success();
    }



}