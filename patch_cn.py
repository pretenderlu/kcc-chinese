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
    if total:
        print('如需还原英文原版：python patch_cn.py --restore')


if __name__ == '__main__':
    main()
