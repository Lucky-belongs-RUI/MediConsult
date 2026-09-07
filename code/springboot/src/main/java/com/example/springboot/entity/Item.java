package com.example.springboot.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.Data;

import java.util.Date;

@Data
@TableName("item")
public class Item {
    @TableId(type = IdType.AUTO)
    private Integer id;
    private String title;
    private String description;
    private Integer categoryId;
    private Integer userId;
    private String coverBucket;
    private String coverObjectKey;
    private String fileBucket;
    private String fileObjectKey;
    private String tags;
    private String extraData;
    @JsonFormat(pattern = "yyyy-MM-dd",timezone = "GMT+8")
    private Date createTime;
    @JsonFormat(pattern = "yyyy-MM-dd",timezone = "GMT+8")
    private Date updateTime;
}
