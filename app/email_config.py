#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/16 上午10:52
# @Author  : tudoudou
# @File    : email_config.py
# @Software: PyCharm

"""
    說明：
    username 填寫發送郵件的郵箱
    password 填寫郵箱的授權碼
    注意：此處應當開通QQ郵箱的IMAP/SMTP服務，如不明白請查看郵箱說明文檔。
"""

email_config = {
    'username': 'ctudoudou@foxmail.com',
    'password': 'xxxxxxxxxxxxxx',
    'contents': '您好！有用户在人间真情悬赏平台咨询您的二手商品/您的悬赏任务，请及时登录平台后处理。',
    'title': '人间真情悬赏平台邮件提醒',
    # 請不要修改以下內容，在不確定的情況下
    'servers': 'smtp.qq.com',
    'post': 465,
}
