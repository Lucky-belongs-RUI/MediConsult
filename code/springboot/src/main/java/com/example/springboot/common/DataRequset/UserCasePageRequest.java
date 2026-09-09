package com.example.springboot.common.DataRequset;


import lombok.Data;

@Data
public class UserCasePageRequest extends BaseRequest{
    /** 用户ID（我的病例） */
    private Integer userId;
    /** 是否公开：null 全部，0 私有，1 公开 */
    private Integer isPublic;
    private String title;
    private Integer categoryId;
}
