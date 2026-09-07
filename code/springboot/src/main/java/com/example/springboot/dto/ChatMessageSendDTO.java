package com.example.springboot.dto;

import lombok.Data;



@Data
public class ChatMessageSendDTO {

    private Long sessionId;


    private String content;


    private String model;

    private String extraData;
}
