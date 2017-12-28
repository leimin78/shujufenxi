## 数据看芳华

## 数据收集来自豆瓣影评

#创建数据库
CREATE DATABASE IF NOT EXISTS fanghua default charset utf8 COLLATE utf8_general_ci;

用户昵称,星级,评论时间,有用数,评论内容

create table fanghua
(
    user_name varchar(100),
    film_star int,
    film_comment_time varchar(100),
    comment_agree int,
    comment_content varchar(1000)
)

完成数据采集，可视化处理
