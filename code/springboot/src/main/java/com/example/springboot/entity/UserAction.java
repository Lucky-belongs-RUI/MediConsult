package com.example.springboot.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import lombok.Data;

import java.time.LocalDateTime;

@Data
@TableName("user_action")
public class UserAction {
    @TableId(type = IdType.AUTO)
    private Integer id;
    private Integer userId;
    private Integer itemId;
    private Integer actionType;
    private String extraData;
    private String username;
    private String itemTitle;
    @com.baomidou.mybatisplus.annotation.TableField(exist = false)
    private Category category;
    private LocalDateTime createTime;
}
