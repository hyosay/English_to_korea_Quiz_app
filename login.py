import pymysql
import numpy as np

#mysql 접속
conn = pymysql.connect(
    user='root',
    passwd='0000',
    host= 'localhost',
    charset='utf8'
)

#커서 생성
cursor = conn.cursor()

#db 생성
# create schema
def mk_user():
    insert_user = input()
    cursor.execute("SHOW DATABASES")
    rows = cursor.fetchall()
    cursor.execute("CREATE SCHEMA '{}'".format(input()))



login_key = input('이름을 입력해주세요. : ')


cursor.execute("show databases")
rows = cursor.fetchall()

print (type(np.array(rows).flatten().tolist()))




'''for i in range(len(rows)):
    if rows[i][0] == login_key:
        print('로그인 정보가 확인 되었습니다.')
        cursor.execute('use {}'.format(login_key))
        print(cursor.fetchall())

        break
    else:
        print('로그인 정보가 일치하지 않습니다.')
        print('아이디를 다시 입력해주세요.')

'''

conn.commit()
conn.close()


