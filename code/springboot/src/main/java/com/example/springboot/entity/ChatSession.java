package com.example.springboot.entity;
import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.Data;

import java.time.LocalDateTime;
import java.util.Date;

@Data
@TableName("chat_session")
public class ChatSession {
    @TableId(type = IdType.AUTO)
    private Long id;
    private Long userId;
    private String sessionName;
    private LocalDateTime createTime;
    @JsonFormat(pattern = "yyyy-MM-dd",timezone = "GMT+8")
    private Date updateTime;
}
