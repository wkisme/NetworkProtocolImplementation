#!/usr/bin/env python3
# coding=utf-8

import sys
import socket as soc
from db.db import Sql


def main():

    # 初始化服务器地址
    SELF_ADDR = ('0.0.0.0', 30080)
    BUFFERSIZE = 1024

    # 初始化 mysql 连接对象
    mysql_init = (
        'localhost', 3306, 'chatroom',
        'root', 'very_strong_password', 'utf8'
    )
    sql_obj = Sql(*mysql_init)
    # 创建数据表
    TABLE = 'tb_userlist'
    sql_obj.create(TABLE)

    # 初始化客户端用户列表及连接列表
    user_list = []
    client_list = []

    # 绑定 套接字 实例
    udpServer = soc.socket(soc.AF_INET, soc.SOCK_DGRAM)
    udpServer.bind(SELF_ADDR)

    # 服务器进入主循环
    while True:

        # 接收并处理信息
        try:
            buf, addr = udpServer.recvfrom(BUFFERSIZE)
            msg = buf.decode()
            print(msg)
            msgLst = msg.split('|')
        except KeyboardInterrupt:
            print('即将退出程序')
            sys.exit(0)
        except Exception as err:
            print(err)
        # 注意, '|'.join(msgLst[2:]) 表示之后的文字 in str

        # 处理群聊室发送
        if msgLst[0] == 'Send':
            for x in client_list:
                udpServer.sendto(buf, x)

        # 处理 客户端登入
        elif msgLst[0] == 'Login':

            # 检索 数据表
            flag_login = sql_obj.select(TABLE, msgLst[1], '|'.join(msgLst[2:]))
            # 如果密码正确(数据表有该Query)
            if flag_login is True:
                # 如果没有同名用户登入
                if msgLst[1] not in user_list:
                    udpServer.sendto(b'1', addr)
                else:
                    udpServer.sendto(b'2', addr)
                    continue
            else:
                udpServer.sendto(b'0', addr)
                continue

        # 确认客户端已进入聊天室后
        elif msgLst[0] == 'InRoom':
            user_list.append(msgLst[1])
            for x in client_list:
                udpServer.sendto(
                    ('Send|%s|%s 已进入聊天室' %
                        ('管理员:', msgLst[1])).encode(),
                    x)
            client_list.append(addr)
            print(client_list)

        # 处理客户端 注册
        elif msgLst[0] == 'Register':
            # 尝试插入数据表
            flag_reg = sql_obj.insert(TABLE, msgLst[1], '|'.join(msgLst[2:]))
            # 如果没有相同用户名
            if flag_reg is True and '管理员' not in msgLst[1]:
                udpServer.sendto(b'1', addr)
            else:
                udpServer.sendto(b'2', addr)
                print(user_list)
                continue

        # 处理客户端退出聊天室
        elif msgLst[0] == 'Quit':
            try:
                user_list.remove(msgLst[1])
                client_list.remove(addr)
            except Exception as err:
                print(err)
            for x in client_list:
                udpServer.sendto(
                    ('Send|%s|%s 已退出聊天室' %
                        ('管理员', msgLst[1])).encode(),
                    x
                )


if __name__ == "__main__":
    main()
