package com.example.springboot.controller;


import com.example.springboot.common.DataRequset.CategoryPageRequest;
import com.example.springboot.common.Result;

import com.example.springboot.entity.Category;
import com.example.springboot.service.CategoryService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.Date;
import java.util.List;


@CrossOrigin
@RestController
@RequestMapping("/api/category")
public class CategoryController {


    @Autowired
    CategoryService categoryService;

    


    @PostMapping("")
    public Result save(@RequestBody Category obj){
        categoryService.save(obj);
        return Result.success();
    }
    @PutMapping("")
    public Result update(@RequestBody Category obj){
        obj.setUpdateTime(new Date());
        categoryService.update(obj);
        return Result.success();
    }
    @GetMapping("/list")
    public Result list(){
        List<Category> users=categoryService.list();
        return Result.success(users);
    }
    @GetMapping("/{id}")
    public Result getById(@PathVariable Integer id){
        Category obj=categoryService.getById(id);
        return Result.success(obj);
    }

    @GetMapping("/page")
    public Result page(CategoryPageRequest pageRequest){

        return Result.success(categoryService.page(pageRequest));
    }
    @DeleteMapping("/{id}")
    public Result delete(@PathVariable Integer id){
        categoryService.deleteById(id);
        return Result.success();
    }



}