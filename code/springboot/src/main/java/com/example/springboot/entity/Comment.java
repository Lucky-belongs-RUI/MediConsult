package com.example.springboot.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Data
@TableName("comment")
public class Comment {
    @TableId(type = IdType.AUTO)
    private Long id;
    private Long userId;
    @TableField(exist = false)
    private User userInfo;
    private Long itemId;
    private String content;
    private Long parentId;
    private Long replyToCommentId;
    private Long replyToUserId;
    @TableField(exist = false)
    private User replyToUserInfo;
    private LocalDateTime createTime;
    private LocalDateTime updateTime;
    @TableField(exist = false)
    private List<Comment> replies = new ArrayList<>();
}
