import urllib.request
import re   # 正则表达式
import json # 处理51job数据
import xlwt # 写入Excel
import xlrd # 读取Excel
import sqlite3 # 数据库
from bs4 import BeautifulSoup  # 处理网页


# 主程序
def main():
    # url = "https://search.51job.com/list/010000,000000,0000,00,9,99,java,2,1.html?"
    url = "https://search.51job.com/list/010000,000000,0000,00,9,99,python,2,1.html?"
    # savepath = ".\\51jobJava.xlsx"
    savepath = ".\\51jobPython.xlsx"
    dbpath = "51job.db"
    # askHtml(url)
    # datalist = getData()
    # for i in range(len(datalist)):
    #     print(datalist[i])
    # saveExcel(datalist, savepath)
    # 初始化数据库
    # intiSqlit3(dbpath)
    # saveSqlit3(savepath,dbpath)
    saveSqlit3(savepath,dbpath)


# 数据请求
def askHtml(url):
    head = {
       "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"
        # "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    }
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        # print(response.getcode())
        # UnicodeDecodeError: 'gbk' codec can't decode byte 0xae in position 196: illegal multibyte sequence
        html = response.read().decode("gbk",'ignore')
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


# 解析数据
def getData():
    # 用于保存爬取的数据
    datalist = []
    k = 1
    for i in range(1, 21):
       # url = "https://search.51job.com/list/010000,000000,0000,00,9,99,java,2,"+str(i)+".html?"
        url = "https://search.51job.com/list/010000,000000,0000,00,9,99,python,2,"+str(i)+".html?"
        html = askHtml(url)
      # html = open('webList.html').readlines()
        data = re.findall("\"engine_search_result\":(.+?),\"jobid_count\"", str(html))
        jsonObj = json.loads(data[0])
        for item in jsonObj:
            # time.sleep(0.001)
            items = [item['job_href'].replace("\\", ""), item['job_name'].replace("\\", ""),item['providesalary_text'].replace("\\", ""),
                     item['companytype_text'], item['company_name'],
                     item['companysize_text'], item['attribute_text'][1].replace("\\", ""), item['companyind_text'].replace("\\", "")]
            datalist.append(items)
            print(items)
            print("正在获取第"+str(k)+"条....")
            k = k + 1
            # print(items[0])

    # 处理详情页的信息
    # print(len(datalist))
    for i in range(0,len(datalist)):
        result = datalist[i]
        #print(result[0])
        for j in range(0, 1):
            html = askHtml(result[0])
            # html = open('pageList.html', 'r')
            bs = BeautifulSoup(html, 'html.parser')
            #print(bs)
            findJob = re.compile(r'\d+[）.、]\w{9,}')

            finComp = re.compile(r'<div class="tmsg inbox">.*')
            for item in bs.find_all('div', class_="tCompany_center clearfix"):
                item = str(item)
                link = re.findall(findJob, item)
                if len(link) != 0:
                    result.append(link)
                else:
                    result.append(" ")
                # print(link)
                comp = re.findall(finComp, item)
                if len(comp) != 0:
                    result.append(str(comp).replace('<div cllass="tmsg inbox">', ""))
                else:
                    result.append(" ")
                #print(str(comp).replace('<div class="tmsg inbox">',""))
            print(datalist[i])
    print("爬取完毕")
    return datalist

# 保存数据到Excel
def saveExcel(datalist, savepath):
    print("保存中...")
    book = xlwt.Workbook(encoding='gbk', style_compression=0)  # 创建wookbook对象
    # sheet = book.add_sheet("北京-java", cell_overwrite_ok=True)  # 创建工作表
    sheet = book.add_sheet("北京-Python", cell_overwrite_ok=True)  # 创建工作表
    col = ("招聘链接", "岗位名称", "薪资", "公司类型", "公司名字", "人员情况", "学历", "所属领域", "职位信息", "公司信息")
    for i in range(0, 10):
        sheet.write(0, i, col[i])  # 列名
        print(len(datalist))
    for i in range(0, len(datalist)):
        print("第%d条正在保存..." % (i + 1))
        data = datalist[i]
        print(data)
        for j in range(0, len(data)):
            sheet.write(i + 1, j, data[j])
    book.save(savepath)
# 初始化数据库
def intiSqlit3(dbpath):
    # 连接数据库
    conn = sqlite3.connect(dbpath)
    # 创建一个游标
    cur = conn.cursor()

    # 创建javaBJ这张表
    # sql = '''
    #         create table javaBJ(
    #             id INTEGER primary key autoincrement ,
    #             job_href text ,
    #             job_name varchar ,
    #             providesalary_text varchar ,
    #             companytype_text varchar ,
    #             company_name varchar ,
    #             companysize_text varchar ,
    #             attribute_text varchar ,
    #             companyind_text varchar ,
    #             zhiweixinxi text ,
    #             company_text text 没必要
    #         )
    #     '''
    # 创建pythonBJ这张表
    sql = '''
            create table pythonBJ(
                id INTEGER primary key autoincrement ,
                job_href text ,
                job_name varchar ,
                providesalary_text varchar ,
                companytype_text varchar ,
                company_name varchar ,
                companysize_text varchar ,
                attribute_text varchar ,
                companyind_text varchar ,
                zhiweixinxi text 
            )
        '''
    # 执行sql语句
    cur.execute(sql)
    #提交
    conn.commit()
    cur.close()
    conn.close()


# 将excel表中的数据保存数据到Sqlite3
def saveSqlit3(savepath, dbpath):
    # 初始化数据库
    # intiSqlit3(dbpath)

    # 打开excel文件
    book = xlrd.open_workbook(savepath)
    # sheet = book.sheet_by_name("北京-java")
    sheet = book.sheet_by_name("北京-Python")
    # 读取标题行
    title = sheet.row_values(0,0)
    # 读取每一行每一列、
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    row_num = sheet.nrows
    col_num = sheet.ncols
    for i in range(1, row_num - 1):
        dataExcel = []
        for j in range(0, col_num - 1):
            str = '"' + sheet.cell_value(i, j) + '"'
            dataExcel.append(str)
           # print(str)
           #  dataExcel.append(sheet.cell_value(i, j) )
           # print(sheet.cell_value(i, col_num - 1))
        # print(sheet.cell_value(i, col_num - 1))
        # exit()

        # 将Java的数据保存在JaveBJ表中
        # sql = '''
        #     insert into javaBJ(job_href,job_name,providesalary_text,companytype_text,company_name,companysize_text,
        #     attribute_text,companyind_text,zhiweixinxi,company_text) values (%s)'''%",".join(dataExcel)

        # 将Python的数据保存在PythonBJ表中
        sql = '''
                    insert into pythonBJ(job_href,job_name,providesalary_text,companytype_text,company_name,companysize_text,
                    attribute_text,companyind_text,zhiweixinxi) values (%s)''' % ",".join(dataExcel)
        #print(sql.replace('[',"").replace(']',"") )
        sql = sql.replace('[',"").replace(']',"")
        print(sql)
        cur.execute(sql)
        conn.commit()
        #dataExcel.append(result)
    # 连接数据ku
    cur.close()
    conn.close()


# 程序启动入口
if __name__ == '__main__':
    main()
    print("数据分析处理完毕")


