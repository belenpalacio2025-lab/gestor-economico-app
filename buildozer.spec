[app]
title = Gestor Economico Digital
package.name = gestoreconomico
package.domain = org.proyecto
source.dir = .
source.include_exts = py,kv,png,jpg,atlas,db
version = 0.1.0
requirements = python3,kivy==2.3.1
orientation = portrait
fullscreen = 0

android.permissions =
android.api = 34
android.minapi = 23
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
