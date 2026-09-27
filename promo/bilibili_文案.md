# B 站图文/专栏文案

## 配图
1. 头图：`xhs_cover.png`
2. `kcc_main_clean.png` — 主界面全览（插入"汉化范围"一节）
3. `kcc_tooltip.png` — 悬停中文说明（插入"翻译细节"一节）
4. `kcc_editor.png` — 元数据编辑器（插入"翻译细节"一节）

## 标题
【汉化发布】漫画转 Kindle 神器 KCC 中文汉化版 v11.0.1，全界面中文 + 选项中文说明

## 正文

### 这是什么

KCC（Kindle Comic Converter）是漫画圈里公认的转换神器：把 CBZ/CBR/PDF/图片文件夹转换成 Kindle、Kobo 等电纸书专用的 MOBI/EPUB/CBZ 格式，自动裁边、跨页拆分、面板视图（把一页切成 4 格放大看）、条漫模式……功能非常多。

但问题也很明显：**全英文界面，30 多个选项全是专业术语**，什么 Spread splitter、Panel View 4/2/HQ、Inter-panel crop，光看名字根本不敢下手。

于是我给 KCC v11.0.1 做了完整汉化，并打包好了 exe，**开箱即用，不需要装 Python**。

### 下载

GitHub Releases（免登录直接下载）：
https://github.com/pretenderlu/kcc-chinese/releases

下载 `KCC-v11.0.1-zh_CN.exe`，双击即用。
（想转 MOBI 的话还需另装亚马逊官方的 KindleGen，软件里会提示；处理 CBZ/CBR 压缩包需安装 7z。）

### 汉化范围

- 主界面全部按钮、选项、标签中文化
- 250+ 条界面文本，包括**每个选项的悬停说明**——勾选/半勾选/不勾选分别是什么效果，都有中文详解
- 转换过程中的状态提示、错误信息也是中文
- 内置元数据编辑器（系列/卷/期号/作者）同步汉化

【此处插入 kcc_main_clean.png 主界面截图】

### 翻译细节

【此处插入 kcc_tooltip.png 悬停说明截图】

值得一提的是：设备型号（如 Kindle Paperwhite 12）和输出格式名（如 MOBI/AZW3）**有意保留英文**——这些文本在程序内部兼作逻辑键，翻译会导致功能失效。其余的能翻尽翻。

【此处插入 kcc_editor.png 元数据编辑器截图】

### 技术实现（感兴趣可以看）

汉化采用"补丁包"方案而不是 fork 魔改：一个 Python 脚本基于 tokenize 精确替换源码字符串字面量，对照表独立成 JSON 文件，一键打补丁、一键还原、可重复执行。上游 KCC 更新版本后，补丁脚本会自动报告哪些字符串变了，维护成本很低。

打包通过 GitHub Actions 自动完成，和官方一样基于 PyInstaller，体积（86MB）与官方 exe 基本一致。

项目地址（欢迎 Star / Issue 反馈错翻漏翻）：
https://github.com/pretenderlu/kcc-chinese

### 版权说明

KCC 原项目由 ciromattia 开发并开源（ISC 协议），本汉化仅修改界面显示文本，不改动任何转换逻辑，版权归原作者所有。汉化版同样免费发布，请勿用于商业用途。
