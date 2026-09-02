[app]

# 应用名称
title = 十二生肖注册

# 包名
package.name = zodiacregister
package.domain = com.example

# 版本
version = 1.0.0
version.code = 1

# 源码目录（必须）
source.dir = .

# 支持的架构
android.archs = arm64-v8a

# 依赖库
requirements = python3,kivy,requests

# 权限
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Android 版本
android.api = 30
android.minapi = 21

# 屏幕方向
orientation = portrait

# 全屏
fullscreen = 0

# 其他
android.gradle_dependencies =
android.enable_androidx = True
android.allow_backup = True

# 主文件
main.py = main.py

[buildozer]
log_level = 2
warn_on_root = 1
