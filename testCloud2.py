import jieba #分词
from matplotlib import pyplot as plt # 绘图 数据可视化
from wordcloud import WordCloud # 词云
from PIL import Image # 图片处理
import numpy as np # 矩阵运算
import sqlite3 #连接数据库

def Wordcloud2():
    conn = sqlite3.connect('51job.db') # 单引号
    cur = conn.cursor()

    sql = "select zhiweixinxi from pythonBJ"
    datalist = cur.execute(sql)
    text = ""

    for item in datalist:
        text = text + item[0]
    #print(text)
    cur.close()
    conn.close()

    #进行分词，要转换为字符串
    cut = jieba.cut(text)
    string = ' '.join(cut)
    string = string.replace("的","")
    string = string.replace("和","")
    print(len(string))

    # 打开遮罩图片
    img = Image.open(r'.\static\assets\img\timg.jpg')
    # 将图片转换为数组
    img_arr = np.array(img)

    # 制作词云
    wc = WordCloud(
        background_color= "white",
        mask = img_arr,
        font_path="msyh.ttc"
    )
    wc.generate_from_text(string)

    # 绘制图片
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')


    # 保存词云
    plt.savefig(r'.\static\assets\img\wordColud2.jpg',dpi=500)

    # 打印词云
    print(plt.show())


