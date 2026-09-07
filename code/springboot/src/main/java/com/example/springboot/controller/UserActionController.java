package com.example.springboot.controller;


import com.example.springboot.common.DataRequset.UserActionPageRequest;
import com.example.springboot.common.Result;
import com.example.springboot.entity.UserAction;
import com.example.springboot.service.UserActionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;


@CrossOrigin
@RestController
@RequestMapping("/api/user-action")
public class UserActionController {


    @Autowired
    UserActionService userActionService;

    


    @PostMapping("")
    public Result save(@RequestBody UserAction obj){
        userActionService.save(obj);
        return Result.success(1);
    }
    @PutMapping("")
    public Result update(@RequestBody UserAction obj){
        userActionService.update(obj);
        return Result.success();
    }
    @GetMapping("")
    public Result list(){
        List<UserAction> users=userActionService.list();
        return Result.success(users);
    }
    @GetMapping("/{id}")
    public Result getById(@PathVariable Integer id){
        UserAction obj=userActionService.getById(id);
        return Result.success(obj);
    }
    @GetMapping("/view/count/{itemId}")
    public Result getByitemId(@PathVariable Integer itemId){
        List<UserAction> obj=userActionService.getByitemId(itemId);
        return Result.success(obj.size());
    }
    @GetMapping("/admin/page")
    public Result page(UserActionPageRequest pageRequest){

        return Result.success(userActionService.page(pageRequest));
    }
    @GetMapping("/page")
    public Result pageByUser(UserActionPageRequest pageRequest){
        return Result.success(userActionService.page(pageRequest));
    }

    @DeleteMapping("/batch")
    public Result deleteBatch(
            @RequestBody(required = false) Integer[] ids
    ) {
        if (ids == null || ids.length == 0) {
            return Result.error("请选择要删除的记录（未传入有效 IDs）");
        }
        try {
            userActionService.deleteByIds(ids);
            return Result.success(ids.length);
        } catch (Exception e) {
            return Result.error("批量删除失败：" + e.getMessage());
        }
    }
    @DeleteMapping("/my/batch")
    public Result deletemyBatch(
            @RequestBody(required = false) Integer[] ids
    ) {
        if (ids == null || ids.length == 0) {
            return Result.error("请选择要删除的记录（未传入有效 IDs）");
        }
        try {
            userActionService.deleteByIds(ids);
            return Result.success(ids.length);
        } catch (Exception e) {
            return Result.error("批量删除失败：" + e.getMessage());
        }
    }


}