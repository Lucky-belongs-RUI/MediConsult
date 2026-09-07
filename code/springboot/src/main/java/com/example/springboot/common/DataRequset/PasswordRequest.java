package com.example.springboot.common.DataRequset;





import lombok.Data;

@Data
public class PasswordRequest {
    private Integer id;
    private String oldPassword;
    private String newPassword;
}
