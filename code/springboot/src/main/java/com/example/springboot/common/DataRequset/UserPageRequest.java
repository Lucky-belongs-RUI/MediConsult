package com.example.springboot.common.DataRequset;


import lombok.Data;

@Data
public class UserPageRequest extends BaseRequest{
    private String username;
    private String realName;
    private Integer role;
    private Integer status;

}
