package com.example.springboot.service.impl;


import com.example.springboot.common.DataRequset.BaseRequest;
import com.example.springboot.entity.Comment;
import com.example.springboot.mapper.CommentMapper;
import com.example.springboot.service.CommentService;
import com.example.springboot.vo.PageVo;
import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class CommentServiceImpl implements CommentService {
    @Autowired
    CommentMapper commentMapper;

    @Override
    public List<Comment> list(){
        return commentMapper.list();
    }

    @Override
    public PageVo page(BaseRequest baseRequest) {
        PageHelper.startPage(baseRequest.getCurrent(), baseRequest.getSize());
        List<Comment> users = commentMapper.listByCondition(baseRequest);
        PageInfo<Comment> userPageInfo = new PageInfo<>(users);

        return new PageVo(userPageInfo);
    }



    @Override
    public Comment getById(Integer id) {
        return commentMapper.getById(id);
    }



    @Override
    public void deleteById(Integer id) {

        commentMapper.deleteById(id);

    }



    @Override
    public List<Comment> getByUserId(Integer userId) {
        return commentMapper.getByUserId(userId);
    }
    @Override
    public List<Comment> getCommentTree(Integer itemId) {
        List<Comment> commentList = commentMapper.getByAllId(itemId);
        if (commentList == null || commentList.isEmpty()) {
            return new ArrayList<>();
        }

        List<Comment> validComments = commentList.stream()
                .filter(comment -> comment != null && comment.getId() != null)
                .collect(Collectors.toList());

        Map<Long, Comment> commentMap = validComments.stream()
                .collect(Collectors.toMap(Comment::getId, comment -> comment));

        List<Comment> commentTree = new ArrayList<>();
        for (Comment comment : validComments) {
            Long parentId = comment.getParentId();
            if (parentId == null) {
                commentTree.add(comment);
            } else {
                Comment parentComment = commentMap.get(parentId);
                if (parentComment != null) {
                    if (parentComment.getReplies() == null) {
                        parentComment.setReplies(new ArrayList<>());
                    }
                    parentComment.getReplies().add(comment);
                }
            }
        }

        return commentTree;
    }

    @Override
    public void save(Comment obj) {


        commentMapper.save( obj);
    }

}
