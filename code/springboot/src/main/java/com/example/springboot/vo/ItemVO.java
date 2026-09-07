package com.example.springboot.vo;

import com.example.springboot.entity.Category;
import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.Data;

import java.util.Date;

@Data
public class ItemVO   {

        private Long id;
        private String title;
        private String description;
        private String coverUrl;
        private String coverObjectKey;
        private String coverBucket;
        private String fileUrl;
        private String fileObjectKey;
        private String fileBucket;
        private String tags;
        private String extraData;
        private Category category;
        private Long userId;
        private Long categoryId;
        private String userRealName;
        @JsonFormat(pattern = "yyyy-MM-dd",timezone = "GMT+8")
        private Date createTime;
        @JsonFormat(pattern = "yyyy-MM-dd",timezone = "GMT+8")
        private Date updateTime;
        private Integer favorites;
        private Integer views;


}
