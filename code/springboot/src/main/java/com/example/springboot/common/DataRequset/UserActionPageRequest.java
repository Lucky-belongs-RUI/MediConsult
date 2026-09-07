package com.example.springboot.common.DataRequset;



import lombok.Data;

@Data
public class UserActionPageRequest extends BaseRequest{
    private Integer actionType;
    private Long userId;
    private String username;
    private String itemTitle;

}
