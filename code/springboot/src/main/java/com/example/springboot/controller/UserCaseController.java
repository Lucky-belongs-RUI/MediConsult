package com.example.springboot.controller;

import com.example.springboot.common.DataRequset.UserCasePageRequest;
import com.example.springboot.common.Result;
import com.example.springboot.entity.UserCase;
import com.example.springboot.service.UserCaseService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.Date;
import java.util.Map;

@CrossOrigin
@RestController
@RequestMapping("/api/user-case")
public class UserCaseController {

    @Autowired
    UserCaseService userCaseService;

    /** 记录病例（保存问诊结果） */
    @PostMapping("")
    public Result save(@RequestBody UserCase obj) {
        obj.setCreateTime(new Date());
        obj.setUpdateTime(new Date());
        userCaseService.save(obj);
        return Result.success(obj.getId());
    }

    /** 我的病例（分页） */
    @GetMapping("/my")
    public Result myPage(UserCasePageRequest pageRequest) {
        return Result.success(userCaseService.page(pageRequest));
    }

    /** 公开病例（分页） */
    @GetMapping("/public")
    public Result publicPage(UserCasePageRequest pageRequest) {
        pageRequest.setIsPublic(1);
        return Result.success(userCaseService.page(pageRequest));
    }

    /** 病例详情 */
    @GetMapping("/{id}")
    public Result getById(@PathVariable Integer id) {
        return Result.success(userCaseService.getById(id));
    }

    /** 更新病例 */
    @PutMapping("")
    public Result update(@RequestBody UserCase obj) {
        obj.setUpdateTime(new Date());
        userCaseService.update(obj);
        return Result.success();
    }

    /** 公开 / 取消公开 */
    @PutMapping("/visibility")
    public Result updateVisibility(@RequestBody Map<String, Integer> body) {
        Integer id = body.get("id");
        Integer isPublic = body.get("isPublic");
        userCaseService.updateVisibility(id, isPublic);
        return Result.success("操作成功");
    }

    /** 删除病例 */
    @DeleteMapping("/{id}")
    public Result delete(@PathVariable Integer id) {
        userCaseService.deleteById(id);
        return Result.success();
    }
}
