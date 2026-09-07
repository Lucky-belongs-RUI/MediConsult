package com.example.springboot.service;


import com.example.springboot.common.DataRequset.BaseRequest;
import com.example.springboot.entity.Item;
import com.example.springboot.vo.ItemVO;
import com.example.springboot.vo.PageVo;

import java.util.List;

public interface ItemService {
    List<Item> list();
    PageVo page(BaseRequest baseRequest);

    void save(ItemVO obj);
    ItemVO getById(Integer id);
    Item getById2(Integer id);
    void update(ItemVO obj);
    void deleteById(Integer id);


    List<ItemVO> listCategoryId(Integer id);

}
