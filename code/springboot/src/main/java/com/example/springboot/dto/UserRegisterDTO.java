package com.example.springboot.dto;

import lombok.Data;

@Data
public class UserRegisterDTO {

    private String username;


    private String password;

    private String realName;

    private String phone;

    private String email;
}
