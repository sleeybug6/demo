#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
红旗云自动签到脚本
"""

import requests
import json
import os
from pathlib import Path


class HongqiyeCheckin:
    def __init__(self):
        self.base_url = "https://ai.juguang.chat/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Content-Type': 'application/json',
            'Origin': self.base_url,
            'Referer': f'{self.base_url}/',
        })

        # Cookie 存储路径
        self.cookie_file = Path(__file__).parent / '.cookies.json'

    def load_cookies(self):
        """从文件加载 cookies"""
        if self.cookie_file.exists():
            with open(self.cookie_file, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
                for name, value in cookies.items():
                    self.session.cookies.set(name, value)
                return True
        return False

    def save_cookies(self):
        """保存 cookies 到文件"""
        cookies = {cookie.name: cookie.value for cookie in self.session.cookies}
        with open(self.cookie_file, 'w', encoding='utf-8') as f:
            json.dump(cookies, f, indent=2, ensure_ascii=False)

    def login(self, username: str, password: str) -> bool:
        """
        登录 - 需要根据实际 API 修改
        """
        login_url = f"{self.base_url}/login"  # TODO: 修改为实际的登录 API

        payload = {
            # TODO: 根据实际登录接口修改参数
            "username": username,
            "password": password,
        }

        try:
            response = self.session.post(login_url, json=payload)
            response.raise_for_status()
            result = response.json()

            # TODO: 根据实际返回结果判断登录是否成功
            if result.get('code') == 200 or result.get('success'):
                print("✓ 登录成功")
                self.save_cookies()
                return True
            else:
                print(f"✗ 登录失败: {result}")
                return False

        except Exception as e:
            print(f"✗ 登录异常: {e}")
            return False

    def checkin(self) -> bool:
        """
        签到 - 需要根据实际 API 修改
        """
        checkin_url = f"{self.base_url}/api/checkin"  # TODO: 修改为实际的签到 API

        try:
            response = self.session.post(checkin_url)
            response.raise_for_status()
            result = response.json()

            # TODO: 根据实际返回结果判断签到是否成功
            if result.get('code') == 200 or result.get('success'):
                print(f"✓ 签到成功: {result.get('message', '已完成')}")
                return True
            else:
                print(f"签到结果: {result}")
                return result.get('already_checked_in', False)

        except Exception as e:
            print(f"✗ 签到异常: {e}")
            return False

    def run(self, username: str = None, password: str = None):
        """执行签到流程"""
        # 尝试加载已保存的 cookies
        has_cookies = self.load_cookies()

        if has_cookies:
            print("→ 使用已保存的会话")
            # 直接尝试签到
            result = self.checkin()
            if result:
                return
            print("会话可能已过期，尝试重新登录...")

        # 需要登录
        if not username or not password:
            username = input("请输入用户名: ").strip()
            password = input("请输入密码: ").strip()

        if self.login(username, password):
            self.checkin()


def main():
    bot = HongqiyeCheckin()

    # 可以通过环境变量或命令行参数传入账号密码
    import sys
    username = sys.argv[1] if len(sys.argv) > 1 else None
    password = sys.argv[2] if len(sys.argv) > 2 else None

    bot.run(username, password)


if __name__ == "__main__":
    main()
