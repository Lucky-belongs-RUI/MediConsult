package com.example.springboot.service;


import com.example.springboot.common.DataRequset.BaseRequest;
import com.example.springboot.entity.Comment;
import com.example.springboot.vo.PageVo;

import java.util.List;

public interface CommentService {
    List<Comment> list();
    PageVo page(BaseRequest baseRequest);

    void save(Comment obj);

    Comment getById(Integer id);


    void deleteById(Integer id);

    


    List<Comment> getByUserId(Integer userId);

    List<Comment> getCommentTree(Integer itemId);

}
