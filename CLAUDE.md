# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个小型 Python 脚本集合，主要功能是红旗云自动签到。

## 运行方式

```bash
# 运行签到脚本
python checkin.py [username] [password]

# 其他简单脚本
python hello.py
python test.py
```

## 依赖

- `checkin.py` 需要 `requests` 库：`pip install requests`
- `hello.py` 和 `test.py` 无外部依赖

## 代码结构

- `checkin.py` - 红旗云自动签到脚本，支持 Cookie 持久化（存储在 `.cookies.json`），可通过命令行参数或交互式输入账号密码
- `hello.py` - 简单的 hello world 脚本
- `test.py` - 欢迎界面和乘法计算器