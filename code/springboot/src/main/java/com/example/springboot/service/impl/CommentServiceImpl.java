package com.example.springboot.service.impl;


import com.example.springboot.common.DataRequset.CommentPageRequest;
import com.example.springboot.config.FileServiceConfig;
import com.example.springboot.entity.Comment;
import com.example.springboot.entity.User;
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

    @Autowired
    FileServiceConfig fileServiceConfig;

    /** 组装用户头像 URL（与 ItemServiceImpl.buildFileUrl 同规则） */
    private void fillAvatarUrl(User user) {
        if (user != null && user.getAvatarBucket() != null && !user.getAvatarBucket().isEmpty()
                && user.getAvatarObjectKey() != null && !user.getAvatarObjectKey().isEmpty()) {
            user.setAvatarUrl(fileServiceConfig.getUrl() + "/file/" + user.getAvatarBucket() + "/" + user.getAvatarObjectKey());
        }
    }

    /** 为评论及其回复填充 userInfo / replyToUserInfo 的头像 URL */
    private void fillCommentAvatarUrls(List<Comment> comments) {
        if (comments == null) {
            return;
        }
        for (Comment comment : comments) {
            fillAvatarUrl(comment.getUserInfo());
            fillAvatarUrl(comment.getReplyToUserInfo());
            if (comment.getReplies() != null) {
                for (Comment reply : comment.getReplies()) {
                    fillAvatarUrl(reply.getUserInfo());
                    fillAvatarUrl(reply.getReplyToUserInfo());
                }
            }
        }
    }

    @Override
    public List<Comment> list(){
        return commentMapper.list();
    }

    @Override
    public PageVo page(CommentPageRequest pageRequest) {
        PageHelper.startPage(pageRequest.getCurrent(), pageRequest.getSize());
        List<Comment> users = commentMapper.listByCondition(pageRequest);
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

        fillCommentAvatarUrls(commentTree);

        return commentTree;
    }

    @Override
    public void save(Comment obj) {


        commentMapper.save( obj);
    }

}
