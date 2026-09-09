package com.example.springboot.mapper;


import com.example.springboot.common.DataRequset.CommentPageRequest;
import com.example.springboot.entity.Comment;
import org.apache.ibatis.annotations.Mapper;

import java.util.List;


@Mapper
public  interface CommentMapper {
    List<Comment> list();

    List<Comment>  listByCondition(CommentPageRequest pageRequest);

    void save(Comment user);

    Comment getById(Integer id);

    void deleteById(Integer id);


    List<Comment> getByUserId(Integer userId);

    List<Comment> getByAllId(Integer itemId);
}
