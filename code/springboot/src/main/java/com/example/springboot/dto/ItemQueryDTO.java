package com.example.springboot.dto;

import lombok.Data;

@Data
public class ItemQueryDTO {

    private String title;

    private Long categoryId;
    private String tag;
    private String userRealName;
}
