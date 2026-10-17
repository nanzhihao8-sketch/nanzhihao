#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""雷霆DeepSeek微信自动回复脚本 · 防消息重复发送补丁

【解决什么问题】
底层库 wechatauto 判断"消息是否发出"时，会截取输入框区域、数深色像素。
鼠标指针是深色的，停在输入框上会被误判成"文字还没发出去"，库于是重试，
结果同一条消息被重复发 2~3 遍。

【这个脚本做什么】
在虚拟环境的 wechatauto/guia.py 末尾追加一段补丁：
统计深色像素时跳过鼠标指针覆盖的小矩形（16×28 像素），从根源避免误判。

【怎么用】
直接双击同目录下的「应用补丁.bat」即可（推荐）。
也可以手动指定路径：
  python patch-dedup.py ^
    %USERPROFILE%\\AppData\\Local\\wechatbot\\venv\\Lib\\site-packages\\wechatauto\\guia.py

【注意】
- 新版 bot.py 已内置同样的补丁，新装用户无需运行本脚本（运行也无副作用）。
- pip 重装/升级 wechatauto-replica 后补丁会失效，重新运行一次即可。
"""

import os
import py_compile
import sys

# ---- Windows 控制台切 UTF-8（否则中文/emoji 在 GBK 控制台下会乱码甚至崩溃）----
if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.kernel32.SetConsoleOutputCP(65001)
        ctypes.windll.kernel32.SetConsoleCP(65001)
    except Exception:
        pass
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

VENV = os.path.join(os.environ.get("USERPROFILE", ""),
                    "AppData", "Local", "wechatbot", "venv")
MARKER = "[雷霆补丁]"

PATCH_BLOCK = r'''

# ==================== [雷霆补丁] 防止鼠标指针导致消息重复发送 ====================
# 原理：_input_box_has_text 靠"输入框区域深色像素数量"判断消息是否已发出；
# 鼠标指针是深色的，停在输入框上会被误判成"还有文字没发出去"，库于是重试，
# 结果同一条消息被重复发好几遍。这里统计时跳过指针覆盖的小矩形。
def _thunder_input_box_has_text(self, box=None) -> bool:
    if box is None:
        box = self.get_input_box()
    if not box:
        return False
    x0, y0, x1, y1 = box
    rel = (x0 + 20, y0 + 10, x1 - 20, y0 + 200)
    scr = self._rel_to_screen(rel)
    img = self._grab_screen(scr)
    px = img.load()
    cx = cy = -99999
    try:
        import ctypes
        from ctypes import wintypes
        _pt = wintypes.POINT()
        if ctypes.windll.user32.GetCursorPos(ctypes.byref(_pt)):
            cx, cy = _pt.x - scr[0], _pt.y - scr[1]
    except Exception:
        pass
    dark = 0
    for y in range(0, img.size[1], 2):
        for x in range(0, img.size[0], 2):
            if abs(x - cx) <= 16 and abs(y - cy) <= 28:
                continue            # 跳过鼠标指针覆盖的区域
            if sum(px[x, y]) < 450:
                dark += 1
    return dark > 20


try:
    _thunder_input_box_has_text._thunder_patched = True
    WeChatGUI._input_box_has_text = _thunder_input_box_has_text
except Exception:
    pass
# ==================== [雷霆补丁 END] ====================
'''


def find_guia():
    """按优先级定位 wechatauto/guia.py。"""
    # 1) 命令行显式指定（可以是 目录 / venv 根目录 / guia.py 本身）
    if len(sys.argv) > 1:
        arg = os.path.abspath(sys.argv[1])
        for p in (arg,
                  os.path.join(arg, "guia.py"),
                  os.path.join(arg, "Lib", "site-packages", "wechatauto", "guia.py")):
            if os.path.isfile(p):
                return p

    # 2) 当前解释器里已经装了 wechatauto
    try:
        import wechatauto.guia as _g
        p = getattr(_g, "__file__", None)
        if p and os.path.isfile(p):
            return p
    except Exception:
        pass

    # 3) 默认安装位置（install.bat 创建）
    p = os.path.join(VENV, "Lib", "site-packages", "wechatauto", "guia.py")
    if os.path.isfile(p):
        return p

    # 4) 兜底：扫描 site-packages 里所有 wechatauto*
    sp = os.path.join(VENV, "Lib", "site-packages")
    if os.path.isdir(sp):
        for name in sorted(os.listdir(sp)):
            if name.lower().startswith("wechatauto"):
                q = os.path.join(sp, name, "guia.py")
                if os.path.isfile(q):
                    return q
    return None


def main():
    print("=" * 64)
    print("   雷霆DeepSeek微信自动回复脚本 · 防重复发送补丁")
    print("=" * 64)
    print()

    guia = find_guia()
    if not guia:
        print("[错误] 没找到 wechatauto/guia.py")
        print()
        print("可能原因：")
        print("  1. 还没运行过 install.bat（依赖没装）")
        print("  2. 安装到了非默认位置")
        print()
        print("手动指定路径的用法：")
        print("  python patch-dedup.py <你的虚拟环境路径>")
        print("  例如：python patch-dedup.py \"D:\\myvenv\"")
        return 1

    print("[1/3] 目标文件：")
    print("      " + guia)
    print()

    try:
        with open(guia, "r", encoding="utf-8") as f:
            src = f.read()
    except Exception as e:
        print("[错误] 读取失败：" + str(e))
        print("       可能没有权限，请用管理员身份运行。")
        return 1

    if MARKER in src:
        print("[2/3] 补丁已存在，无需重复安装。")
        print()
        print("✅ 已就位：鼠标指针不会再被误判成文字，消息不会重复发送。")
        return 0

    print("[2/3] 正在写入补丁 ...")
    try:
        with open(guia, "a", encoding="utf-8") as f:
            f.write(PATCH_BLOCK)
    except Exception as e:
        print("[错误] 写入失败：" + str(e))
        print("       可能没有写权限，请用管理员身份运行。")
        return 1

    print()
    print("[3/3] 语法自检 ...")
    try:
        py_compile.compile(guia, doraise=True)
        print("      ✅ 通过")
    except Exception as e:
        print("      ❌ 失败：" + str(e))
        print("      补丁写入异常，建议重跑 install.bat 修复依赖。")
        return 1

    print()
    print("=" * 64)
    print("   ✅ 补丁安装成功！")
    print()
    print("   下次启动 run.bat 时日志会出现：")
    print("      ✅ 已应用运行时补丁：防止鼠标指针导致消息重复发送")
    print()
    print("   提示：pip 重装依赖后补丁会失效，重新运行本脚本即可。")
    print("=" * 64)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n已取消。")
        sys.exit(1)
