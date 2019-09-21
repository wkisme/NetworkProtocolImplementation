import sys
import pymysql as sql
# 本文件 db.py 将由 s_main.py 导入


class Sql():
    def __init__(self, host, port, db, user, passwd, charset='utf8'):
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.passwd = passwd
        self.charset = charset

    def start(self):
        try:
            self.conn = sql.connect(
                host=self.host, port=self.port,
                db=self.db, user=self.user,
                passwd=self.passwd, charset=self.charset
            )
        except Exception:
            try:
                self.conn = sql.connect(
                    host=self.host, port=self.port,
                    user=self.user, passwd=self.passwd,
                    charset=self.charset
                )
                cmd = ("create database if not exists %s " % self.db +
                       "default charset utf8 collate utf8_general_ci;")
                cursor = sql.cursors.Cursor(self.conn)
                cursor.execute(cmd)
                self.conn.commit()
                cursor.execute("use %s;" % self.db)
            except Exception as err:
                print(err)
                print("无法创建数据库, 程序退出")
                sys.exit(1)

    def run(self, cmd):
        self.start()
        self.cursor = sql.cursors.Cursor(self.conn)
        try:
            self.cursor.execute(cmd)
            result = self.cursor.fetchall()
            if result:
                print(result)
            self.conn.commit()
            print("OK")  # 调试语句
        except Exception as exp:
            self.conn.rollback()
            print("SQLERROR: %s" % exp)
            result = None
        finally:
            self.cursor.close()
            self.conn.close()
            if result is not None:
                return result
            else:
                return False

    # 下面加入自定义业务
    # 用于插入表, id 主键, 用户名 unique, 密码 非空
    def create(self, table):
        try:
            cmd = ("create table if not exists %s" % table +
                   "(id int primary key auto_increment, " +
                   "user varchar(30) unique, " +
                   "passwd varchar(80) not null);")
            self.run(cmd)
            return True
        except Exception as err:
            print("SQLERROR: %s" % err)
            return False

    # 用于插入数据 到 用户密码清单(3 个字段)
    def insert(self, table, user, passwd):
        try:
            cmd = "insert into %s values(null, '%s', '%s');" %\
                (table, user, passwd)
            flag = self.run(cmd)
            if flag is not False:
                return True
            else:
                return False
        except Exception as err:
            print("SQLERROR: %s" % err)
            return False

    # 用于验证查找的数据是否存在
    def select(self, table, user, passwd):
        try:
            cmd = "select * from %s where user='%s' and passwd='%s'" %\
                (table, user, passwd)
            result = self.run(cmd)
            if len(result) == 1:
                return True
        except Exception as err:
            print("SQLERROR: %s" % err)
            return False
        return False


if __name__ == '__main__':
    info = ('localhost', 3306, 'pytest', 'root', '123456', 'utf8')
    cnt = Sql(*info)
    table = 'usrLst'
    user = ''
    passwd = ''
    cnt.create(table)
    if len(user) >= 6 and len(passwd) >= 6:
        # 如果 flag_0 is True, 可以注册账户, 否则 表示 用户名已存在 或 密码为空
        flag_0 = cnt.insert(table, user, passwd)
        print(flag_0)
        # 如果 flag_1 is True, 可以登入, 修改密码
        flag_1 = cnt.select(table, user, passwd)
        print(flag_1)
    else:
        print("用户名或密码长度少于6字符")
