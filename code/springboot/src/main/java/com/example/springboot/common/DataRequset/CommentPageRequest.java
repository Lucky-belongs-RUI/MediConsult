package com.example.springboot.common.DataRequset;


import lombok.Data;

@Data
public class CommentPageRequest extends BaseRequest{
    private Integer itemId;
    private Integer userId;
    private boolean onlyParent;

}
