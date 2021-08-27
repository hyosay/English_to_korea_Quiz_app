import pymysql
conn = pymysql.connect(
    user='root',
    passwd='0000',
    host= 'localhost',
    charset='utf8'
)


cursor = conn.cursor()


conn.commit()
conn.close()

