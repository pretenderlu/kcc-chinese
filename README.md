# KCC 一键汉化补丁

对 [KCC (Kindle Comic Converter)](https://github.com/ciromattia/kcc) 的 GUI 界面进行汉化。
基于 KCC **v11.0.3** 制作，共翻译 250 余处界面文本（按钮、选项、工具提示、状态消息、对话框）。

## 使用方法

```bash
# 1. 克隆 KCC 源码到本目录（得到 kcc/ 子目录）
git clone https://github.com/ciromattia/kcc.git kcc

# 2. 一键打补丁
python patch_cn.py

# 3. 运行汉化版
cd kcc
pip install -r requirements.txt
python kcc.py
```

## 其他命令

```bash
python patch_cn.py --restore   # 还原为英文原版
python patch_cn.py --dir D:\path\to\kcc   # 指定其他 KCC 源码目录
python patch_cn.py --force     # KCC 版本与补丁不一致时强制执行（不推荐）
```

## 说明

- 首次打补丁前会自动备份原文件为 `<文件名>.orig`，`--restore` 用备份还原。
- 补丁是幂等的：重复运行不会重复替换。
- 补丁基于 Python `tokenize` 精确替换字符串字面量，不会误改代码逻辑。
- 设备型号（如 `Kindle Scribe 3`）和输出格式（如 `MOBI/AZW3`）的下拉项
  在程序中兼作逻辑键，**有意保留英文**，翻译它们会导致功能失效。
- 命令行输出（`comic2ebook.py` 的 print 日志等）未翻译，仅汉化 GUI 可见文本。

## 文件

- `patch_cn.py` — 补丁脚本
- `strings_zh.json` — 英中对照表（`strings` 为整串精确匹配，`fstrings` 为 f-string 片段匹配）

## 打包汉化版 exe

```bash
pip install pyinstaller
cd kcc
python -m PyInstaller --clean -y kcc.spec
# 产物：kcc/dist/kcc.exe
```

也可以用 GitHub Actions 自动打包：`.github/workflows/build.yml` 已配置好，
推送到 GitHub 后在 Actions 页手动触发（workflow_dispatch）即可产出
Windows 的 `KCC-v11.0.3-zh_CN-windows.exe` 和 macOS 的 dmg（arm64 / intel）。
打 `v*` 标签会自动创建 Release 并附上全部平台产物。
升级 KCC 版本时记得同步修改工作流里的 `ref` 标签、产物文件名和
`strings_zh.json` 里的 `kcc_version`。

注意：macOS 版未做 Apple 签名/公证（与上游官方包相同），
首次打开需在"系统设置 → 隐私与安全性"里允许，或右键 → 打开。

## 上游更新后如何维护

1. `git -C kcc pull` 更新源码（若有冲突可先 `--restore` 再更新）。
2. 运行 `python patch_cn.py --force`。
3. 脚本会列出"未找到字符串"的警告——这些是上游新增或改动过的文本，
   在 `strings_zh.json` 中更新对应条目后重新打补丁即可。
