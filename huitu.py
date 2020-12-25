from matplotlib import pyplot as plt  # 绘图 数据可视化


def huitu():
    # 将绘画框进行对象化
    fig = plt.figure()

    # 设置图标头部标题大小
    # plt.title("不同薪资公司数量占比", fontsize=15)
    # 设置X轴标题及大小
    # plt.xlabel("salary", fontsize=10)
    # 设置y轴标题及大小
    # plt.ylabel("number", fontsize=10)
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
    p3.plot(x2, y2)

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