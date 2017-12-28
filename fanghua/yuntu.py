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
    query_sql = "select comment_content from {0}".format(table_name)
    texts = db.query_db(query_sql)
    text = ''
    for t in texts:
        text += t[0]
    result = analyse.textrank(text, topK=1000, withWeight=True)
    keywords = dict()
    for i in result:
        keywords[i[0]] = i[1]
    print(keywords)
    return keywords

def getwordCloud(abs_filename,keywords):
    image = Image.open(abs_filename)
    graph = np.array(image)
    wc = WordCloud(font_path='/Users/leimin/spiderCrawl/shuju/shujufenxi/fanghua/simhei.ttf',background_color='white', max_words=1000, mask=graph)
    wc.generate_from_frequencies(keywords)
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

