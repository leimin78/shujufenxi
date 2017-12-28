### 本项目主要记录自己学习数据采集,数据维度分析,及数据可视化

##子项目1  拉勾网,深圳 职位分析


allCategory.py 获取所有岗位分类，对分类名及url链接进行入库

#职位分类表结构,分类名,分类URL

CREATE TABLE jobCategories
(
category_name varchar(100),
category_url varchar(500)
)

#公司属性表,公司ID,公司所在城市,所在区域,融资情况,行业,公司大小,公司标签,公司名
create table company_detail
(
    companyId int(100) not null unique,
    city varchar(100),
    district varchar(100),
    financeStage varchar(100),
    industryField varchar(100),
    companySize varchar(100),
    companyLabelList varchar(200),
    companyFullName varchar(100)
)

#职位属性表,职位id,职位名,工作年限,教育情况,职位所属公司id,薪资,公司福利,创建时间,职位标签,职位描述,职位所属分类

create table position_detail
(
    positionId int(100) not null unique,
    positionName varchar(100),
    workYear varchar(100),
    education varchar(100),
    companyId int(100),
    salary varchar(100),
    positionAdvantage varchar(100),
    createTime varchar(100),
    positionLables varchar(200),
    positionText varchar(1000),
    caregory
)

项目分析文章--http://www.jianshu.com/p/83dea1b4aa27
