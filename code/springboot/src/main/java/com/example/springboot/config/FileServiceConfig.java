package com.example.springboot.config;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Data
@Component
@ConfigurationProperties(prefix = "file-service")
public class FileServiceConfig {
    private String url = "http://127.0.0.1:5000/api";
}
