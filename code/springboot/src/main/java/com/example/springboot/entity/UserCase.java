package com.example.springboot.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.Data;

import java.util.Date;

/**
 * 个人病例（用户问诊记录）
 */
@Data
@TableName("user_case")
public class UserCase {
    @TableId(type = IdType.AUTO)
    private Integer id;
    /** 所属用户ID */
    private Integer userId;
    /** 公开后对应的病例库记录ID（item.id），未发布为空 */
    private Integer itemId;
    /** 问诊名称/病例标题 */
    private String title;
    /** 患者姓名 */
    private String patientName;
    /** 年龄 */
    private Integer age;
    /** 性别 */
    private String gender;
    /** 问诊科室ID */
    private Integer categoryId;
    /** 特殊情况备注 */
    private String remark;
    /** 问诊记录内容 */
    private String content;
    /** AI结构化摘要（模型按病例库格式输出的JSON） */
    private String aiSummary;
    /** 是否公开：0否 1是 */
    private Integer isPublic;
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss", timezone = "GMT+8")
    private Date createTime;
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss", timezone = "GMT+8")
    private Date updateTime;

    @TableField(exist = false)
    private String categoryName;
    @TableField(exist = false)
    private String userRealName;
}
