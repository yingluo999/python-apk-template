[app]

# 应用名称
title = 十二生肖注册

# 包名
package.name = zodiacregister
package.domain = com.qiqi

# 版本
version = 1.0.0
version.code = 1

# 源码目录
source.dir = .
source.include_exts = py,json,txt

# 主入口文件
main.py = main.py

# 依赖
requirements = python3,kivy,requests

# Android 配置
android.permissions = INTERNET
android.api = 30
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

# 屏幕方向
orientation = portrait
fullscreen = 0

# 关键：接受 SDK 许可证
android.accept_sdk_license = True
android.encoding = utf-8

[buildozer]
warn_on_root = 0
log_level = 2
