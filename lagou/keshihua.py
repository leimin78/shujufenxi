from flask import Flask,render_template
from dbHandle import dbHandle

app = Flask(__name__)

#查询行业及行业职位数sql
category_count_sql = "select category,count(category) from position_detail group by category order by count(category) desc"

#查询工作年限
work_year_sql = "select workYear,count(workYear) from position_detail group by workYear order by count(workYear) desc"

#查询工作学历要求
education_sql = "select education,count(education) from position_detail group by education order by count(education) desc"


#小于5ksql
less_5_sql = "select workYear,count(*) from position_detail_bak where salary<5 group by workYear"

#5-10 sql
less_10_sql = "select workYear,count(*) from position_detail_bak where salary>5 and salary<10 group by workYear"

#10-15 sql
less_15_sql = "select workYear,count(*) from position_detail_bak where salary>10 and salary<15 group by workYear"

#15-25 sql
less_25_sql = "select workYear,count(*) from position_detail_bak where salary>15 and salary<25 group by workYear"

#25-40 sql
less_40_sql = "select workYear,count(*) from position_detail_bak where salary>25 and salary<40 group by workYear"

#40+ sql
more_40_sql = "select workYear,count(*) from position_detail_bak where salary>40 group by workYear"


#查询工资分布

salary_sql = "select salary,workYear,count(salary) from position_detail group by salary,workYear"
@app.route('/')
def index():
    db = dbHandle()
    datas = db.query_db(category_count_sql)
    print(datas)
    return render_template('data.html',datas=datas[:50])

@app.route('/workyear')
def year():
    db = dbHandle()
    datas = db.query_db(work_year_sql)
    print(datas)
    return render_template('education.html', datas=datas)

@app.route('/education')
def education():
    db = dbHandle()
    datas = db.query_db(education_sql)
    print(datas)
    return render_template('workyear.html', datas=datas)

@app.route('/salary')
def salary():
    db = dbHandle()



    #工资区间划分
    #0-5,5-10,10-15,15-25,25-40,40+
    less_5 = db.query_db(less_5_sql)
    less_10 = db.query_db(less_10_sql)
    less_15 = db.query_db(less_15_sql)
    less_25 = db.query_db(less_25_sql)
    less_40 = db.query_db(less_40_sql)
    more_40 = db.query_db(more_40_sql)

    print("less 5:{0}".format(less_5))
    print("less 10:{0}".format(less_10))
    print("less 15:{0}".format(less_15))
    print("less 25:{0}".format(less_25))
    print("less 40:{0}".format(less_40))
    print("more 40:{0}".format(more_40))



    # new_list = []
    # for data in datas:
    #     newdata = data[0].split('-')
    #     if len(newdata)>1:
    #         total = int(newdata[0].strip('K').strip('k'))+int(newdata[1].strip('K').strip('k'))
    #         avg = total/2
    #         new = (avg,data[1],data[2])
    #         new_sql = "update position_detail_bak set salary={0} where salary='{1}';".format(avg,data[0])
    #         print(new_sql)
    #         #print(new)
    #         new_list.append(new)
    #
    # print(new_list)
    # key_lis = ['1-3年','3-5年','不限','5-10年','1年以下','10年以上','应届毕业生']


    return render_template('salary.html')

if __name__ == '__main__':
    app.run()