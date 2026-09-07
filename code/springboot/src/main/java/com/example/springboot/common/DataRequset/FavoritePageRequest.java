package com.example.springboot.common.DataRequset;


import lombok.Data;

@Data
public class FavoritePageRequest extends BaseRequest{
    private Long userId;
    private Long itemId;

}
