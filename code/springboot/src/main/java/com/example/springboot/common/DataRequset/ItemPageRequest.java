package com.example.springboot.common.DataRequset;



import lombok.Data;

@Data
public class ItemPageRequest extends BaseRequest{
    private String title;
    private Long categoryId;
    private String userRealName;
    private String tag;


}
