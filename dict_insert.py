import pymysql
import re

# 1.创建数据库连接对象
db = pymysql.connect(host="localhost",\
             user="root",password="123456",\
             database="project",charset="utf8")
cursor = db.cursor()
with open('dict.txt') as f:
    for s in f:
        try:
          data=re.match('(\w+)\s+(.+)',s)
          word=data.group(1)
          parse=data.group(2)
          sql_insert = "insert into dict values('%s','%s');"%(word,parse)
          cursor.execute(sql_insert)
          db.commit()
        except:
            db.rollback()
            continue


# 2.利用 db 创建游标对象
# # 3.利用cursor的execute()方法执行SQL命令
print("ok")
# 5.关闭游标对象
cursor.close()
# 6.断开数据库连接
db.close()
