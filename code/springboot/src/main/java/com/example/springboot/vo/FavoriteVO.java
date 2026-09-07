package com.example.springboot.vo;

import com.example.springboot.entity.Item;
import lombok.Data;

import java.time.LocalDateTime;

@Data
public class FavoriteVO {
    private Long id;
    private Long userId;
    private Long itemId;
    private Item item;
    private LocalDateTime createTime;

}
