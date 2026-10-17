[app]
title = Yilan
package.name = yilan
package.domain = org.beraydin47
source.dir = .
source.include_exts = py
source.exclude_dirs = .github, bin
version = 1.0
requirements = python3,pygame
orientation = portrait
fullscreen = 1

android.api = 34
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
android.ndk = 25b

# pygame recipe, p4a develop dalindaki Python 3.14 ile derlenmiyor
p4a.branch = v2024.01.21

[buildozer]
log_level = 2
warn_on_root = 1
