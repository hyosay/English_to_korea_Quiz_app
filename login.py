import pymysql
import numpy as np
import pandas as pd

#localhost mysql 접속
conn = pymysql.connect(
    user='root',
    passwd='0000',
    host= 'localhost',
    charset='utf8'
)
# pandas를 통해 데이터를 시각화
# numpy를 통해서 데이터를 전제
# 변수 설명
'''회원가입 변수
user_rows: root에 있는 '''


#커서 생성
cursor = conn.cursor()
def sign_up():
    #user 만들기 회원가입
    #회원가입 스키마까지 생성
    cursor.execute('use mysql')
    cursor.execute('select user from user')
    user_rows = cursor.fetchall()
    user_rows = np.array(user_rows).flatten().tolist()
    print(user_rows)
    count = 5
    while count:
        create_name = input('이름을 입력해주세요. : ')
        create_id = input('사용할 아이디를 입력해주세요. : ')
        if create_id in user_rows:
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
                    # mysql에 유저 아이디, 비밀번호 등록
                    cursor.execute("use mysql")
                    cursor.execute("create user {0}@localhost identified by '{1}'".format(create_id, create_passwd))
                    # 아이디와 동일한 DB생성 및 본인 DB에 대한 권한부여
                    cursor.execute("create schema {}".format(create_id))
                    cursor.execute("grant all privileges on {0}.* to {1}@localhost".format(create_id, create_id))
                    # 운영자 mysql에 유저 정보입력
                    cursor.execute("use user_info")
                    cursor.execute("INSERT INTO user_info (id, name, passwd) VALUES (\'{0}\', \'{1}\', \'{2}\')".format(create_id, create_name, create_passwd))

                    # 본인 이름의 DB에 단어장 생성
                    cursor.execute('use {0}'.format(create_id))
                    table = '''CREATE TABLE word (
                    영어 VARCHAR(30) NOT NULL,
                    한국어 VARCHAR(30) NOT NULL
                    )'''
                    cursor.execute(table)
                    # 저장
                    cursor.execute("flush privileges")
                    count = 0
                    break
                else:
                    if passwd_count == 5:
                        print('회원가입을 처음부터 다시 진행해주십시요.')
                        count = 0
                    else:
                        print('비밀번호 조건에 일치하지 않습니다. 사용할 비밀버호를 다시 입력해주세요.({}/5)'.format(passwd_count))


def login():
    #user mysql 접속
    id = input('아이디를 입력해주세요 : ')
    passwd = input('비밀번호를 입력해주세요 : ')

    #1차보안
    cursor.execute('use mysql')
    cursor.execute('SELECT user FROM user')
    user_rows = np.array(cursor.fetchall()).flatten().tolist()

    cursor.execute('use user_info')
    cursor.execute('SELECT id, passwd from user_info')
    user_info_rows = cursor.fetchall()


    #접속
    if (id, passwd) in user_info_rows and id in user_rows:
        print('로그인이 확인 되었습니다.')

        user = pymysql.connect(
                user='{}'.format(id),
                passwd='{}'.format(passwd),
                host= 'localhost',
                charset='utf8',
                db= '{}'.format(id)
            )
        user_cursor = user.cursor()


        # 데이터 삽입하기
        while 1:
            print('옵션을 선택해주세요. 1. 단어장 확인 \t 2. 데이터 추가하기, 3. 종료')
            k = int(input())
            if k == 1:
                user_cursor.execute('select * from word')
                word_list = user_cursor.fetchall()
                word_eng = np.array(word_list).flatten().tolist()[0::2]
                word_kor = np.array(word_list).flatten().tolist()[1::2]

                result = pd.DataFrame({'eng': word_eng,
                                       'kor': word_kor})
                print(result)


            elif k == 2:
                eng = input('영어를 입력하세요 : ')
                kor = input('한글을 입력하세요 : ')
                user_cursor.execute('INSERT INTO word (영어, 한국어) VALUES (\'{0}\', \'{1}\')'.format(eng, kor))

            elif k == 3:
                print('프로그램을 종료합니다.')
                user.commit()
                user.close()
                break
    else:
        print('no')



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
'''def login():
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
'''


login()
conn.commit()


conn.close()


