[app]
title = Yilan
package.name = yilan
package.domain = org.beraydin47
source.dir = .
source.include_exts = py
source.exclude_dirs = .github, bin
version = 1.0
requirements = python3==3.10.12,hostpython3==3.10.12,pygame
orientation = portrait
fullscreen = 1

android.api = 34
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
android.ndk = 25b

# p4a pygame recipe (2.1) Cython C dosyalari Python 3.11+ ile derlenmiyor
p4a.branch = v2024.01.21

[buildozer]
log_level = 2
warn_on_root = 1
