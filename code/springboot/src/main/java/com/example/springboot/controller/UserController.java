package com.example.springboot.controller;

import com.example.springboot.common.DataRequset.LoginData;
import com.example.springboot.common.DataRequset.PasswordRequest;
import com.example.springboot.common.DataRequset.UserPageRequest;
import com.example.springboot.common.Result;
import com.example.springboot.dto.UserLoginDTO;
import com.example.springboot.entity.User;
import com.example.springboot.service.ItemService;
import com.example.springboot.service.UserService;
import com.example.springboot.vo.ItemVO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.Date;
import java.util.List;
import java.util.Map;

@CrossOrigin
@RestController
@RequestMapping("/api/user")
public class UserController {



    @Autowired
    UserService userService;




    @PostMapping("/login")
    public Result login(@RequestBody UserLoginDTO request){
        User user= userService.login( request);
        LoginData loginData = new LoginData();
        loginData.setUserInfo(user);
        return Result.success(loginData);


    }
    @PostMapping("/register")
    public Result register(@RequestBody User obj){
        obj.setRole(0);
        userService.save( obj);
        return Result.success("注册成功");
    }
    @PutMapping("/{id}/reset-password")
    public Result resetPassword(
            @PathVariable("id") Integer id) {
        userService.changePass(id);
        return Result.success("密码重置成功");
    }
    @PostMapping("/password")
    public Result resetPassword(@RequestBody PasswordRequest request) {
        userService.updatePassword(request);
        return Result.success("密码修改成功");
    }

    @PostMapping("")
    public Result save(@RequestBody User admin){
        userService.save( admin);
        return Result.success();
    }
    @PostMapping("/logout")
    public Result logout(){
        return Result.success(1);
    }
    @PutMapping("")
    public Result update(@RequestBody User admin){
        admin.setUpdateTime(new Date());
        userService.update(admin);
        return Result.success();
    }
    @GetMapping("/list")
    public Result list(){
        List<User> users=userService.list();
        return Result.success(users);
    }
    @GetMapping("/page")
    public Result page(UserPageRequest pageRequest){

        return Result.success(userService.page(pageRequest));
    }
    @DeleteMapping("/{id}")
    public Result delete(@PathVariable Integer id){
        userService.deleteById(id);
        return Result.success();
    }

    @PutMapping("/{id}/status")
    public Result updateUserStatus(
            @PathVariable("id") Integer id,
            @RequestBody(required = true) Map<String, Integer> statusMap) {

        if (!statusMap.containsKey("status") || statusMap.get("status") == null) {
            return Result.error("用户状态（status）不能为空");
        }
        Integer status = statusMap.get("status");

        userService.updateUserStatus(id, status);
        return Result.success("用户状态修改成功");
    }

    @Autowired
    ItemService itemService;

    @GetMapping("/item/{id}")
    public Result getById(@PathVariable Integer id){
        ItemVO obj=itemService.getById(id);
        return Result.success(obj);
    }


}