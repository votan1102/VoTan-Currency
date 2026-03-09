import os, sys, subprocess, re

SD = os.path.dirname(os.path.abspath(__file__))
BASE = "android/app/src/main/res"

# 1. Chạy 5 file icon theo DPI
for dpi in ["mdpi","hdpi","xhdpi","xxhdpi","xxxhdpi"]:
    r = subprocess.run([sys.executable, os.path.join(SD, f"icon_{dpi}.py")],
                       capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0:
        print("ERR:", r.stderr); sys.exit(1)

# 2. Adaptive icon XML (Android 8+)
adp = os.path.join(BASE, "mipmap-anydpi-v26")
os.makedirs(adp, exist_ok=True)
XML = ('<?xml version="1.0" encoding="utf-8"?>\n'
       '<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n'
       '    <background android:drawable="@color/ic_launcher_background"/>\n'
       '    <foreground android:drawable="@mipmap/ic_launcher_foreground"/>\n'
       '</adaptive-icon>')
open(os.path.join(adp, "ic_launcher.xml"), "w").write(XML)
open(os.path.join(adp, "ic_launcher_round.xml"), "w").write(XML)
print("OK adaptive XML")

# 3. Xóa file ic_launcher_background.xml riêng nếu có (Capacitor mới tạo file này)
#    Để tránh Duplicate resources với colors.xml
for vdir in ["values", "values-night", "values-v31"]:
    dup = os.path.join(BASE, vdir, "ic_launcher_background.xml")
    if os.path.exists(dup):
        os.remove(dup)
        print(f"REMOVED {vdir}/ic_launcher_background.xml")

# 4. Cập nhật màu trong colors.xml có sẵn
colors_file = os.path.join(BASE, "values", "colors.xml")
COLOR_ENTRY = '    <color name="ic_launcher_background">#050505</color>'
if os.path.exists(colors_file):
    content = open(colors_file).read()
    if "ic_launcher_background" not in content:
        content = content.replace("</resources>", COLOR_ENTRY + "\n</resources>")
        open(colors_file, "w").write(content)
        print("OK color added to colors.xml")
    else:
        content = re.sub(
            r'<color name="ic_launcher_background">[^<]*</color>',
            '<color name="ic_launcher_background">#050505</color>',
            content)
        open(colors_file, "w").write(content)
        print("OK color updated in colors.xml")
else:
    os.makedirs(os.path.dirname(colors_file), exist_ok=True)
    open(colors_file, "w").write(
        '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
        + COLOR_ENTRY + '\n</resources>')
    print("OK colors.xml created")

print("ALL ICONS DONE!")
