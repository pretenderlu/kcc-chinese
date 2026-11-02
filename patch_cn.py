#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KCC 一键汉化补丁
================

用法：
    python patch_cn.py                # 打补丁（默认目标为脚本旁的 kcc/ 目录）
    python patch_cn.py --dir <KCC源码目录>
    python patch_cn.py --restore      # 还原英文原版
    python patch_cn.py --force        # 版本不匹配时仍强制打补丁

原理：
    基于 tokenize 精确定位 Python 源码中的字符串字面量（含 f-string 片段），
    按 strings_zh.json 对照表把英文替换为中文。
    普通字符串按“字面值精确匹配”替换；f-string 按“片段替换”处理。
    首次打补丁前会自动备份原文件为 <文件名>.orig。
"""

import argparse
import ast
import io
import json
import re
import shutil
import sys
import tokenize
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
MAPPING_FILE = SCRIPT_DIR / 'strings_zh.json'
BACKUP_SUFFIX = '.orig'

# 悬停动画演示浮层（KCC_demo.py）注入配置
DEMO_MODULE = SCRIPT_DIR / 'KCC_demo.py'
DEMO_MARKER = 'KCC_ZH_DEMO_BEGIN'
DEMO_ANCHOR = 'MW.show()'          # KCCGUI.__init__ 末尾，演示在此之后安装
DEMO_HOOK = '''
        # KCC_ZH_DEMO_BEGIN（KCC 汉化版增强：悬停动画演示浮层）
        try:
            from . import KCC_demo
            KCC_demo.install_demos(GUI)
        except Exception:
            pass
        # KCC_ZH_DEMO_END
'''

# 汉化版标识（仓库信息）注入配置
BRAND_MARKER = 'KCC_ZH_BRAND_BEGIN'
BRAND_ANCHOR = 'MW.show()'         # KCCGUI.__init__ 末尾
BRAND_REPO = 'https://github.com/pretenderlu/kcc-chinese'
BRAND_HOOK = '''
        # KCC_ZH_BRAND_BEGIN（KCC 汉化版标识：标题后缀 + 状态栏仓库链接）
        try:
            from PySide6.QtWidgets import QPushButton as _zhQPushButton
            from PySide6.QtGui import QDesktopServices as _zhQDS, QCursor as _zhQCursor
            from PySide6.QtCore import QUrl as _zhQUrl, Qt as _zhQt
            _zhBrand = _zhQPushButton('汉化增强版 · GitHub')
            _zhBrand.setFlat(True)
            _zhBrand.setStyleSheet(
                'QPushButton{border:none;color:#3b82f6;text-decoration:underline;padding:0 8px;}'
                'QPushButton:hover{color:#1d4ed8;}')
            _zhBrand.setCursor(_zhQCursor(_zhQt.PointingHandCursor))
            _zhBrand.setToolTip('基于 ciromattia/kcc 的简体中文汉化 + 悬停动画演示增强\\n点击打开汉化版仓库：github.com/pretenderlu/kcc-chinese')
            _zhBrand.clicked.connect(lambda: _zhQDS.openUrl(
                _zhQUrl('https://github.com/pretenderlu/kcc-chinese')))
            MW.statusBar().addPermanentWidget(_zhBrand)
            MW.setWindowTitle(MW.windowTitle() + '（汉化增强版）')
        except Exception:
            pass
        # KCC_ZH_BRAND_END
'''


# KFX 直接生成（汉化增强）注入配置
# 写入器来源：HankunYu/kindle-comic-workaround-5.19.x v1.3.1（MIT，见 vendor_kfx/README.md）
KFX_VENDOR_DIR = SCRIPT_DIR / 'vendor_kfx'
KFX_VENDOR_FILES = ('kfx_writer.py', 'kpf_generator.py')
KFX_MARKER = 'KCC_ZH_KFX_BEGIN'
# 锚点：makeBook() 的 tome 循环中 EPUB 输出分支（else: 下一行含 Creating EPUB file）
KFX_ANCHOR_NEXT = 'Creating EPUB file'
KFX_HOOK = '''        elif getattr(options, 'kfx_direct', False):
            # KCC_ZH_KFX_BEGIN（汉化增强：伪格式 KFXD，直接生成 KFX，无需 Calibre / Kindle Previewer）
            # 注意：上游在 checkOptions 里把 format 'KFX' 改写为 'EPUB' + options.kfx=True；
            # 我们新增的 'KFXD' 同样改写为 'EPUB'，但额外置 kfx_direct=True 走直出分支
            print(f"{job_progress}生成 KFX 文件...")
            if GUI:
                GUI.progressBarTick.emit(f'{job_progress}生成 KFX 文件')
            from . import kpf_generator as _kpfg
            sys.modules.setdefault('kpf_generator', _kpfg)  # kfx_writer 用的是扁平绝对导入
            from . import kfx_writer as _kfxw
            if cover and (cover.smartcover or options.customcover):
                cover.save_to_folder(os.path.join(tome, 'OEBPS', 'Images', '##cover.jpg'), tomeNumber, len(tomes))
            _kfx_images = []
            for _kfx_root, _kfx_dirs, _kfx_files in os.walk(os.path.join(tome, 'OEBPS', 'Images')):
                _kfx_dirs[:] = os_sorted(_kfx_dirs)
                for _kfx_f in os_sorted(_kfx_files):
                    if getImageFileName(_kfx_f)[1] in IMAGE_TYPES:
                        _kfx_images.append(os.path.join(_kfx_root, _kfx_f))
            # KFX 写入器只支持 JPEG/PNG，管线可能产出 GIF/WebP（kindle_azw3/forcewebp 等），
            # 兜底转换时尊重用户的「PNG 输出」选择：勾选转 PNG（无损），否则转 JPEG
            for _kfx_i, _kfx_p in enumerate(_kfx_images):
                _kfx_im = Image.open(_kfx_p)
                if _kfx_im.format not in ('JPEG', 'PNG'):
                    if options.forcepng:
                        _kfx_newp = os.path.splitext(_kfx_p)[0] + '-kfx.png'
                        _kfx_im.save(_kfx_newp, 'PNG', optimize=1)
                    else:
                        _kfx_im = _kfx_im.convert('RGB')
                        _kfx_newp = os.path.splitext(_kfx_p)[0] + '-kfx.jpg'
                        _kfx_im.save(_kfx_newp, 'JPEG', quality=92)
                    _kfx_images[_kfx_i] = _kfx_newp
                _kfx_im.close()
            if len(tomes) > 1:
                filepath.append(getOutputFilename(source, options.output, '.kfx', ' ' + str(tomeNumber)))
            else:
                filepath.append(getOutputFilename(source, options.output, '.kfx', ''))
            _kfxw.generate_kfx(_kfx_images, filepath[-1], title=options.title,
                               author=options.authors[0] if options.authors else '',
                               reading_direction='rtl' if options.righttoleft else 'ltr',
                               language=options.language)
            # KCC_ZH_KFX_END
'''


def inject_kfx(root):
    """把 KFX 写入器（vendor_kfx/）拷入源码树，并注入直出 KFX 分支与相关提示文案。"""
    if not KFX_VENDOR_DIR.is_dir():
        print('  警告：vendor_kfx/ 不存在，KFX 直出注入跳过')
        return
    pkg = root / 'kindlecomicconverter'
    for name in KFX_VENDOR_FILES:
        shutil.copy2(KFX_VENDOR_DIR / name, pkg / name)

    # (模式, 文件, 锚点, 注入内容, 幂等标记)
    # 模式 before_else：在「else: + 下一行含锚点」前插入；after_line：在锚点行后插入；before_line：在锚点行前插入
    hooks = [
        # checkOptions()：新增伪格式 KFXD（直出 KFX）。保留上游 'KFX' 原行为（KFX-ready EPUB + 195MB 分卷）
        ('before_line', pkg / 'comic2ebook.py', '# Override profile data',
         '''    # KCC_ZH_KFXD_BEGIN 汉化增强：伪格式 KFXD，直出 KFX（不强制分卷，USB 侧载无 200MB 限制）
    if options.format == 'KFXD':
        options.format = 'EPUB'
        options.kfx = True
        options.kfx_direct = True
        options.panelview = False
    # KCC_ZH_KFXD_END
''', 'KCC_ZH_KFXD_BEGIN'),
        # Scribe 2480 支持：kindle_scribe_azw3 赋值之后，KFXD 直出不经过 kindlegen（无 1920 限高），禁用上下半页切分
        ('after_line', pkg / 'comic2ebook.py', "options.kindle_scribe_azw3 = options.profile.startswith('KS') and options.kindle_azw3",
         '''    if getattr(options, 'kfx_direct', False):
        # KCC_ZH_KFXD_2480_BEGIN KFX 直出不依赖 kindlegen，整页 2480 全高直接写入，无需 above/below 切分
        options.kindle_scribe_azw3 = False
        # KCC_ZH_KFXD_2480_END
''', 'KCC_ZH_KFXD_2480_BEGIN'),
        # makeBook() tome 循环：EPUB 输出分支前插入 KFX 直出分支
        ('before_else', pkg / 'comic2ebook.py', KFX_ANCHOR_NEXT, KFX_HOOK, KFX_MARKER),
        # makeBook() 进度条提示：KFXD 时显示「生成 KFX 文件」而非「压缩 EPUB 文件」
        ('before_else', pkg / 'comic2ebook.py', '压缩 EPUB 文件',
         '''        elif getattr(options, 'kfx_direct', False):
            # KCC_ZH_KFXGUI_A_BEGIN
            GUI.progressBarTick.emit(f'{job_progress}生成 KFX 文件')
            # KCC_ZH_KFXGUI_A_END
''', 'KCC_ZH_KFXGUI_A_BEGIN'),
        # KCC_gui.py 转换开始日志：KFXD 时显示「生成 KFX 文件」
        ('before_else', pkg / 'KCC_gui.py', 'QT_TRANSLATE_NOOP(\'KCCGUI\', "创建 EPUB 文件"), \'info\', False',
         '''            elif gui_current_format == 'KFXD':
                # KCC_ZH_KFXGUI_B_BEGIN
                MW.addMessage.emit(QT_TRANSLATE_NOOP('KCCGUI', "生成 KFX 文件"), 'info', False)
                GUI.progress.content = QCoreApplication.translate('KCCGUI', "生成 KFX 文件")
                # KCC_ZH_KFXGUI_B_END
''', 'KCC_ZH_KFXGUI_B_BEGIN'),
        # KCC_gui.py 转换完成日志：KFXD 时显示「生成 KFX 文件……完成！」
        ('before_else', pkg / 'KCC_gui.py', '"创建 EPUB 文件……<b>完成！</b>"',
         '''                elif gui_current_format == 'KFXD':
                    # KCC_ZH_KFXGUI_C_BEGIN
                    MW.addMessage.emit(QT_TRANSLATE_NOOP('KCCGUI', "生成 KFX 文件……<b>完成！</b>"), 'info', True)
                    # KCC_ZH_KFXGUI_C_END
''', 'KCC_ZH_KFXGUI_C_BEGIN'),
        # KCC_gui.py 格式下拉框：新增「KFX（直接生成）」条目（伪格式 KFXD）
        ('after_line', pkg / 'KCC_gui.py', "'format': 'KFX'},",
         '''            "KFX（直接生成 · 无需 Calibre）": {'icon': 'KFX', 'format': 'KFXD'},  # KCC_ZH_KFXD_FMT
''', 'KCC_ZH_KFXD_FMT'),
    ]
    for mode, target, anchor, hook, marker in hooks:
        text = target.read_bytes().decode('utf-8')
        if marker in text:
            print(f'KFX 直出: {target.name} 已注入过（{marker}），跳过')
            continue
        lines = text.splitlines(keepends=True)
        done = False
        for i, ln in enumerate(lines):
            if mode == 'after_line' and anchor in ln:
                eol = '\r\n' if ln.endswith('\r\n') else '\n'
                lines.insert(i + 1, hook.replace('\n', eol))
                done = True
                break
            if mode == 'before_line' and ln.strip() == anchor:
                eol = '\r\n' if ln.endswith('\r\n') else '\n'
                lines.insert(i, hook.replace('\n', eol))
                done = True
                break
            if mode == 'before_else' and ln.strip() == 'else:' and i + 1 < len(lines) and anchor in lines[i + 1]:
                eol = '\r\n' if ln.endswith('\r\n') else '\n'
                lines.insert(i, hook.replace('\n', eol))
                done = True
                break
        if done:
            target.write_bytes(''.join(lines).encode('utf-8'))
            print(f'KFX 直出: 已注入 {target.name}（{marker}）')
        else:
            print(f'  警告：KFX 注入锚点未找到（{marker}），已跳过')


def inject_branding(root):
    """在 KCCGUI 初始化末尾注入汉化版标识（标题后缀 + 仓库链接按钮）。"""
    gui_file = root / 'kindlecomicconverter' / 'KCC_gui.py'
    text = gui_file.read_bytes().decode('utf-8')
    if BRAND_MARKER in text:
        print('汉化标识: 已注入过，跳过')
        return
    lines = text.splitlines(keepends=True)
    for i, ln in enumerate(lines):
        if ln.strip() == BRAND_ANCHOR:
            eol = '\r\n' if ln.endswith('\r\n') else '\n'
            hook = BRAND_HOOK.replace('\n', eol)
            lines.insert(i + 1, hook)
            gui_file.write_bytes(''.join(lines).encode('utf-8'))
            print('汉化标识: 已注入 kindlecomicconverter/KCC_gui.py')
            return
    print('  警告：汉化标识注入锚点未找到，已跳过')


def inject_demo(root):
    """把 KCC_demo.py 拷入源码树，并在 KCCGUI 初始化末尾注入安装调用。"""
    if not DEMO_MODULE.exists():
        return
    pkg = root / 'kindlecomicconverter'
    shutil.copy2(DEMO_MODULE, pkg / 'KCC_demo.py')
    gui_file = pkg / 'KCC_gui.py'
    text = gui_file.read_bytes().decode('utf-8')
    if DEMO_MARKER in text:
        print('演示浮层: 已注入过，跳过')
        return
    lines = text.splitlines(keepends=True)
    for i, ln in enumerate(lines):
        if ln.strip() == DEMO_ANCHOR:
            eol = '\r\n' if ln.endswith('\r\n') else '\n'
            hook = DEMO_HOOK.replace('\n', eol)
            lines.insert(i + 1, hook)
            gui_file.write_bytes(''.join(lines).encode('utf-8'))
            print('演示浮层: 已注入 kindlecomicconverter/KCC_gui.py')
            return
    print('  警告：演示浮层注入锚点未找到，已跳过')


def escape_fragment(s):
    """把字符串转义成它在 .py 源码里的原始文本形式（用于匹配 f-string 片段）。"""
    return (s.replace('\\', '\\\\')
             .replace('\n', '\\n')
             .replace('\t', '\\t')
             .replace('\r', '\\r'))


def quote_string(s):
    """把字符串生成一个合法的 Python 双引号字面量（非 ASCII 保持原文）。"""
    return json.dumps(s, ensure_ascii=False)


def patch_source(text, strings, fstrings):
    """对单个源码文本执行替换，返回 (新文本, 命中条目集合, 替换次数)。"""
    hit = set()
    count = 0
    lines = text.splitlines(keepends=True)
    # 预先算好每行起始偏移，便于按 (row, col) 定位
    offsets = [0]
    for ln in lines:
        offsets.append(offsets[-1] + len(ln))

    tokens = list(tokenize.generate_tokens(io.StringIO(text).readline))
    # 待替换区间：(start_offset, end_offset, new_text)，从后往前应用
    edits = []
    fstring_middle = getattr(tokenize, 'FSTRING_MIDDLE', None)

    for tok in tokens:
        if tok.type == tokenize.STRING:
            raw = tok.string
            try:
                value = ast.literal_eval(raw)
            except (ValueError, SyntaxError):
                value = None
            if isinstance(value, str) and value in strings:
                edits.append((tok.start, tok.end, quote_string(strings[value])))
                hit.add(value)
            elif value is None and re.match(r'(?i)^[rubf]*f', raw):
                # Python < 3.12：f-string 是单个 STRING token，做片段替换
                new_raw = raw
                for en, zh in fstrings.items():
                    frag = escape_fragment(en)
                    if frag in new_raw:
                        new_raw = new_raw.replace(frag, escape_fragment(zh))
                        hit.add(en)
                if new_raw != raw:
                    edits.append((tok.start, tok.end, new_raw))
        elif fstring_middle is not None and tok.type == fstring_middle:
            # Python >= 3.12：f-string 的静态文本部分是 FSTRING_MIDDLE token
            new_raw = tok.string
            for en, zh in fstrings.items():
                frag = escape_fragment(en)
                if frag in new_raw:
                    new_raw = new_raw.replace(frag, escape_fragment(zh))
                    hit.add(en)
            if new_raw != tok.string:
                edits.append((tok.start, tok.end, new_raw))

    for (start, end, new_text) in sorted(edits, reverse=True):
        s = offsets[start[0] - 1] + start[1]
        e = offsets[end[0] - 1] + end[1]
        text = text[:s] + new_text + text[e:]
        count += 1
    return text, hit, count


def find_version(root):
    init = root / 'kindlecomicconverter' / '__init__.py'
    if init.exists():
        m = re.search(r"__version__\s*=\s*'([^']+)'",
                      init.read_text(encoding='utf-8'))
        if m:
            return m.group(1)
    return None


def main():
    # Windows 控制台默认 GBK，避免中文输出乱码
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding='utf-8', errors='replace')
        except Exception:
            pass

    ap = argparse.ArgumentParser(description='KCC 一键汉化补丁')
    ap.add_argument('--dir', default=None, help='KCC 源码目录（默认：脚本旁的 kcc/）')
    ap.add_argument('--restore', action='store_true', help='还原英文原版')
    ap.add_argument('--no-demo', action='store_true', help='纯汉化版：不注入悬停动画演示（仍注入汉化版标识）')
    ap.add_argument('--force', action='store_true', help='版本不匹配时仍强制执行')
    args = ap.parse_args()

    root = Path(args.dir) if args.dir else SCRIPT_DIR / 'kcc'
    if not (root / 'kindlecomicconverter').is_dir():
        sys.exit(f'错误：{root} 不是有效的 KCC 源码目录，请用 --dir 指定。')
    root = root.resolve()

    mapping = json.loads(MAPPING_FILE.read_text(encoding='utf-8'))
    files = sorted(set(mapping['strings']) | set(mapping['fstrings']))

    if args.restore:
        restored = 0
        for rel in files:
            bak = root / (rel + BACKUP_SUFFIX)
            target = root / rel
            if bak.exists():
                shutil.copy2(bak, target)
                bak.unlink()
                restored += 1
                print(f'已还原: {rel}')
        demo = root / 'kindlecomicconverter' / 'KCC_demo.py'
        if demo.exists():
            demo.unlink()
            print('已删除: kindlecomicconverter/KCC_demo.py')
        for name in KFX_VENDOR_FILES:
            vend = root / 'kindlecomicconverter' / name
            if vend.exists():
                vend.unlink()
                print(f'已删除: kindlecomicconverter/{name}')
        if restored:
            print(f'完成，共还原 {restored} 个文件。')
        else:
            print('没有找到备份文件，无需还原。')
        return

    version = find_version(root)
    expected = mapping.get('kcc_version')
    print(f'目标目录: {root}')
    print(f'KCC 版本: {version or "未知"}（本补丁基于 {expected} 制作）')
    if version and expected and version != expected and not args.force:
        sys.exit('版本不匹配！字符串可能已变动，已中止。\n'
                 '如确认要强制打补丁，请加 --force（建议先用 --restore 还原旧补丁）。')

    total = 0
    for rel in files:
        target = root / rel
        if not target.exists():
            print(f'跳过（文件不存在）: {rel}')
            continue
        backup = root / (rel + BACKUP_SUFFIX)
        if not backup.exists():
            shutil.copy2(target, backup)

        text = target.read_bytes().decode('utf-8')
        strings = mapping['strings'].get(rel, {})
        fstrings = mapping['fstrings'].get(rel, {})
        new_text, hit, count = patch_source(text, strings, fstrings)

        missing = (set(strings) | set(fstrings)) - hit
        if count:
            target.write_bytes(new_text.encode('utf-8'))
            print(f'已汉化: {rel}（替换 {count} 处）')
        else:
            print(f'无需修改: {rel}（可能已打过补丁）')
        for m in sorted(missing):
            print(f'  警告：未找到字符串 {m!r}（上游可能已改动）')
        total += count

    print(f'\n完成，共替换 {total} 处。')
    if args.no_demo:
        print('纯汉化版：跳过悬停动画演示与 KFX 直出注入。')
    else:
        inject_demo(root)
        inject_kfx(root)
    inject_branding(root)
    if total:
        print('如需还原英文原版：python patch_cn.py --restore')


if __name__ == '__main__':
    main()
