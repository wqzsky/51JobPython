from flask import Flask, render_template, request
import sqlite3  # 数据库
import json
import testCloud
import testCloud2
from matplotlib import pyplot as plt  # 绘图 数据可视化

app = Flask(__name__)


# “主页”方法
@app.route('/')
def index():
    # 连接数据库
    con = sqlite3.connect("51job.db")

    # 创建游标
    cur = con.cursor()

    # 查询数据总数并赋给sql
    sql = "select count(*) from javaBJ"

    # 将游标中的数据取出
    data = cur.execute(sql)

    # 关闭数据库，撤销游标
    cur.close()
    con.close()
    return render_template("index.html", num=data)


# 主页/index路径
@app.route('/index')
def home():
    return render_template("index.html")


# “职位”方法
@app.route('/position', methods=["GET"])
def position():
    # 调用request方法
    page = request.values.get('page', 1)

    # 创建javalist列表和pylist列表存放查询到的数据，连接数据库
    javalist = []
    pylist = []
    con = sqlite3.connect("51job.db")

    # 创建cur和cur1游标操作数据库
    cur = con.cursor()
    cur1 = con.cursor()

    # 查询python和java中的所有数据并按二十分配
    sql1 = "select * from pythonBJ limit %s,20" % ((int(page) - 1) * 20)
    sql = "select * from javaBJ limit %s,20" % ((int(page) - 1) * 20)
    data = cur.execute(sql)
    data1 = cur1.execute(sql1)

    # 分别将查询的数据赋给定义的两个列表
    for item in data:
        javalist.append(item)
    for item1 in data1:
        pylist.append(item1)
    cur.close()
    cur1.close()
    con.close()

    # 将存放数据列表传值给可视化页面
    return render_template("position.html", javalist=javalist, pylist=pylist, page=int(page))


# “分析”方法
@app.route('/analyze')
def analyze():

    # 将绘画框进行对象化
    fig = plt.figure()

    # 设置图标头部标题大小
    plt.title("", fontsize=15)
    # 设置X轴标题及大小
    plt.xlabel("薪资", fontsize=10)
    # 设置y轴标题及大小
    plt.ylabel("数量", fontsize=10)
    # 将p1定义为绘画框的子图，211表示将会话框划分为2行一列，最后的1表示第一幅图
    p1 = fig.add_subplot(211)

    # 将p3定义为绘画框的子图，与p1覆盖
    p3 = fig.add_subplot(211)

    # 分别定义x与y轴
    x = ['0-5k', '5k-10k', '10k-15k', '15k-20k', '20k-25k', '25k-30k', '30k+']
    y = [0.06, 0.28, 0.24, 0.22, 0.12, 0.03, 0.08]
    x2 = ['0-5k', '5k-10k', '10k-15k', '15k-20k', '20k-25k', '25k-30k', '30k+']
    y2 = [0.07, 0.24, 0.23, 0.21, 0.12, 0.05, 0.15]

    # 调用库中.plot绘制折线图
    p1.plot(x, y)
    p3.plot(x2,y2)

    # 将p2定义为绘画框的子图，212表示将会话框划分为2行2列，最后的2表示第二幅图
    p2 = fig.add_subplot(212)
    a = ['0-5k', '5k-10k', '10k-15k', '15k-20k', '20k-25k', '25k-30k', '30k+']
    b = [0.07, 0.24, 0.23, 0.21, 0.12, 0.05, 0.15]

    # 调用库中.scatter绘制散点图
    p2.scatter(a, b)

    # 保存绘制的图形
    plt.savefig(r'.\static\assets\img\zhexian.jpg', dpi=500)

    # 打印绘制图形
    print(plt.show())

    # 定义公司类型、Java数量、python数量列表
    comtypelist = []
    countnum = []
    pynum = []

    # 连接数据库，从而创建游标
    con = sqlite3.connect("51job.db")
    cur = con.cursor()
    cur1 = con.cursor()

    # 编写sql语句查询公司类型及相关数量
    sql = "select companytype_text,count(companytype_text) from javaBJ group by companytype_text order by count(companytype_text)"
    sql1 = "select companytype_text,count(companytype_text) from pythonBJ group by companytype_text order by count(companytype_text)"
    data = cur.execute(sql)
    data1 = cur1.execute(sql1)

    # 分别将查询的语句赋给列表并关闭数据库及游标
    for item in data:
        comtypelist.append(str(item[0]))
        countnum.append(item[1])
    for item2 in data1:
        pynum.append(item2[1])
    cur.close()
    cur1.close()
    con.close()

    return render_template("analyze.html", comtypelist=comtypelist, countnum=countnum, pynum=pynum)


# “词云”方法
@app.route('/word_cloud')
def word_cloud():
    testCloud.Wordcloud()
    testCloud2.Wordcloud2()
    return render_template("word_cloud.html")

# “成员”方法
@app.route('/member')
def member():
    # 将 member.html，返回给前端请求页面
    return render_template("member.html")


@app.route('/keyWords', methods=["GET","POST"])
def keyWords():
    keyWord = request.values.get('word')
    if keyWord == "":
        keyWord = 11111;
    datalist = []
    conn = sqlite3.connect("51job.db")
    cur = conn.cursor()
    sql = "select * from TotalBJ where company_name like '%%%s%%'"%keyWord
    print(sql)
    data = cur.execute(sql)
    for item in data:
        datalist.append(item)
    cur.close()
    conn.close()
    print(json.dumps(datalist))
    return json.dumps(datalist)


# 主方法
if __name__ == '__main__':
    app.run(debug=True)
