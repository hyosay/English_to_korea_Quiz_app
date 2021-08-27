import pymysql
import numpy as np

#localhost mysql 접속
conn = pymysql.connect(
    user='root',
    passwd='0000',
    host= 'localhost',
    charset='utf8'
)

#커서 생성
cursor = conn.cursor()
#user 만들기 회원가입
#회원가입 스키마까지 생성
cursor.execute('use mysql')
cursor.execute('select user from user')
user_rows = cursor.fetchall()
user_rows = np.array(user_rows).flatten().tolist()
print(user_rows)
count = 5
while count:
    create_user = input('사용할 아이디를 입력해주세요. : ')
    if create_user in user_rows:
        print('이미 존재하는 아이디 입니다.',end= ' ')
        if count == 1:
            print('회원가입을 처음부터 다시 진행해주십시요.')
            break
        else:
            print('아이디를 다시 입력해주세요({}/5)'.format(6 - count))
            count -= 1
    else:
        for passwd_count in range(1, 6):
            create_passwd = input('사용할 비밀번호를 입력해주세요.(영문숫자포함8자리)')
            if create_passwd.isalnum() and len(create_passwd) >= 8:
                print('아이디가 생성되었습니다.')
                cursor.execute("use mysql")
                cursor.execute("create user {0}@localhost identified by '{1}'".format(create_user, create_passwd))
                cursor.execute("create schema {}".format(create_user))
                cursor.execute("grant all privileges on {0}.* to {1}@localhost".format(create_user, create_user))
                cursor.execute("flush privileges")
                count = 0
                break
            else:
                if passwd_count == 5:
                    print('회원가입을 처음부터 다시 진행해주십시요.')
                    count = 0
                else:
                    print('비밀번호 조건에 일치하지 않습니다. 사용할 비밀버호를 다시 입력해주세요.({}/5)'.format(passwd_count))







'''
#user mysql 접속
_user = input('아이디를 입력해주세요 : ')
passwd = input('비밀번호를 입력해주세요 : ')
print(_user)
user = pymysql.connect(
    user='{}'.format(_user),
    passwd='{}'.format(passwd),
    host= 'localhost',
    charset='utf8'
)
user_cursor = user.cursor()

cursor.execute('use mysql')
cursor.execute('SELECT host, user FROM user')
user_rows = cursor.fetchall()

for i, j in user_rows:
    if j == _user:
        print('확인')
        
        user_cursor.execute('USE {}'.format(_user))
user_cursor.execute('show databases;')
rows = user_cursor.fetchall()

print(rows)'''







# create schema
def mk_user():
    insert_user = input("사용할 아이디를 입력하세요.")
    cursor.execute("SHOW DATABASES")
    rows = cursor.fetchall()
    rows = np.array(rows).flatten().tolist()
    if insert_user in rows:
        print('중복된 사용자가 있습니다.')
    else:
        cursor.execute("CREATE SCHEMA '{}'".format(input()))
        print('아이디가 생성되었습니다.')


login_count = 0

#변경예정
def login():
    global login_count

    login_key = input('이름을 입력해주세요. : ')

    cursor.execute("show databases;")
    rows = cursor.fetchall()
    rows = np.array(rows).flatten().tolist()


    if login_key in rows:
        print('로그인 정보가 확인 되었습니다.')
        cursor.execute('use {}'.format(login_key))
        cursor.execute('show tables;')
    elif login_key == 'stop':
        return print('out')
    else:
        print('로그인 정보가 인치하지 않습니다.')
        print('아이디를 다시 입력해주세요')
        print('틀린 횟수: {}'.format(login_count))
        login_count += 1
        if login_count > 5:
            print('보안을 위해 종료합니다.')
            return print('안녕히계세요')
        return login()


conn.commit()

'''user.commit()


user.close()'''
conn.close()

