# -*- encoding:utf-8 -*-

import matplotlib
matplotlib.use('TkAgg')
import jieba
from jieba import analyse
from PIL import Image, ImageSequence
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
from dbHandle import dbHandle


def getContent(table_name):
    db = dbHandle()
    jieba.del_word("电影")
    jieba.del_word("导演")
    jieba.del_word("没有")
    jieba.del_word("影片")
    jieba.del_word("看到")
    query_sql = "select comment_content from {0}".format(table_name)
    texts = db.query_db(query_sql)
    text = ''
    for t in texts:
        text += t[0]
    #result = jieba.analyse.textrank(text, topK=1000, withWeight=True)
    result = jieba.cut(text,cut_all=True)
    wl_space_split = " ".join(result)
    return wl_space_split

def getwordCloud(abs_filename,keywords):
    image = Image.open(abs_filename)
    graph = np.array(image)
    wc = WordCloud(font_path='/Users/leimin/spiderCrawl/shuju/shujufenxi/fanghua/simhei.ttf',background_color='white', max_words=1000, mask=graph)
    wc.generate(keywords)
    image_color = ImageColorGenerator(graph)

    # 显示图片
    plt.imshow(wc)
    plt.imshow(wc.recolor(color_func=image_color))
    plt.axis("off")  # 关闭图像坐标系
    plt.show()

if __name__ == '__main__':
    keywords = getContent("fanghua")
    fanghua_path = '/Users/leimin/spiderCrawl/shuju/shujufenxi/fanghua/fanghua.jpg'
    getwordCloud(fanghua_path,keywords)

