[app]

# 应用名称
title = 十二生肖注册

# 包名
package.name = zodiacregister
package.domain = com.qiqi

# 源代码目录
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,txt,ttf

# 版本号
version = 1.0.0

# 依赖 (Kivy 是必须的)
requirements = python3,kivy,requests,urllib3,certifi,charset-normalizer,idna

# Android 配置
android.permissions = android.permission.INTERNET, android.permission.WRITE_EXTERNAL_STORAGE, android.permission.READ_EXTERNAL_STORAGE, android.permission.MANAGE_EXTERNAL_STORAGE, android.permission.READ_MEDIA_IMAGES, android.permission.READ_MEDIA_VIDEO, android.permission.READ_MEDIA_AUDIO
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

# 屏幕方向
orientation = portrait
fullscreen = 0

# Android 特定
android.accept_sdk_license = True
android.manifest.application.android:requestLegacyExternalStorage = true
android.release_artifact = apk

[buildozer]
log_level = 2
warn_on_root = 0
