package com.example.springboot.common.DataRequset;

import lombok.Data;

@Data
public class BaseRequest {
    private int size=10;
    private int current=1;
}
