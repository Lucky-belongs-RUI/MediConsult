package com.example.springboot.mapper;


import com.example.springboot.common.DataRequset.BaseRequest;
import com.example.springboot.entity.Item;
import com.example.springboot.vo.ItemVO;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;


@Mapper
public  interface ItemMapper {
    List<Item> list();

    List<ItemVO>  listByCondition(BaseRequest baseRequest);

    void save(ItemVO user);

    ItemVO getById(Integer id);
    Item getById2(Integer id);

    void updateById(ItemVO user);

    void deleteById(Integer id);

    Item selectByname(@Param("name") String username);
    void deleteUserActionByItemId(Integer id);


    List<ItemVO> listCategoryId(Integer id);

}
