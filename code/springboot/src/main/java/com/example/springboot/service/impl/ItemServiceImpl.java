package com.example.springboot.service.impl;


import com.example.springboot.common.DataRequset.BaseRequest;
import com.example.springboot.config.FileServiceConfig;
import com.example.springboot.entity.Item;
import com.example.springboot.mapper.ItemMapper;
import com.example.springboot.service.ItemService;
import com.example.springboot.vo.ItemVO;
import com.example.springboot.vo.PageVo;
import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;


@Service
public class ItemServiceImpl implements ItemService {
    @Autowired
    ItemMapper itemMapper;

    @Autowired
    FileServiceConfig fileServiceConfig;

    private String buildFileUrl(String bucket, String objectKey) {
        if (bucket == null || bucket.isEmpty() || objectKey == null || objectKey.isEmpty()) {
            return null;
        }
        return fileServiceConfig.getUrl() + "/file/" + bucket + "/" + objectKey;
    }

    @Override
    public List<Item> list(){
        return itemMapper.list();
    }

    @Override
    public PageVo page(BaseRequest baseRequest) {
        PageHelper.startPage(baseRequest.getCurrent(), baseRequest.getSize());
        List<ItemVO> users = itemMapper.listByCondition(baseRequest);
        users.forEach(item -> {
            item.setCoverUrl(buildFileUrl(item.getCoverBucket(), item.getCoverObjectKey()));
            item.setFileUrl(buildFileUrl(item.getFileBucket(), item.getFileObjectKey()));
            if (item.getCategory() != null) {
                item.getCategory().setIconUrl(
                    buildFileUrl(item.getCategory().getIconBucket(), item.getCategory().getIconObjectKey())
                );
            }
        });
        PageInfo<ItemVO> userPageInfo = new PageInfo(users);
        return new PageVo(userPageInfo);
    }

    @Override
    public ItemVO getById(Integer id) {
        ItemVO item = itemMapper.getById(id);
        if (item != null) {
            item.setCoverUrl(buildFileUrl(item.getCoverBucket(), item.getCoverObjectKey()));
            item.setFileUrl(buildFileUrl(item.getFileBucket(), item.getFileObjectKey()));
            if (item.getCategory() != null) {
                item.getCategory().setIconUrl(
                    buildFileUrl(item.getCategory().getIconBucket(), item.getCategory().getIconObjectKey())
                );
            }
        }
        return item;
    }

    @Override
    public Item getById2(Integer id) {
        return itemMapper.getById2(id);
    }

    @Override
    public void update(ItemVO obj) {
        itemMapper.updateById(obj);

    }

    @Override
    public void deleteById(Integer id) {
        itemMapper.deleteUserActionByItemId(id);
        itemMapper.deleteById(id);

    }

    @Override
    public List<ItemVO> listCategoryId(Integer id) {
        List<ItemVO> items = itemMapper.listCategoryId(id);
        items.forEach(item -> {
            item.setCoverUrl(buildFileUrl(item.getCoverBucket(), item.getCoverObjectKey()));
            item.setFileUrl(buildFileUrl(item.getFileBucket(), item.getFileObjectKey()));
            if (item.getCategory() != null) {
                item.getCategory().setIconUrl(
                    buildFileUrl(item.getCategory().getIconBucket(), item.getCategory().getIconObjectKey())
                );
            }
        });
        return items;
    }


    @Override
    public void save(ItemVO obj) {

        itemMapper.save( obj);
    }

}
