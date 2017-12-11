### 本项目主要记录自己学习数据采集,数据维度分析,及数据可视化

##子项目1  拉勾网,深圳 职位分析

暂定须采集信息如下:
1.岗位名称
2.岗位薪资
3.岗位描述
4.岗位要求
5.公司名称
6.公司规模
7.学历要求
8.经验要求
9.岗位url


allCategory.py 获取所有岗位分类，对分类名及url链接进行入库

职位分类表结构

CREATE TABLE jobCategories
(
category_name varchar(100),
category_url varchar(500)
)

