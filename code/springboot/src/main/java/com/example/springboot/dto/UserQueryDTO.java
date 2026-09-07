package com.example.springboot.dto;

import lombok.Data;

@Data
public class UserQueryDTO {

    private String username;

    private Integer role;

    private Integer status;

    private Integer offset;

    private Integer size;
}
