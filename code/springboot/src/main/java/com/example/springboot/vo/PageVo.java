package com.example.springboot.vo;

import com.github.pagehelper.PageInfo;
import lombok.Data;

import java.util.List;
@Data
public class PageVo {
        private List records;
        private long total;
        private int size;
        private int current;
        private int pages;

        public PageVo(PageInfo pageInfo) {
            this.records = pageInfo.getList();
            this.total = pageInfo.getTotal();
            this.size = pageInfo.getPageSize();
            this.current = pageInfo.getPageNum();
            this.pages = pageInfo.getPages();
        }


}
