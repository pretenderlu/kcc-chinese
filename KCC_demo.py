# -*- coding: utf-8 -*-
"""悬停动画演示浮层（KCC 汉化版增强，非上游功能）。

鼠标悬停在特定选项上时，在主窗口上半部分固定位置弹出演示卡片：
圆角 + 投影 + 淡入动效，卡片内是 QPainter 实时绘制的 60fps 矢量动画。

动画内容严格按代码实际行为制作。除非选项本身是横版专属功能，
演示页面统一使用竖版画面。

卡片排版规则：动画画面必须在卡片内保持居中；标题、副标题等文字
过长时应在适当位置换行，不得用单行长句把卡片撑宽导致动画偏移。
补充提示（tips）单独占一行，以小灯泡 💡 开头（不用斜体）。
- 跨页拆分（rotateBox → options.splitter）：
  不勾选=0 仅切割；半勾选=2 切割+旋转（输出三页）；勾选=1 仅旋转
- 面板视图（qualityBox → autoscale/hq）：
  不勾选=4 面板；半勾选=2 面板（上下）；勾选=4 高清面板
- 从右向左（mangaBox → righttoleft）：页面/分格阅读顺序翻转
- 条漫模式（webtoonBox → webtoon）：多页拼接为长条，再按屏高沿格子间隙重切
- 裁剪模式（croppingBox → options.cropping）：
  不勾选=0 不裁剪；半勾选=1 cropMargin 裁白边；
  勾选=2 cropPageNumber 以页码和画面为界裁掉外围（页码保留）
- 拉伸/放大（upscaleBox → stretch/upscale）：
  不勾选=小图保持原尺寸；半勾选=stretch 强制拉伸铺满（可能变形）；
  勾选=upscale 等比放大适配
- 彩色模式（colorBox → forcecolor）：不勾选=转灰度（墨水屏）；勾选=保留彩色
- 黑/白边距（borderBox）：不勾选=自动检测填充色；半勾选=白边；勾选=黑边
- 自定义伽马（gammaBox → gamma）：gamma>1 压暗中间调，<1 提亮
- 跨页偏移（spreadShiftBox → spreadshift）：配对起点后移一页，跨页正确拼合
- 面板间裁剪（interPanelCropBox → interpanelcrop）：
  不勾选=保留间隔；半勾选=裁横向空白带；勾选=横竖都裁
- 自定义自动对比度（autocontrastBox）：
  不勾选=仅黑白页增强（默认）；半勾选=禁用；勾选=黑白+彩色都增强
- 不旋转（noRotateBox → norotate）：跨页拆分时锁定双页方向，不旋转
- 纵向 4 面板（vertical4PanelBox → vertical4panel）：4 面板放大的阅读顺序，
  不勾选=先顶部两格（横向）；勾选=先两侧格（纵向/竖排）。
  前置条件：面板视图已启用（面板视图 4/2/高清或旧版面板视图），Webtoon 模式下无效
- 1x4 转 2x2 条带（maximizeStrips → maximizestrips）：1x4 条带重排为 2x2
- 彩虹纹消除（eraseRainbowBox → eraserainbow）：衰减干扰频率
- 文件合并（fileFusionBox → filefusion）：多文件合并为单个输出
- JPEG/PNG/mozJpeg（mozJpegBox）：不勾选=JPEG；半勾选=forcepng 无损 PNG；
  勾选=mozjpeg 同画质小 10-20%、耗时翻倍
- 极限黑点（autoLevelBox → autolevel）：黑点设为最常见的暗色像素值，
  发灰扫描页的文字变得更黑更实（image.py autolevelImage）
- 分卷大小（chunkSizeCheckBox → targetsize）：不勾选=默认上限
  （条漫 100MB，其他 400MB）；勾选=按设定 MB 拆分为多卷
- 元数据标题（metadataTitleBox → metadatatitle）：不勾选=默认标题；
  半勾选=默认+元数据标题；勾选=仅元数据标题
- 禁用处理（disableProcessingBox → noprocessing）：图片原样打包，
  忽略设备配置与所有处理选项
- 删除输入（deleteBox → delete）：转换完成后删除输入文件（不可恢复）
- 输出拆分（outputSplit → batchsplit=2）：不勾选=自动拆分；
  勾选=每个子目录单独输出一卷
- 首先旋转（rotateFirstBox → rotatefirst）：跨页拆分半勾选时，旋转版
  跨页排在拆分页面之前（勾选）或之后（不勾选，默认）
- 向右旋转（rotateRightBox → rotateright）：跨页默认逆时针旋转 90°，
  勾选后改为顺时针（向右）
- 智能封面裁剪（smartCoverCropBox → smartcovercrop）：宽幅图（宽/高>1.83）
  裁出封面区域（从左到右阅读取偏右一段），丢弃其余部分
- 封面填充（coverFillBox → coverfill）：封面按设备宽高比居中裁剪后填满
  屏幕；默认仅等比缩放，可能留边
- 反转方向（invertDirectionBox → invertdirection）：仅反转 EPUB 翻页方向
  （page-progression-direction），页面内容顺序不变；方向以「从右向左」
  设置为基准取反（普通 LTR 漫画不勾选时不受影响）
- 轻小说模式（lightnovelBox → lightnovel）：保留原始文件结构，仅调整
  图片尺寸（不重组为标准 EPUB 结构）
- 单页横屏（onePageLandscapeBox → onepagelandscape）：横屏时所有页
  page-spread=center（单页居中视口），默认 left/right 配对
- 壁纸模式（wallpaperBox）：自动勾选 KOReader 壁纸所需选项
  （图像文件夹/仅旋转/不旋转/放大/无损 PNG）
- 保留 ComicInfo.xml（keepComicInfoBox → keepcomicinfo）：仅 CBZ 输出时
  保留原始 ComicInfo.xml
- 自定义 JPEG 质量（jpegQualityBox → jpegquality）：不勾选=默认 85
  （KS/KCS 为 90）；勾选=自定义 0~95，越低体积越小画质越差
- 不量化（noQuantizeBox → noquantize）：PNG 输出默认量化到 16 色（4 位），
  勾选后保留完整灰阶（作用于「JPEG/PNG/mozJpeg」半勾选的 PNG 输出）
- WebP（webpBox → webp）：有损 WebP 替换 JPG、无损 WebP 替换 PNG；
  PDF 与 Kindle MOBI/AZW3 输出不生效
- 强制 EBOK（ebokBox → ebok）：MOBI 标记为 EBOK 归入 Kindle「图书」，
  默认 PDOC 归入「文档」；仅 MOBI 输出生效
- 临时目录（tempDirBox → tempdir）：不勾选=系统盘临时目录；
  勾选=源文件所在盘
- PNG 兼容模式（pngLegacyBox → pnglegacy）：8 位灰度 PNG 代替 4 位
  调色板 PNG（作用于 PNG 输出路径）
- 强制 PNG RGB（forcePngRgbBox → force_png_rgb）：全彩图片也保存为
  无损 PNG，体积显著增大（作用于 PNG 输出路径）
- 旧版面板视图（legacyPanelViewBox → legacypanelview）：KCC 6 的面板
  视图方式，放大格固定 1.5x；适用于固件 5.19.2（回退前）/5.19.3+
- PDF 宽度渲染（pdfWidthBox → pdfwidth）：矢量 PDF 竖版页按设备宽度
  渲染（默认按高度）；横版页始终按高度
- 旧版提取（legacyExtractBox → legacyextract）：直接抽取 PDF/EPUB
  内嵌原图（默认整页渲染），渲染出问题时可尝试

调试：设置环境变量 KCC_DEMO_AUTO=spread|panel|manga|webtoon|crop|upscale|color|
border|gamma|spreadshift|interpanel|autocontrast|norotate|v4panel|strips|
rainbow|filefusion|imgformat|autolevel|chunksize|metatitle|noprocessing|
deleteinput|outputsplit|rotatefirst|rotateright|smartcover|coverfill|
invertdir|lightnovel|onepagelandscape|wallpaper|comicinfo|
jpgq|noquant|webp|ebok|tempdir|
pnglegacy|pngrgb|legacypv|pdfwidth|legacyextract
可在启动后自动弹出对应演示，并把定位信息写入 ~/kcc_demo_debug.log。
"""

import math
import os

from PySide6.QtCore import (QEasingCurve, QElapsedTimer, QEvent, QObject, QPoint,
                            QPointF, QPropertyAnimation, QRect, QRectF, Qt, QTimer)
from PySide6.QtGui import (QColor, QImage, QLinearGradient, QPainter, QPainterPath,
                           QPen, QPolygon)
from PySide6.QtWidgets import (QApplication, QFrame, QGraphicsDropShadowEffect,
                               QLabel, QVBoxLayout, QWidget)

_SHADOW = 14          # 阴影留白（绘制内容向内收缩的量）
_ACCENT = QColor(59, 130, 246)
_CHIPS = ('不勾选', '半勾选', '勾选')


def _ease(t):
    """easeInOutCubic，t ∈ [0,1]。"""
    t = max(0.0, min(1.0, t))
    return 4 * t * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 3) / 2


def _mix(c1, c2, k):
    """颜色线性插值。"""
    return QColor(int(c1.red() + (c2.red() - c1.red()) * k),
                  int(c1.green() + (c2.green() - c1.green()) * k),
                  int(c1.blue() + (c2.blue() - c1.blue()) * k))


def _tone(p, rect, spacing=6, r=1.1, color=QColor(110, 110, 110, 130)):
    """在 rect 内绘制网点纸（screentone）圆点。"""
    p.save()
    p.setClipRect(rect)
    p.setPen(Qt.NoPen)
    p.setBrush(color)
    y = rect.top() + spacing / 2
    while y < rect.bottom():
        x = rect.left() + spacing / 2
        while x < rect.right():
            p.drawEllipse(QPoint(int(x), int(y)), r, r)
            x += spacing
        y += spacing
    p.restore()


def _speed_lines(p, rect, count=7, color=QColor(90, 90, 90, 160)):
    """在 rect 内绘制速度线。"""
    p.save()
    p.setClipRect(rect)
    step = rect.height() / (count + 1)
    for i in range(count):
        c = QColor(color)
        c.setAlpha(90 + (i * 97) % 110)
        p.setPen(QPen(c, 1))
        y = rect.top() + step * (i + 1)
        p.drawLine(rect.left() + 2, int(y), rect.right() - 2, int(y))
    p.restore()


def _panel_art(p, rect, kind):
    """在一格面板内画一种内容：0=天空场景 1=网点 2=速度线 3=剪影。"""
    p.setPen(QPen(QColor(120, 120, 120), 1))
    p.setBrush(QColor(250, 250, 250))
    p.drawRect(rect)
    inner = rect.adjusted(2, 2, -2, -2)
    if kind == 0:
        grad = QLinearGradient(inner.topLeft(), inner.bottomLeft())
        grad.setColorAt(0, QColor(168, 205, 236))
        grad.setColorAt(1, QColor(240, 247, 252))
        p.setPen(Qt.NoPen)
        p.setBrush(grad)
        p.drawRect(inner)
        p.setBrush(QColor(96, 125, 139, 200))
        p.drawPolygon(QPolygon([QPoint(inner.left(), inner.bottom()),
                                QPoint(int(inner.center().x()),
                                       int(inner.top() + inner.height() * 0.4)),
                                QPoint(inner.right(), inner.bottom())]))
        p.setBrush(QColor(255, 255, 255))
        p.setPen(QPen(QColor(120, 120, 120), 1))
        p.drawEllipse(int(inner.left() + inner.width() * 0.55), int(inner.top() + 5),
                      int(inner.width() * 0.36), int(inner.height() * 0.28))
    elif kind == 1:
        _tone(p, inner)
    elif kind == 2:
        _speed_lines(p, inner)
    else:
        p.save()
        p.setClipRect(inner)
        p.setPen(QPen(QColor(100, 100, 100, 150), 1))
        for i in range(-4, 12):
            p.drawLine(inner.left(), int(inner.top() + i * inner.height() / 6),
                       inner.right(), int(inner.top() + (i - 2) * inner.height() / 6))
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(66, 66, 66, 220))
        p.drawRoundedRect(int(inner.center().x() - 7),
                          int(inner.top() + inner.height() * 0.2),
                          14, int(inner.height() * 0.6), 6, 6)
        p.restore()


def draw_manga_page(p, rect, variant=0):
    """画一页"像漫画"的页面：白纸 + 分格 + 内容。"""
    p.save()
    p.setRenderHint(QPainter.Antialiasing)
    p.setPen(QPen(QColor(176, 176, 176), 1))
    p.setBrush(QColor(253, 253, 251))
    p.drawRoundedRect(rect, 2, 2)
    inner = rect.adjusted(6, 6, -6, -6)

    if variant == 0:
        # 上：大场景；下：左右两小格
        top = QRect(inner.left(), inner.top(), inner.width(), int(inner.height() * 0.55))
        _panel_art(p, top, 0)
        h = inner.height() - top.height() - 4
        left = QRect(inner.left(), top.bottom() + 4, int(inner.width() * 0.48), h)
        right = QRect(left.right() + 4, left.top(), inner.right() - left.right() - 4, h)
        _panel_art(p, left, 1)
        _panel_art(p, right, 2)
    elif variant == 1:
        # 左：纵向动作格；右：上下两小格
        left = QRect(inner.left(), inner.top(), int(inner.width() * 0.55), inner.height())
        _panel_art(p, left, 3)
        w = inner.right() - left.right() - 4
        rtop = QRect(left.right() + 4, inner.top(), w, int(inner.height() * 0.48))
        rbot = QRect(rtop.left(), rtop.bottom() + 4, w, inner.bottom() - rtop.bottom() - 4)
        _panel_art(p, rtop, 1)
        _panel_art(p, rbot, 1)
    else:
        # 2x2 四等分（面板视图演示用）
        w = (inner.width() - 4) // 2
        h = (inner.height() - 4) // 2
        _panel_art(p, QRect(inner.left(), inner.top(), w, h), 0)
        _panel_art(p, QRect(inner.left() + w + 4, inner.top(),
                            inner.right() - inner.left() - w - 4, h), 1)
        _panel_art(p, QRect(inner.left(), inner.top() + h + 4, w,
                            inner.bottom() - inner.top() - h - 4), 2)
        _panel_art(p, QRect(inner.left() + w + 4, inner.top() + h + 4,
                            inner.right() - inner.left() - w - 4,
                            inner.bottom() - inner.top() - h - 4), 3)
    p.restore()


def draw_spread(p, center, pw, ph, gap):
    """以 center 为中心画一组双页跨页，返回整体外框。"""
    total = pw * 2 + gap
    lx = int(center.x() - total / 2)
    ty = int(center.y() - ph / 2)
    draw_manga_page(p, QRect(lx, ty, pw, ph), variant=0)
    draw_manga_page(p, QRect(lx + pw + gap, ty, pw, ph), variant=1)
    return QRect(lx, ty, int(total), ph)


_PAGE_IMG_CACHE = {}


def _page_image(w, h, variant, gray):
    """把漫画页离屏渲染成 QImage 并缓存；gray=True 时转为灰度图。"""
    key = (w, h, variant, gray)
    img = _PAGE_IMG_CACHE.get(key)
    if img is None:
        img = QImage(w, h, QImage.Format_ARGB32)
        img.fill(QColor(255, 255, 255))
        pp = QPainter(img)
        pp.setRenderHint(QPainter.Antialiasing)
        draw_manga_page(pp, QRect(0, 0, w, h), variant=variant)
        pp.end()
        if gray:
            img = img.convertToFormat(QImage.Format_Grayscale8)
        _PAGE_IMG_CACHE[key] = img
    return img


class DemoCanvas(QWidget):
    """动画画布：按 demo 类型分场景循环绘制。"""

    def __init__(self, demo, parent=None):
        super().__init__(parent)
        self.demo = demo
        self.setFixedSize(420, 280)
        self._clock = QElapsedTimer()
        self._timer = QTimer(self)
        self._timer.setInterval(16)
        self._timer.timeout.connect(self.update)

    def start(self):
        self._clock.start()
        self._timer.start()

    def stop(self):
        self._timer.stop()

    # 每个场景：(时长秒, 绘制函数)
    def _scenes(self):
        if self.demo == 'spread':
            return [(3.4, self._sc_split),
                    (4.6, self._sc_split_rotate),
                    (3.2, self._sc_rotate)]
        if self.demo == 'panel':
            return [(5.2, self._sc_panel4),
                    (3.6, self._sc_panel2),
                    (5.2, self._sc_panel4hq)]
        if self.demo == 'manga':
            return [(4.2, self._sc_read_ltr),
                    (4.2, self._sc_read_rtl)]
        if self.demo == 'webtoon':
            return [(3.2, self._sc_webtoon_pages),
                    (5.0, self._sc_webtoon_strip)]
        if self.demo == 'crop':
            return [(2.8, self._sc_crop_none),
                    (4.2, self._sc_crop_margin),
                    (3.6, self._sc_crop_pagenum)]
        if self.demo == 'upscale':
            return [(3.0, self._sc_up_none),
                    (3.8, self._sc_up_stretch),
                    (3.8, self._sc_up_scale)]
        if self.demo == 'color':
            return [(4.0, self._sc_color_gray),
                    (2.8, self._sc_color_keep)]
        if self.demo == 'border':
            return [(3.4, self._sc_border_auto),
                    (2.6, self._sc_border_white),
                    (2.6, self._sc_border_black)]
        if self.demo == 'gamma':
            return [(2.6, self._sc_gamma_off),
                    (4.2, self._sc_gamma_on)]
        if self.demo == 'spreadshift':
            return [(4.2, self._sc_shift_off),
                    (4.2, self._sc_shift_on)]
        if self.demo == 'interpanel':
            return [(2.8, self._sc_ip_none),
                    (3.8, self._sc_ip_h),
                    (4.0, self._sc_ip_both)]
        if self.demo == 'autocontrast':
            return [(3.6, self._sc_ac_bw),
                    (2.6, self._sc_ac_off),
                    (3.6, self._sc_ac_color)]
        if self.demo == 'norotate':
            return [(3.6, self._sc_norot_off),
                    (3.2, self._sc_norot_on)]
        if self.demo == 'v4panel':
            return [(4.0, self._sc_v4_h),
                    (4.0, self._sc_v4_v)]
        if self.demo == 'strips':
            return [(2.6, self._sc_v4_strip),
                    (4.0, self._sc_v4_grid)]
        if self.demo == 'rainbow':
            return [(2.8, self._sc_rb_off),
                    (3.6, self._sc_rb_on)]
        if self.demo == 'filefusion':
            return [(2.8, self._sc_ff_off),
                    (4.2, self._sc_ff_on)]
        if self.demo == 'imgformat':
            return [(2.6, self._sc_fmt_jpeg),
                    (3.0, self._sc_fmt_png),
                    (3.2, self._sc_fmt_moz)]
        if self.demo == 'autolevel':
            return [(2.8, self._sc_al_off),
                    (4.2, self._sc_al_on)]
        if self.demo == 'chunksize':
            return [(3.0, self._sc_cs_off),
                    (4.6, self._sc_cs_on)]
        if self.demo == 'metatitle':
            return [(3.0, self._sc_mt_off),
                    (3.8, self._sc_mt_part),
                    (3.4, self._sc_mt_only)]
        if self.demo == 'noprocessing':
            return [(3.6, self._sc_np_off),
                    (3.6, self._sc_np_on)]
        if self.demo == 'deleteinput':
            return [(3.0, self._sc_del_off),
                    (4.6, self._sc_del_on)]
        if self.demo == 'outputsplit':
            return [(3.0, self._sc_os_off),
                    (4.4, self._sc_os_on)]
        if self.demo == 'rotatefirst':
            return [(3.6, self._sc_rf_off),
                    (4.4, self._sc_rf_on)]
        if self.demo == 'rotateright':
            return [(3.4, self._sc_rr_off),
                    (3.4, self._sc_rr_on)]
        if self.demo == 'smartcover':
            return [(2.8, self._sc_scc_off),
                    (5.0, self._sc_scc_on)]
        if self.demo == 'coverfill':
            return [(2.8, self._sc_cf_off),
                    (4.2, self._sc_cf_on)]
        if self.demo == 'invertdir':
            return [(3.2, self._sc_id_off),
                    (3.6, self._sc_id_on)]
        if self.demo == 'lightnovel':
            return [(3.4, self._sc_ln_off),
                    (4.2, self._sc_ln_on)]
        if self.demo == 'onepagelandscape':
            return [(3.2, self._sc_opl_off),
                    (3.6, self._sc_opl_on)]
        if self.demo == 'wallpaper':
            return [(2.6, self._sc_wp_off),
                    (5.2, self._sc_wp_on)]
        if self.demo == 'comicinfo':
            return [(3.0, self._sc_ci_off),
                    (4.2, self._sc_ci_on)]
        if self.demo == 'jpgq':
            return [(2.8, self._sc_jq_off),
                    (4.4, self._sc_jq_on)]
        if self.demo == 'noquant':
            return [(3.0, self._sc_nq_off),
                    (3.6, self._sc_nq_on)]
        if self.demo == 'webp':
            return [(2.8, self._sc_wp2_off),
                    (4.2, self._sc_wp2_on)]
        if self.demo == 'ebok':
            return [(3.0, self._sc_eb_off),
                    (4.2, self._sc_eb_on)]
        if self.demo == 'tempdir':
            return [(3.0, self._sc_td_off),
                    (3.6, self._sc_td_on)]
        if self.demo == 'pnglegacy':
            return [(2.8, self._sc_pl_off),
                    (3.6, self._sc_pl_on)]
        if self.demo == 'pngrgb':
            return [(2.8, self._sc_prgb_off),
                    (3.8, self._sc_prgb_on)]
        if self.demo == 'legacypv':
            return [(3.4, self._sc_lpv_off),
                    (4.0, self._sc_lpv_on)]
        if self.demo == 'pdfwidth':
            return [(3.0, self._sc_pdfw_off),
                    (4.0, self._sc_pdfw_on)]
        if self.demo == 'legacyextract':
            return [(3.0, self._sc_le_off),
                    (4.2, self._sc_le_on)]
        return [(5.2, self._sc_panel4),
                (3.6, self._sc_panel2),
                (5.2, self._sc_panel4hq)]

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        t = self._clock.elapsed() / 1000.0
        scenes = self._scenes()
        total = sum(s[0] for s in scenes)
        acc = 0.0
        idx, local = 0, 0.0
        for i, (dur, _) in enumerate(scenes):
            if t % total < acc + dur:
                idx, local = i, (t % total - acc) / dur
                break
            acc += dur
        # 场景开始/结束做快速淡入淡出，切换不突兀
        fade = min(_ease(local / 0.08), 1.0 - _ease((local - 0.94) / 0.06))
        p.setOpacity(max(0.0, fade))
        scenes[idx][1](p, local)
        p.setOpacity(1.0)
        self._draw_chips(p, idx)
        p.end()

    def _chips(self):
        """两态选项只显示两枚胶囊。"""
        if self.demo in ('manga', 'webtoon', 'color', 'gamma', 'spreadshift',
                         'norotate', 'v4panel', 'strips', 'rainbow', 'filefusion',
                         'autolevel', 'chunksize', 'noprocessing', 'deleteinput',
                         'outputsplit', 'rotatefirst', 'rotateright',
                         'smartcover', 'coverfill', 'invertdir', 'lightnovel',
                         'onepagelandscape', 'wallpaper', 'comicinfo',
                         'jpgq', 'noquant', 'webp', 'ebok', 'tempdir',
                         'pnglegacy', 'pngrgb', 'legacypv', 'pdfwidth',
                         'legacyextract'):
            return ('不勾选', '勾选')
        return _CHIPS

    def _draw_chips(self, p, active):
        f = p.font()
        f.setPointSizeF(9)
        p.setFont(f)
        chips = self._chips()
        w, h, gap = 64, 18, 8
        x = (self.width() - (w * len(chips) + gap * (len(chips) - 1))) / 2
        for i, name in enumerate(chips):
            r = QRectF(x + i * (w + gap), 4, w, h)
            on = i == active
            p.setPen(QPen(_ACCENT if on else QColor(200, 200, 200), 1))
            p.setBrush(_ACCENT if on else QColor(245, 245, 245))
            p.drawRoundedRect(r, 9, 9)
            p.setPen(QColor(255, 255, 255) if on else QColor(130, 130, 130))
            p.drawText(r, Qt.AlignCenter, name)

    def _caption(self, p, text, color=QColor(120, 120, 120), bold=False):
        f = p.font()
        f.setPointSizeF(10)
        f.setBold(bold)
        p.setFont(f)
        p.setPen(color)
        p.drawText(QRect(0, self.height() - 22, self.width(), 18), Qt.AlignHCenter, text)

    # ================= 跨页拆分 =================
    # 代码语义（image.py / comic2ebook.py）：
    # splitter=0 仅切割；splitter=2 切割+旋转（三页输出）；splitter=1 仅旋转

    def _sc_split(self, p, t):
        """不勾选：跨页 → 中线裁切 → 分成两页。"""
        cut = _ease((t - 0.15) / 0.22)
        sep = _ease((t - 0.45) / 0.30)
        pw, ph, gap = 122, 182, 36
        center = QPoint(self.width() // 2, (self.height() - 2) // 2)
        draw_spread(p, center, pw, ph, int(gap * sep))
        if cut > 0:
            line_x = center.x()
            glow = QColor(_ACCENT)
            glow.setAlpha(70)
            p.setPen(QPen(glow, 5, Qt.DashLine))
            p.drawLine(int(line_x), int(center.y() - ph / 2 * cut),
                       int(line_x), int(center.y() + ph / 2 * cut))
            p.setPen(QPen(_ACCENT, 1.6, Qt.DashLine))
            p.drawLine(int(line_x), int(center.y() - ph / 2 * cut),
                       int(line_x), int(center.y() + ph / 2 * cut))
        if sep > 0.6:
            self._caption(p, '切割：跨页分成两个独立页面', QColor(34, 139, 34), True)
        elif cut > 0.6:
            self._caption(p, '沿中线裁切……', _ACCENT)
        else:
            self._caption(p, '原始双页跨页')

    def _sc_split_rotate(self, p, t):
        """半勾选：先切割成两页（渐隐），再展示整页旋转版。"""
        cut = _ease(t / 0.15)
        sep = _ease((t - 0.10) / 0.20)
        fade_out = _ease((t - 0.36) / 0.12)     # 拆分后的两页渐隐
        rot_in = _ease((t - 0.46) / 0.12)       # 整页淡入
        angle = 90 * _ease((t - 0.56) / 0.28)   # 旋转动画
        center = QPoint(self.width() // 2, (self.height() - 2) // 2)
        base = p.opacity()

        # 阶段一：切割后的两页分开，随后整体渐隐
        if fade_out < 1:
            pw, ph = 122, 182
            gap = 36 * sep
            p.setOpacity(base * (1 - fade_out))
            spread = draw_spread(p, center, pw, ph, int(gap))
            if cut > 0:
                line_x = center.x()
                p.setPen(QPen(_ACCENT, 1.4, Qt.DashLine))
                p.drawLine(int(line_x), spread.top(), int(line_x), spread.bottom())
            p.setOpacity(base)

        # 阶段二：整页淡入并旋转 90°
        if rot_in > 0:
            p.setOpacity(base * rot_in)
            p.save()
            p.translate(center)
            s = 1.0 - 0.28 * _ease((t - 0.56) / 0.28)
            p.scale(s, s)
            p.rotate(angle)
            draw_spread(p, QPoint(0, 0), 122, 182, 0)
            p.restore()
            p.setOpacity(base)

        if angle >= 89:
            self._caption(p, '再额外输出一份旋转 90° 的版本', _ACCENT, True)
        elif rot_in > 0.6:
            self._caption(p, '再额外输出一份旋转 90° 的版本', _ACCENT)
        elif fade_out > 0:
            self._caption(p, '已输出两个独立页面', QColor(120, 120, 120))
        elif sep > 0.6:
            self._caption(p, '先沿中线切割成两页……')
        else:
            self._caption(p, '原始双页跨页')

    def _sc_rotate(self, p, t):
        """勾选：整页旋转 90°，不切割。"""
        angle = 90 * _ease((t - 0.2) / 0.45)
        pw, ph = 122, 182
        center = QPoint(self.width() // 2, (self.height() - 2) // 2)
        p.save()
        p.translate(center)
        # 旋转过程中略微缩小，保证不出画布
        s = 1.0 - 0.28 * _ease((t - 0.2) / 0.45)
        p.scale(s, s)
        p.rotate(angle)
        draw_spread(p, QPoint(0, 0), pw, ph, 0)
        p.restore()
        # 旋转方向箭头
        if 0 < angle < 90:
            self._caption(p, '旋转中……', _ACCENT)
        elif angle >= 89:
            self._caption(p, '整页旋转 90°，不切割', QColor(34, 139, 34), True)
        else:
            self._caption(p, '原始双页跨页')

    # ================= 面板视图 =================
    # 代码语义：默认 4 面板（逐格放大四个角）；
    # autoscale（半勾选）= 2 面板（上下两半）；hq（勾选）= 4 高清面板

    def _page_rect(self):
        return QRectF((self.width() - 144) / 2, 32, 144, 216)

    def _quad_frames(self, page):
        inner = page.adjusted(6, 6, -6, -6)
        w = (inner.width() - 4) / 2
        h = (inner.height() - 4) / 2
        return [QRectF(inner.left(), inner.top(), w, h),
                QRectF(inner.left() + w + 4, inner.top(), w, h),
                QRectF(inner.left(), inner.top() + h + 4, w, h),
                QRectF(inner.left() + w + 4, inner.top() + h + 4, w, h)]

    def _half_frames(self, page):
        inner = page.adjusted(6, 6, -6, -6)
        h = (inner.height() - 4) / 2
        return [QRectF(inner.left(), inner.top(), inner.width(), h),
                QRectF(inner.left(), inner.top() + h + 4, inner.width(), h)]

    def _panel_scene(self, p, t, frames, captions, hq=False):
        page = self._page_rect()
        draw_manga_page(p, page.toRect(), variant=2)
        seq = [page] + frames           # 取景框：整页 → 逐格
        seg = 1.0 / len(seq)
        idx = min(int(t / seg), len(seq) - 1)
        local = (t - idx * seg) / seg
        move = _ease(local / 0.5)
        prev = seq[idx - 1] if idx > 0 else seq[0]
        cur = seq[idx]
        cam = QRectF(prev.left() + (cur.left() - prev.left()) * move,
                     prev.top() + (cur.top() - prev.top()) * move,
                     prev.width() + (cur.width() - prev.width()) * move,
                     prev.height() + (cur.height() - prev.height()) * move)
        # 取景框外压暗
        path = QPainterPath()
        path.addRect(QRectF(self.rect()))
        path.addRoundedRect(cam, 4, 4)
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(30, 30, 30, 110))
        p.drawPath(path)
        p.setBrush(Qt.NoBrush)
        p.setPen(QPen(QColor(255, 255, 255, 220), 4))
        p.drawRoundedRect(cam, 4, 4)
        p.setPen(QPen(_ACCENT, 2))
        p.drawRoundedRect(cam, 4, 4)
        if hq and idx > 0:
            # 高清面板：取景框右上角 HQ 徽标
            badge = QRectF(cam.right() - 26, cam.top() - 8, 26, 14)
            p.setPen(Qt.NoPen)
            p.setBrush(_ACCENT)
            p.drawRoundedRect(badge, 7, 7)
            f = p.font()
            f.setPointSizeF(8)
            f.setBold(True)
            p.setFont(f)
            p.setPen(QColor(255, 255, 255))
            p.drawText(badge, Qt.AlignCenter, 'HQ')
        self._caption(p, captions[idx], _ACCENT if idx > 0 else QColor(120, 120, 120),
                      bold=idx > 0)

    def _sc_panel4(self, p, t):
        """不勾选：4 面板，逐格放大四个角。"""
        self._panel_scene(p, t, self._quad_frames(self._page_rect()),
                          ['整页', '第 1 格（左上）', '第 2 格（右上）',
                           '第 3 格（左下）', '第 4 格（右下）'])

    def _sc_panel2(self, p, t):
        """半勾选：2 面板，只放大上下两半。"""
        self._panel_scene(p, t, self._half_frames(self._page_rect()),
                          ['整页', '上半部分', '下半部分'])

    def _sc_panel4hq(self, p, t):
        """勾选：4 高清面板（更高质量的放大）。"""
        self._panel_scene(p, t, self._quad_frames(self._page_rect()),
                          ['整页', '第 1 格 · 高清', '第 2 格 · 高清',
                           '第 3 格 · 高清', '第 4 格 · 高清'], hq=True)

    # ================= 从右向左 =================
    # 代码语义：righttoleft=True 时页面与分格按日漫顺序（右→左）排列

    def _read_scene(self, p, t, rtl):
        pw, ph, gap = 122, 182, 8
        center = QPoint(self.width() // 2, (self.height() - 2) // 2 - 6)
        spread = draw_spread(p, center, pw, ph, gap)
        left = QRect(spread.left(), spread.top(), pw, ph)
        right = QRect(spread.left() + pw + gap, spread.top(), pw, ph)

        def top_c(r):
            return QPoint(int(r.center().x()), int(r.top() + ph * 0.28))

        def bot_c(r):
            return QPoint(int(r.center().x()), int(r.top() + ph * 0.72))

        if rtl:
            order = [top_c(right), bot_c(right), top_c(left), bot_c(left)]
        else:
            order = [top_c(left), bot_c(left), top_c(right), bot_c(right)]
        # 顺序徽标依次浮现
        self._order_badges(p, t, order)
        # 方向箭头
        ay = spread.bottom() + 16
        x0, x1 = spread.left() + 10, spread.right() - 10
        p.setPen(QPen(_ACCENT, 2))
        p.drawLine(x0, ay, x1, ay)
        ex = x0 if rtl else x1
        d = -1 if rtl else 1
        p.drawLine(ex, ay, ex - 8 * d, ay - 5)
        p.drawLine(ex, ay, ex - 8 * d, ay + 5)

    def _sc_read_ltr(self, p, t):
        """不勾选：从左向右阅读。"""
        self._read_scene(p, t, rtl=False)
        if t < 0.15:
            self._caption(p, '双页漫画的阅读顺序')
        else:
            self._caption(p, '从左向右阅读（西式漫画）', _ACCENT, True)

    def _sc_read_rtl(self, p, t):
        """勾选：从右向左阅读。"""
        self._read_scene(p, t, rtl=True)
        if t < 0.15:
            self._caption(p, '双页漫画的阅读顺序')
        else:
            self._caption(p, '从右向左阅读（日式漫画）', QColor(34, 139, 34), True)

    # ================= 条漫模式 =================
    # 代码语义（comic2ebook.py → comic2panel.py）：
    # 先把多页垂直拼接为一整张长条，再在两格之间的空白处下刀，
    # 按设备屏幕高度重切成一屏一屏的虚拟页（绝不切分格子）

    _WT_PW, _WT_PH = 100, 96      # 源页面尺寸（正常竖版比例）
    _WT_S0 = 0.56                 # 长条阶段整体等比缩小展示（只缩小，不压扁）

    def _wt_strip_rect(self, i, gap, scale):
        """第 i 页在长条（等比缩小展示）中的位置。"""
        w, h = self._WT_PW * scale, self._WT_PH * scale
        g = gap * scale
        x = (self.width() - w) / 2
        total = h * 4 + g * 3
        y0 = 26 + (232 - total) / 2
        return QRectF(x, y0 + i * (h + g), w, h)

    def _wt_page_rect(self, i):
        """第 i 页在成品（两屏并排、正常页面大小）中的位置。"""
        w, h = self._WT_PW, self._WT_PH
        gapx = 30
        x0 = (self.width() - (w * 2 + gapx)) / 2
        y0 = 26 + (232 - h * 2) / 2
        if i < 2:
            return QRectF(x0, y0 + i * h, w, h)
        return QRectF(x0 + w + gapx, y0 + (i - 2) * h, w, h)

    @staticmethod
    def _lerp_rect(a, b, k):
        return QRectF(a.left() + (b.left() - a.left()) * k,
                      a.top() + (b.top() - a.top()) * k,
                      a.width() + (b.width() - a.width()) * k,
                      a.height() + (b.height() - a.height()) * k)

    def _sc_webtoon_pages(self, p, t):
        """不勾选：逐页独立（2x2 排开）。"""
        w, h = self._WT_PW * 0.85, self._WT_PH * 0.85
        gap = 14
        x0 = (self.width() - (w * 2 + gap)) / 2
        y0 = 26 + (232 - (h * 2 + gap)) / 2
        for i in range(4):
            r = QRectF(x0 + (i % 2) * (w + gap), y0 + (i // 2) * (h + gap), w, h)
            draw_manga_page(p, r.toRect(), variant=i % 3)
        self._caption(p, '逐页独立处理，页与页分开')

    def _sc_webtoon_strip(self, p, t):
        """勾选：拼接为长条，再按屏幕高度沿格子间隙重切。"""
        merge = _ease(t / 0.2)              # 阶段1：页缝闭合，拼成长条
        cut = _ease((t - 0.32) / 0.14)      # 阶段2：切割线出现
        k = _ease((t - 0.54) / 0.3)         # 阶段3：分成两屏并恢复正常页面大小
        gap = 8 * (1 - merge)
        for i in range(4):
            r = self._lerp_rect(self._wt_strip_rect(i, gap, self._WT_S0),
                                self._wt_page_rect(i), k)
            draw_manga_page(p, r.toRect(), variant=i % 3)
            # 接缝处的页边框随拼接淡去，呈现无缝效果；切开后恢复
            fade = merge * (1 - k)
            if fade > 0:
                ov = QColor(255, 255, 255)
                ov.setAlpha(int(255 * fade))
                p.setPen(Qt.NoPen)
                p.setBrush(ov)
                if i > 0:
                    p.drawRect(QRectF(r.left(), r.top() - 1, r.width(), 3))
                if i < 3:
                    p.drawRect(QRectF(r.left(), r.bottom() - 2, r.width(), 3))
        # 切割线：落在中间两格之间的空白处（屏幕高度的整数倍位置）
        if cut > 0 and k < 1:
            a = self._lerp_rect(self._wt_strip_rect(1, gap, self._WT_S0),
                                self._wt_page_rect(1), k)
            b = self._lerp_rect(self._wt_strip_rect(2, gap, self._WT_S0),
                                self._wt_page_rect(2), k)
            seam_y = (a.bottom() + b.top()) / 2
            c = QColor(_ACCENT)
            c.setAlpha(int(255 * cut * (1 - k)))
            p.setPen(QPen(c, 2, Qt.DashLine))
            p.setBrush(Qt.NoBrush)
            p.drawLine(QPointF(a.left() - 14, seam_y),
                       QPointF(a.right() + 14, seam_y))
        # 两屏的外框：表示「一屏」的成品页
        if k > 0:
            c = QColor(34, 139, 34)
            c.setAlpha(int(255 * k))
            p.setPen(QPen(c, 2))
            p.setBrush(Qt.NoBrush)
            top = self._wt_page_rect(0).united(self._wt_page_rect(1)).adjusted(-6, -6, 6, 6)
            bottom = self._wt_page_rect(2).united(self._wt_page_rect(3)).adjusted(-6, -6, 6, 6)
            p.drawRoundedRect(top, 5, 5)
            p.drawRoundedRect(bottom, 5, 5)
        if t < 0.28:
            self._caption(p, '先垂直拼接为无缝长条……', _ACCENT)
        elif t < 0.52:
            self._caption(p, '在格子间隙的空白处定位切割线', _ACCENT)
        elif k < 1:
            self._caption(p, '按屏幕高度切开……', _ACCENT)
        else:
            self._caption(p, '切成一屏一屏，格子保持完整', QColor(34, 139, 34), True)

    # ================= 裁剪模式 =================
    # 代码语义（image.py / KCC_gui.py）：
    # cropping=0 不裁剪；cropping=1（半勾选）cropMargin 裁四周白边；
    # cropping=2（勾选）cropPageNumber 仅裁页码（单边不超过 10%）

    _CROP_MARGIN = 22

    def _draw_crop_page(self, p, t, cut=0.0, num_alpha=1.0, num_glow=False):
        outer = self._page_rect()
        m = self._CROP_MARGIN
        cm = m * cut
        page = outer.adjusted(cm, cm, -cm, -cm)
        inner_m = m - cm
        content = page.adjusted(inner_m, inner_m, -inner_m, -inner_m)
        p.setPen(QPen(QColor(176, 176, 176), 1))
        p.setBrush(QColor(253, 253, 251))
        p.drawRoundedRect(page, 2, 2)
        _panel_art(p, content.toRect(), 0)
        # 页码位于底部白边内、靠右对齐
        nr = QRectF(content.right() - 24,
                    content.bottom() + (inner_m - 12) / 2, 24, 12)
        if num_glow:
            p.setPen(QPen(_ACCENT, 1.4, Qt.DashLine))
            p.setBrush(Qt.NoBrush)
            p.drawRect(nr.adjusted(-3, -2, 3, 2))
        if num_alpha > 0:
            c = QColor(120, 120, 120)
            c.setAlpha(int(255 * num_alpha))
            f = p.font()
            f.setPointSizeF(8)
            p.setFont(f)
            p.setPen(c)
            p.drawText(nr, Qt.AlignCenter, '27')
        return outer, page

    def _sc_crop_none(self, p, t):
        """不勾选：不裁剪。"""
        self._draw_crop_page(p, t)
        self._caption(p, '不裁剪，保留原始页面边缘')

    def _sc_crop_margin(self, p, t):
        """半勾选：裁切四周白边。"""
        cut = _ease((t - 0.25) / 0.45)
        # 页码随白边一起被裁掉
        outer, _ = self._draw_crop_page(p, t, cut=cut, num_alpha=1 - cut)
        if cut < 1:
            # 目标裁剪线（画面内容边缘）
            m = self._CROP_MARGIN
            target = outer.adjusted(m, m, -m, -m)
            p.setPen(QPen(_ACCENT, 1.4, Qt.DashLine))
            p.setBrush(Qt.NoBrush)
            p.drawRect(target)
        if cut >= 1:
            self._caption(p, '裁切四周白边，只保留画面', QColor(34, 139, 34), True)
        elif cut > 0:
            self._caption(p, '沿画面边缘裁切……', _ACCENT)
        else:
            self._caption(p, '识别四周白边……')

    def _sc_crop_pagenum(self, p, t):
        """勾选：以页码和画面为边界，裁掉边界之外的外围边缘（页码保留）。"""
        # 对应 cropPageNumber：bbox 包含画面与页码，各边裁切不超过 10%
        final = 0.45                      # 白边裁掉的比例（保留含页码的一圈窄边）
        cut = final * _ease((t - 0.3) / 0.4)
        outer, _ = self._draw_crop_page(p, t, cut=cut,
                                        num_glow=0.08 < t < 0.4)
        if 0.12 < t < 0.9:
            # 目标裁剪框：画面 + 页码都在框内
            m = self._CROP_MARGIN
            target = outer.adjusted(m * final, m * final,
                                    -m * final, -m * final)
            a = QColor(_ACCENT)
            a.setAlpha(120 if cut >= final else 255)
            p.setPen(QPen(a, 1.4, Qt.DashLine))
            p.setBrush(Qt.NoBrush)
            p.drawRect(target)
        if cut >= final:
            self._caption(p, '以页码和画面为界，裁掉外围边缘', QColor(34, 139, 34), True)
        elif cut > 0:
            self._caption(p, '裁掉边界之外的部分……', _ACCENT)
        else:
            self._caption(p, '定位页码与画面边界……')

    # ================= 拉伸 / 放大 =================
    # 代码语义（image.py resizeImage）：
    # 不勾选：小图不放大，保持原始尺寸；半勾选 stretch：强制 resize 到设备
    # 分辨率（可能变形）；勾选 upscale：等比放大至适配屏幕（不变形）

    def _device_frame(self):
        return QRectF((self.width() - 168) / 2, 24, 168, 232)

    def _up_scene(self, p, t, mode):
        frame = self._device_frame()
        p.setPen(QPen(QColor(90, 90, 90), 3))
        p.setBrush(QColor(250, 250, 250))
        p.drawRoundedRect(frame, 8, 8)
        screen = frame.adjusted(5, 5, -5, -5)
        sw, sh = 76.0, 128.0        # 原始小图（三个场景保持一致）
        e = _ease((t - 0.15) / 0.4)
        if mode == 'stretch':
            dw = sw + (screen.width() - sw) * e
            dh = sh + (screen.height() - sh) * e
        elif mode == 'scale':
            k = 1 + (min(screen.width() / sw, screen.height() / sh) - 1) * e
            dw, dh = sw * k, sh * k
        else:
            dw, dh = sw, sh
        rect = QRectF(screen.center().x() - dw / 2,
                      screen.center().y() - dh / 2, dw, dh)
        p.save()
        p.setClipRect(screen)
        draw_manga_page(p, rect.toRect(), variant=0)
        p.restore()
        return e

    def _sc_up_none(self, p, t):
        """不勾选：小图保持原尺寸。"""
        self._up_scene(p, t, 'none')
        self._caption(p, '小图保持原始尺寸，不放大')

    def _sc_up_stretch(self, p, t):
        """半勾选：强制拉伸铺满。"""
        e = self._up_scene(p, t, 'stretch')
        if e >= 1:
            self._caption(p, '强制拉伸铺满屏幕，可能变形', QColor(34, 139, 34), True)
        elif e > 0:
            self._caption(p, '拉伸至设备分辨率……', _ACCENT)
        else:
            self._caption(p, '原始小图')

    def _sc_up_scale(self, p, t):
        """勾选：等比放大适配。"""
        e = self._up_scene(p, t, 'scale')
        if e >= 1:
            self._caption(p, '等比放大至适配屏幕，不变形', QColor(34, 139, 34), True)
        elif e > 0:
            self._caption(p, '等比放大中……', _ACCENT)
        else:
            self._caption(p, '原始小图')

    # ================= 彩色模式 =================
    # 代码语义：forcecolor=True 保留彩色；默认转为灰度以适配电子墨水屏

    def _sc_color_gray(self, p, t):
        """不勾选：彩色页面转为灰度。"""
        r = self._page_rect().toRect()
        gray = _page_image(r.width(), r.height(), 0, True)
        col = _page_image(r.width(), r.height(), 0, False)
        mix = _ease((t - 0.1) / 0.35)
        p.drawImage(r.topLeft(), gray)
        if mix < 1:
            p.save()
            p.setOpacity(1 - mix)
            p.drawImage(r.topLeft(), col)
            p.restore()
        if mix >= 1:
            self._caption(p, '转换为灰度，适配电子墨水屏', QColor(34, 139, 34), True)
        elif mix > 0:
            self._caption(p, '灰度化处理中……', _ACCENT)
        else:
            self._caption(p, '原始彩色页面')

    def _sc_color_keep(self, p, t):
        """勾选：保留彩色。"""
        r = self._page_rect().toRect()
        p.drawImage(r.topLeft(), _page_image(r.width(), r.height(), 0, False))
        self._caption(p, '保留原始彩色（适合彩屏设备）', QColor(34, 139, 34), True)

    # ================= 黑/白边距 =================
    # 代码语义（KCC_gui.py / image.py fill）：不勾选=自动检测页面背景色填充；
    # 半勾选=white_borders 白色边距；勾选=black_borders 黑色边距

    def _border_scene(self, p, t, bar_color, caption,
                      cap_color=QColor(120, 120, 120), bold=False):
        frame = self._device_frame()
        screen = frame.adjusted(5, 5, -5, -5)
        p.setPen(Qt.NoPen)
        p.setBrush(bar_color)
        p.drawRect(screen)
        pw, ph = 112.0, screen.height() - 12    # 竖版页面，左右留边距
        page = QRectF(screen.center().x() - pw / 2, screen.top() + 6, pw, ph)
        draw_manga_page(p, page.toRect(), variant=0)
        p.setPen(QPen(QColor(90, 90, 90), 3))
        p.setBrush(Qt.NoBrush)
        p.drawRoundedRect(frame, 8, 8)
        self._caption(p, caption, cap_color, bold)

    def _sc_border_auto(self, p, t):
        """不勾选：自动检测填充色。"""
        k = _ease(t / 0.5)
        bar = _mix(QColor(170, 170, 170), QColor(250, 250, 246), k)
        if k >= 1:
            self._border_scene(p, t, bar, '自动检测：边距跟随页面背景色',
                               QColor(34, 139, 34), True)
        else:
            self._border_scene(p, t, bar, '检测页面背景色……')

    def _sc_border_white(self, p, t):
        """半勾选：白色边距。"""
        self._border_scene(p, t, QColor(255, 255, 255),
                           '边距统一填充为白色', _ACCENT, True)

    def _sc_border_black(self, p, t):
        """勾选：黑色边距。"""
        self._border_scene(p, t, QColor(18, 18, 18),
                           '边距统一填充为黑色', QColor(34, 139, 34), True)

    # ================= 自定义伽马 =================
    # 代码语义（image.py gammaCorrectImage）：255*(a/255)^gamma，
    # gamma>1 中间调压暗，<1 提亮

    def _sc_gamma_off(self, p, t):
        """不勾选：不做伽马校正。"""
        r = self._page_rect().toRect()
        p.drawImage(r.topLeft(), _page_image(r.width(), r.height(), 0, False))
        self._caption(p, '不校正，保持原始明暗')

    def _sc_gamma_on(self, p, t):
        """勾选：按伽马值压暗中间调（以 1.8 为例）。"""
        r = self._page_rect().toRect()
        p.drawImage(r.topLeft(), _page_image(r.width(), r.height(), 0, False))
        k = _ease((t - 0.1) / 0.4)
        if k > 0:
            ov = QColor(20, 20, 40)
            ov.setAlpha(int(95 * k))           # 模拟中间调压暗
            p.setPen(Qt.NoPen)
            p.setBrush(ov)
            p.drawRect(r)
        # 迷你伽马曲线：从直线 y=x 渐变为 y=x^1.8
        gx, gy, gs = r.right() - 56, r.top() + 10, 46
        p.setPen(QPen(QColor(120, 120, 120), 1))
        p.setBrush(QColor(255, 255, 255, 220))
        p.drawRect(gx, gy, gs, gs)
        p.setPen(QPen(_ACCENT, 1.6))
        g = 1.0 + 0.8 * k
        prev = None
        for i in range(21):
            x = gx + i * gs / 20
            y = gy + gs - pow(i / 20, g) * gs
            if prev is not None:
                p.drawLine(int(prev[0]), int(prev[1]), int(x), int(y))
            prev = (x, y)
        if k >= 1:
            self._caption(p, '伽马 > 1：中间调压暗，画面更通透', QColor(34, 139, 34), True)
        elif k > 0:
            self._caption(p, '应用伽马校正中……', _ACCENT)
        else:
            self._caption(p, '原始画面')

    # ================= 跨页偏移 =================
    # 代码语义（KCC_gui.py 扫描配对）：spreadshift 把配对起点后移一页，
    # 让被封面错开的双页跨页正确拼合

    def _shift_scene(self, p, t, shift):
        w, h, gap = 56, 84, 10
        total = 5 * w + 4 * gap
        x0 = (self.width() - total) / 2
        y = 56
        halves = (1, 2)                          # 第 2、3 页是同一跨页的两半
        pairs = [(1, 2), (3, 4)] if shift else [(0, 1), (2, 3)]
        for i in range(5):
            r = QRect(int(x0 + i * (w + gap)), y, w, h)
            draw_manga_page(p, r, variant=i % 3)
            if i in halves:
                p.setPen(Qt.NoPen)
                p.setBrush(QColor(_ACCENT.red(), _ACCENT.green(), _ACCENT.blue(), 46))
                p.drawRect(r)
            f = p.font()
            f.setPointSizeF(8)
            p.setFont(f)
            p.setPen(QColor(120, 120, 120))
            p.drawText(QRect(r.left(), r.bottom() + 3, w, 14),
                       Qt.AlignHCenter, str(i + 1))
        # 配对括号淡入
        a = _ease((t - 0.2) / 0.2)
        if a > 0:
            p.save()
            p.setOpacity(a)
            p.setPen(QPen(_ACCENT, 2))
            p.setBrush(Qt.NoBrush)
            for i, j in pairs:
                r = QRectF(x0 + i * (w + gap) - 4, y - 6,
                           (j - i) * (w + gap) + w + 8, h + 12)
                p.drawRoundedRect(r, 6, 6)
            p.restore()
        # 跨页两半之间的连线：同组=绿，不同组=红虚线
        link = _ease((t - 0.5) / 0.15)
        if link > 0:
            same = (1, 2) in pairs
            c = QColor(34, 139, 34) if same else QColor(210, 60, 60)
            c.setAlpha(int(255 * link))
            p.setPen(QPen(c, 2, Qt.SolidLine if same else Qt.DashLine))
            cx1 = x0 + 1 * (w + gap) + w / 2
            cx2 = x0 + 2 * (w + gap) + w / 2
            ly = y - 14
            p.drawLine(int(cx1), ly, int(cx2), ly)
        return (1, 2) in pairs and _ease((t - 0.5) / 0.15) >= 1

    def _sc_shift_off(self, p, t):
        """不勾选：从第 1 页起两两配对，跨页两半错位。"""
        done = self._shift_scene(p, t, shift=False)
        if done:
            self._caption(p, '跨页两半被分到不同组合，拼版错位', QColor(210, 60, 60), True)
        else:
            self._caption(p, '从第 1 页起两两配对……')

    def _sc_shift_on(self, p, t):
        """勾选：配对起点后移一页，跨页正确拼合。"""
        done = self._shift_scene(p, t, shift=True)
        if done:
            self._caption(p, '整体后移一页，跨页两半正确拼合', QColor(34, 139, 34), True)
        else:
            self._caption(p, '跳过封面，从第 2 页起配对……')

    # ================= 面板间裁剪 =================
    # 代码语义（image.py cropInterPanelEmptySections）：
    # interpanelcrop=1（半勾选）裁横向空白带；=2（勾选）横向+纵向都裁

    def _interpanel_scene(self, p, t, mode):
        page = self._page_rect()
        p.setPen(QPen(QColor(176, 176, 176), 1))
        p.setBrush(QColor(253, 253, 251))
        p.drawRoundedRect(page, 2, 2)
        inner = page.adjusted(10, 10, -10, -10)
        e = _ease((t - 0.2) / 0.45)
        gx = gy = 24.0
        if mode == 'h':
            gy = 24 - 18 * e
        elif mode == 'both':
            gx = gy = 24 - 18 * e
        cw = (inner.width() - gx) / 2
        ch = (inner.height() - gy) / 2
        kinds = (0, 1, 2, 3)
        for idx in range(4):
            r, c = divmod(idx, 2)
            cell = QRectF(inner.left() + c * (cw + gx),
                          inner.top() + r * (ch + gy), cw, ch)
            _panel_art(p, cell.toRect(), kinds[idx])
        return e

    def _sc_ip_none(self, p, t):
        """不勾选：保留空白间隔。"""
        self._interpanel_scene(p, t, 'none')
        self._caption(p, '保留分格之间的空白间隔')

    def _sc_ip_h(self, p, t):
        """半勾选：裁掉横向空白带。"""
        e = self._interpanel_scene(p, t, 'h')
        if e >= 1:
            self._caption(p, '裁掉横向空白带，分格上下靠拢', QColor(34, 139, 34), True)
        elif e > 0:
            self._caption(p, '裁掉横向空白带……', _ACCENT)
        else:
            self._caption(p, '原始分格间隔')

    def _sc_ip_both(self, p, t):
        """勾选：横向+纵向都裁。"""
        e = self._interpanel_scene(p, t, 'both')
        if e >= 1:
            self._caption(p, '横向和纵向空白带全部裁掉', QColor(34, 139, 34), True)
        elif e > 0:
            self._caption(p, '横竖空白带一起裁掉……', _ACCENT)
        else:
            self._caption(p, '原始分格间隔')

    # ================= 自定义自动对比度 =================
    # 代码语义（image.py autocontrastImage）：默认仅黑白页增强；
    # 半勾选 noautocontrast 禁用；勾选 colorautocontrast 彩色页也增强

    def _contrast_scene(self, p, t, lo0, hi0, lo1, hi1):
        page = self._page_rect()
        p.setPen(QPen(QColor(176, 176, 176), 1))
        p.setBrush(QColor(253, 253, 251))
        p.drawRoundedRect(page, 2, 2)
        inner = page.adjusted(10, 10, -10, -10)
        e = _ease((t - 0.15) / 0.4)
        lo = _mix(lo0, lo1, e)
        hi = _mix(hi0, hi1, e)
        grad = QLinearGradient(inner.topLeft(), inner.bottomLeft())
        grad.setColorAt(0, hi)
        grad.setColorAt(1, lo)
        p.setPen(Qt.NoPen)
        p.setBrush(grad)
        p.drawRect(inner)
        return e

    def _sc_ac_bw(self, p, t):
        """不勾选：黑白页面自动增强对比度（默认）。"""
        e = self._contrast_scene(p, t, QColor(140, 140, 140), QColor(195, 195, 195),
                                 QColor(45, 45, 45), QColor(245, 245, 245))
        if e >= 1:
            self._caption(p, '黑白页面自动增强对比度（默认）', QColor(34, 139, 34), True)
        elif e > 0:
            self._caption(p, '拉伸明暗范围……', _ACCENT)
        else:
            self._caption(p, '低对比度的原始页面')

    def _sc_ac_off(self, p, t):
        """半勾选：禁用自动对比度。"""
        self._contrast_scene(p, t, QColor(140, 140, 140), QColor(195, 195, 195),
                             QColor(140, 140, 140), QColor(195, 195, 195))
        self._caption(p, '禁用对比度增强，画面保持原样', _ACCENT, True)

    def _sc_ac_color(self, p, t):
        """勾选：彩色页面也增强对比度。"""
        e = self._contrast_scene(p, t, QColor(120, 132, 148), QColor(198, 203, 212),
                                 QColor(38, 76, 168), QColor(240, 248, 255))
        if e >= 1:
            self._caption(p, '彩色页面同样增强对比度', QColor(34, 139, 34), True)
        elif e > 0:
            self._caption(p, '增强彩色画面对比度……', _ACCENT)
        else:
            self._caption(p, '低对比度的彩色页面')

    # ================= 不旋转 =================
    # 代码语义（image.py / KCC_gui.py）：norotate 时跨页拆分不再旋转双页
    # 跨页（横版专属演示）

    def _sc_norot_off(self, p, t):
        """不勾选：双页跨页可旋转（默认）。"""
        angle = 90 * _ease((t - 0.2) / 0.45)
        center = QPoint(self.width() // 2, (self.height() - 2) // 2)
        p.save()
        p.translate(center)
        s = 1.0 - 0.28 * _ease((t - 0.2) / 0.45)
        p.scale(s, s)
        p.rotate(angle)
        draw_spread(p, QPoint(0, 0), 122, 182, 0)
        p.restore()
        if angle >= 89:
            self._caption(p, '默认：双页跨页可被旋转', QColor(34, 139, 34), True)
        elif angle > 0:
            self._caption(p, '旋转中……', _ACCENT)
        else:
            self._caption(p, '横向双页跨页')

    def _sc_norot_on(self, p, t):
        """勾选：锁定方向，不旋转。"""
        center = QPoint(self.width() // 2, (self.height() - 2) // 2)
        draw_spread(p, center, 122, 182, 0)
        a = _ease((t - 0.3) / 0.2)
        if a > 0:
            # 禁止符号盖在旋转箭头上
            cx, cy, r = center.x() + 128, center.y() - 86, 22
            p.setPen(QPen(QColor(150, 150, 150), 2))
            p.drawArc(cx - 13, cy - 13, 26, 26, 30 * 16, 300 * 16)
            c = QColor(210, 60, 60)
            c.setAlpha(int(255 * a))
            p.setPen(QPen(c, 3))
            p.setBrush(Qt.NoBrush)
            p.drawEllipse(QPoint(cx, cy), r, r)
            p.drawLine(int(cx - r * 0.7), int(cy + r * 0.7),
                       int(cx + r * 0.7), int(cy - r * 0.7))
        if a >= 1:
            self._caption(p, '锁定方向：双页跨页不旋转', QColor(34, 139, 34), True)
        else:
            self._caption(p, '横向双页跨页')

    # ================= 纵向 4 面板 =================
    # 代码语义（comic2ebook.py buildOPF + 面板视图）：vertical4panel 决定
    # 4 面板放大的阅读顺序——不勾选（横向）先顶部两格（左上→右上→左下→右下）；
    # 勾选（纵向）先两侧格（左上→左下→右上→右下，竖排顺序）

    def _order_badges(self, p, t, pts):
        """在 pts 位置依次浮现蓝色序号徽标。"""
        for i, c in enumerate(pts):
            a = _ease((t - (0.15 + i * 0.16)) / 0.08)
            if a <= 0:
                continue
            p.save()
            p.setOpacity(a)
            p.setPen(Qt.NoPen)
            p.setBrush(_ACCENT)
            r = 13
            p.drawEllipse(c, r, r)
            f = p.font()
            f.setPointSizeF(11)
            f.setBold(True)
            p.setFont(f)
            p.setPen(QColor(255, 255, 255))
            p.drawText(QRect(c.x() - r, c.y() - r, r * 2, r * 2),
                       Qt.AlignCenter, str(i + 1))
            p.restore()

    def _v4_order_scene(self, p, t, vertical):
        page = self._page_rect()
        draw_manga_page(p, page.toRect(), variant=2)
        quads = self._quad_frames(page)          # 0=左上 1=右上 2=左下 3=右下
        order = [0, 2, 1, 3] if vertical else [0, 1, 2, 3]
        pts = [QPoint(int(quads[i].center().x()), int(quads[i].center().y()))
               for i in order]
        self._order_badges(p, t, pts)

    def _sc_v4_h(self, p, t):
        """不勾选（横向）：先放大顶部两格。"""
        self._v4_order_scene(p, t, vertical=False)
        if t < 0.15:
            self._caption(p, '4 面板的放大顺序')
        else:
            self._caption(p, '横向：先放大顶部两格（左 → 右）', _ACCENT, True)

    def _sc_v4_v(self, p, t):
        """勾选（纵向）：先放大两侧格。"""
        self._v4_order_scene(p, t, vertical=True)
        if t < 0.15:
            self._caption(p, '4 面板的放大顺序')
        else:
            self._caption(p, '纵向：先放大两侧格（竖排顺序）', QColor(34, 139, 34), True)

    # ================= 1x4 转 2x2 条带 =================
    # 代码语义（maximizestrips）：1x4 竖条重排为 2x2，充分利用屏幕

    _V4_W, _V4_H, _V4_GAP = 88, 54, 4

    def _v4_start(self, i):
        total = 4 * self._V4_H + 3 * self._V4_GAP
        x = (self.width() - self._V4_W) / 2
        y = (self.height() - 22 - total) / 2 + 6
        return (x, y + i * (self._V4_H + self._V4_GAP), self._V4_W, self._V4_H)

    def _sc_v4_strip(self, p, t):
        """不勾选：保持 1x4 条带。"""
        for i in range(4):
            x, y, w, h = self._v4_start(i)
            _panel_art(p, QRectF(x, y, w, h).toRect(), i % 4)
        self._caption(p, '保持 1x4 条带，逐格向下阅读')

    def _sc_v4_grid(self, p, t):
        """勾选：重排为 2x2。"""
        e = _ease((t - 0.15) / 0.45)
        gw, gh, ggap = 118, 88, 8
        gx0 = (self.width() - (2 * gw + ggap)) / 2
        gy0 = (self.height() - 22 - (2 * gh + ggap)) / 2 + 6
        for i in range(4):
            sx, sy, sw, sh = self._v4_start(i)
            r_, c_ = divmod(i, 2)
            tx = gx0 + c_ * (gw + ggap)
            ty = gy0 + r_ * (gh + ggap)
            rect = QRectF(sx + (tx - sx) * e, sy + (ty - sy) * e,
                          sw + (gw - sw) * e, sh + (gh - sh) * e)
            _panel_art(p, rect.toRect(), i % 4)
        if e >= 1:
            self._caption(p, '重排为 2x2，充分利用屏幕', QColor(34, 139, 34), True)
        elif e > 0:
            self._caption(p, '1x4 → 2x2 重排中……', _ACCENT)
        else:
            self._caption(p, '原始 1x4 条带')

    # ================= 彩虹纹消除 =================
    # 代码语义（image.py optimizeForDisplay）：eraserainbow 通过衰减
    # 干扰频率消除彩色墨水屏上的彩虹纹

    def _rainbow_overlay(self, p, r, alpha):
        p.save()
        p.setClipRect(r)
        for i in range(0, r.height(), 3):
            band = (i // 3) % 3
            col = [(235, 60, 60), (60, 190, 60), (60, 110, 235)][band]
            p.setPen(QPen(QColor(*col, alpha), 1))
            off = (i % 7) - 3
            p.drawLine(r.left(), r.top() + i, r.right(), r.top() + i + off)
        p.restore()

    def _sc_rb_off(self, p, t):
        """不勾选：彩色墨水屏上的彩虹纹。"""
        r = self._page_rect().toRect()
        p.drawImage(r.topLeft(), _page_image(r.width(), r.height(), 0, False))
        self._rainbow_overlay(p, r, 90)
        self._caption(p, '彩色墨水屏上可能出现彩虹纹')

    def _sc_rb_on(self, p, t):
        """勾选：彩虹纹消除。"""
        r = self._page_rect().toRect()
        p.drawImage(r.topLeft(), _page_image(r.width(), r.height(), 0, False))
        k = _ease((t - 0.15) / 0.4)
        if k < 1:
            self._rainbow_overlay(p, r, int(90 * (1 - k)))
        if k >= 1:
            self._caption(p, '衰减干扰频率，彩虹纹消除', QColor(34, 139, 34), True)
        else:
            self._caption(p, '滤除彩虹纹中……', _ACCENT)

    # ================= 文件合并 =================
    # 代码语义（comic2ebook.py filefusion）：所有选中文件合并为单个输出

    def _fusion_scene(self, p, t, merge):
        w, h = 64, 96
        xs = [96, 178, 260]
        y = 66
        cx = self.width() / 2
        k = _ease((t - 0.15) / 0.45) if merge else 0
        done = k >= 1
        m_a = _ease((t - 0.62) / 0.18) if merge else 0
        for i in range(3):
            x = xs[i] + (cx - w / 2 - xs[i]) * k
            r = QRectF(x, y, w, h)
            draw_manga_page(p, r.toRect(), variant=i % 3)
            if m_a <= 0:
                f = p.font()
                f.setPointSizeF(8)
                p.setFont(f)
                p.setPen(QColor(120, 120, 120))
                p.drawText(QRect(int(r.left()), int(r.bottom()) + 4, w, 14),
                           Qt.AlignHCenter, f'第 {i + 1} 章')
        if m_a > 0:
            # 合并后的厚书脊（三道拼合纹）
            p.save()
            p.setOpacity(m_a)
            r = QRectF(cx - 72, y - 8, 144, h + 16)
            p.setPen(QPen(_ACCENT, 2.4))
            p.setBrush(Qt.NoBrush)
            p.drawRoundedRect(r, 5, 5)
            for i in (1, 2):
                x = r.left() + i * r.width() / 3
                p.drawLine(int(x), int(r.top()), int(x), int(r.bottom()))
            p.restore()
        return done and m_a >= 1

    def _sc_ff_off(self, p, t):
        """不勾选：每个文件单独输出。"""
        self._fusion_scene(p, t, merge=False)
        self._caption(p, '每个文件单独转换，输出 3 个文件')

    def _sc_ff_on(self, p, t):
        """勾选：合并为单个文件。"""
        done = self._fusion_scene(p, t, merge=True)
        if done:
            self._caption(p, '所有文件合并为单个输出', QColor(34, 139, 34), True)
        else:
            self._caption(p, '章节文件向一起合并……', _ACCENT)

    # ================= JPEG / PNG / mozJpeg =================
    # 代码语义（KCC_gui.py）：不勾选=标准 JPEG；半勾选=forcepng 黑白图
    # 输出无损 PNG；勾选=mozjpeg 同画质体积小 10-20%，耗时翻倍

    def _imgformat_scene(self, p, t, fmt, frac, note, caption, cap_color, bold):
        page = QRectF(52, 62, 96, 144)
        draw_manga_page(p, page.toRect(), variant=0)
        x0, y0, ref = 200, 118, 130.0
        e = _ease((t - 0.1) / 0.35)
        bw = ref * frac * e
        f = p.font()
        f.setPointSizeF(10)
        f.setBold(True)
        p.setFont(f)
        p.setPen(QColor(90, 90, 90))
        p.drawText(QRectF(x0, y0 - 24, 160, 18), Qt.AlignLeft, fmt)
        p.setPen(Qt.NoPen)
        p.setBrush(_ACCENT)
        p.drawRect(QRectF(x0, y0, bw, 26))
        if note and e >= 1:
            f.setPointSizeF(8)
            f.setBold(False)
            p.setFont(f)
            p.setPen(QColor(150, 110, 40))
            p.drawText(QRectF(x0, y0 + 32, 180, 14), Qt.AlignLeft, note)
        self._caption(p, caption, cap_color, bold)

    def _sc_fmt_jpeg(self, p, t):
        """不勾选：标准 JPEG。"""
        self._imgformat_scene(p, t, 'JPEG', 1.0, None,
                              '标准 JPEG 输出', QColor(120, 120, 120), False)

    def _sc_fmt_png(self, p, t):
        """半勾选：黑白图输出无损 PNG（体积更大）。"""
        self._imgformat_scene(p, t, 'PNG（黑白图）', 1.5, '无损，体积更大',
                              '黑白图片输出为无损 PNG', _ACCENT, True)

    def _sc_fmt_moz(self, p, t):
        """勾选：mozJpeg 更小的 JPEG。"""
        self._imgformat_scene(p, t, 'mozJpeg', 0.85, '体积 -10~20%，耗时 ×2',
                              '同等画质，体积更小、耗时翻倍', QColor(34, 139, 34), True)

    # ================= 极限黑点 =================
    # 代码语义（image.py autolevelImage）：黑点设为最常见的暗色像素值，
    # 适用于文字为黑色但扫描画面发灰的情况

    def _text_page(self, p, rect, tone):
        """画一页文字扫描稿：横线模拟文字行，tone 为文字灰度（0=纯黑）。"""
        p.setPen(QPen(QColor(176, 176, 176), 1))
        p.setBrush(QColor(253, 253, 250))
        p.drawRoundedRect(rect, 2, 2)
        inner = rect.adjusted(12, 14, -12, -14)
        widths = (1.0, 0.88, 0.95, 0.72, 1.0, 0.9, 0.8, 0.97, 0.66, 0.92, 0.84, 0.6)
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(tone, tone, tone))
        y = inner.top()
        for w in widths:
            if y + 5 > inner.bottom():
                break
            p.drawRoundedRect(QRectF(inner.left(), y, inner.width() * w, 5), 2, 2)
            y += 13

    def _sc_al_off(self, p, t):
        """不勾选：默认黑点（最暗像素→纯黑），发灰的文字依旧发灰。"""
        r = QRectF((self.width() - 150) / 2, 34, 150, 208)
        self._text_page(p, r, 125)
        self._caption(p, '默认黑点：文字灰度基本不变，画面仍发灰')

    def _sc_al_on(self, p, t):
        """勾选：黑点=最常见的暗色，文字整体压黑。"""
        k = _ease((t - 0.2) / 0.45)
        r = QRectF((self.width() - 150) / 2, 34, 150, 208)
        self._text_page(p, r, int(125 - 108 * k))
        if k >= 1:
            self._caption(p, '黑点=最常见暗色：文字更黑更实', QColor(34, 139, 34), True)
        elif k > 0:
            self._caption(p, '黑点压向最常见的暗色……', _ACCENT)
        else:
            self._caption(p, '发灰的原始扫描页')

    # ================= 分卷大小 =================
    # 代码语义（KCC_gui.py:384 / comic2ebook.py）：不勾选=默认上限
    # （条漫 100MB，其他 400MB）；勾选=按「分卷大小 MB」拆分

    def _volume_bar(self, p, rect, label, color=QColor(120, 120, 120)):
        p.setPen(QPen(QColor(150, 150, 150), 1))
        p.setBrush(QColor(245, 247, 250))
        p.drawRoundedRect(rect, 5, 5)
        f = p.font()
        f.setPointSizeF(9)
        f.setBold(True)
        p.setFont(f)
        p.setPen(color)
        p.drawText(rect, Qt.AlignCenter, label)

    def _sc_cs_off(self, p, t):
        """不勾选：单文件输出，不超过默认上限即可。"""
        f = p.font()
        f.setPointSizeF(8)
        p.setFont(f)
        p.setPen(QColor(150, 150, 150))
        p.drawText(QRectF(60, 82, 300, 16), Qt.AlignCenter, '默认上限 400MB')
        self._volume_bar(p, QRectF(60, 104, 300, 44), '单文件输出 · 380MB ✓')
        self._caption(p, '默认上限：条漫 100MB，其他 400MB')

    def _sc_cs_on(self, p, t):
        """勾选：输出超过设定大小时拆分为多卷。"""
        k1 = _ease(t / 0.25)          # 切割线生长
        k2 = _ease((t - 0.32) / 0.4)  # 三卷浮现下落
        bar = QRectF(60, 62, 300, 44)
        self._volume_bar(p, bar, '输出合计 450MB')
        seg = 44 * k1
        for frac in (1 / 3, 2 / 3):
            x = int(bar.left() + bar.width() * frac)
            yc = int(bar.top() + 22)
            p.setPen(QPen(_ACCENT, 1.6, Qt.DashLine))
            p.drawLine(x, int(yc - seg / 2), x, int(yc + seg / 2))
        if k2 > 0:
            base = p.opacity()
            p.setOpacity(base * k2)
            sep, w3 = 10.0, (300 - 20) / 3
            yy = 122 + 28 * k2
            for i in range(3):
                self._volume_bar(p, QRectF(60 + i * (w3 + sep), yy, w3, 40),
                                 f'第 {i + 1} 卷 · 150MB', _ACCENT)
            p.setOpacity(base)
        if k2 >= 1:
            self._caption(p, '按「分卷大小」拆分为多卷', QColor(34, 139, 34), True)
        elif k1 > 0:
            self._caption(p, '超出设定大小，按边界拆分……', _ACCENT)
        else:
            self._caption(p, '输出超过了设定的分卷大小')

    # ================= 元数据标题 =================
    # 代码语义（KCC_gui.py:335 / comic2ebook.py metadatatitle）：
    # 不勾选=写入默认标题；半勾选=默认标题附加元数据标题；勾选=仅用元数据标题

    def _meta_scene(self, p, t, label, xml_src, caption, color, bold):
        book = QRectF((self.width() - 100) / 2, 30, 100, 150)
        draw_manga_page(p, book.toRect(), variant=0)
        plate = QRectF((self.width() - 280) / 2, 194, 280, 34)
        p.setPen(QPen(_ACCENT, 1.6))
        p.setBrush(QColor(245, 248, 255))
        p.drawRoundedRect(plate, 6, 6)
        f = p.font()
        f.setPointSizeF(10)
        f.setBold(True)
        p.setFont(f)
        p.setPen(QColor(70, 70, 70))
        p.drawText(plate, Qt.AlignCenter, label)
        if xml_src:
            k = _ease((t - 0.15) / 0.3)
            base = p.opacity()
            p.setOpacity(base * k)
            chip = QRectF(self.width() - 138, 36, 100, 22)
            p.setPen(QPen(QColor(180, 140, 60), 1))
            p.setBrush(QColor(255, 248, 230))
            p.drawRoundedRect(chip, 11, 11)
            f.setPointSizeF(8)
            f.setBold(False)
            p.setFont(f)
            p.setPen(QColor(150, 110, 40))
            p.drawText(chip, Qt.AlignCenter, 'ComicInfo.xml')
            x0 = int(chip.left() + chip.width() / 2)
            p.setPen(QPen(QColor(180, 140, 60), 1.4, Qt.DashLine))
            p.drawLine(x0, int(chip.bottom()) + 3, x0, int(plate.top()) - 6)
            p.setPen(QPen(QColor(180, 140, 60), 1.4))
            p.drawLine(x0, int(plate.top()) - 6, x0 - 5, int(plate.top()) - 12)
            p.drawLine(x0, int(plate.top()) - 6, x0 + 5, int(plate.top()) - 12)
            p.setOpacity(base)
        self._caption(p, caption, color, bold)

    def _sc_mt_off(self, p, t):
        """不勾选：写入默认标题。"""
        self._meta_scene(p, t, '《默认书名 · 第 1 卷》', False,
                         '不勾选：写入默认标题', QColor(120, 120, 120), False)

    def _sc_mt_part(self, p, t):
        """半勾选：默认标题 + 元数据标题。"""
        self._meta_scene(p, t, '《默认书名》 + 《元数据书名》', True,
                         '半勾选：默认标题附加元数据标题', _ACCENT, True)

    def _sc_mt_only(self, p, t):
        """勾选：仅使用元数据标题。"""
        self._meta_scene(p, t, '《ComicInfo 中的书名》', True,
                         '勾选：仅写入元数据标题', QColor(34, 139, 34), True)

    # ================= 禁用处理 =================
    # 代码语义（comic2ebook.py:2016 noprocessing）：不处理任何图片，
    # 忽略设备配置和处理选项，原样打包

    def _pipeline(self, p, box, disabled):
        p.setPen(QPen(QColor(160, 160, 160), 1.6))
        p.setBrush(QColor(248, 248, 248))
        p.drawRoundedRect(box, 8, 8)
        c = box.center()
        r = 13.0
        p.setPen(QPen(QColor(120, 120, 120), 2))
        p.setBrush(Qt.NoBrush)
        p.drawEllipse(c, int(r), int(r))
        for i in range(8):
            a = math.pi / 4 * i
            p.drawLine(int(c.x() + (r + 2) * math.cos(a)),
                       int(c.y() + (r + 2) * math.sin(a)),
                       int(c.x() + (r + 8) * math.cos(a)),
                       int(c.y() + (r + 8) * math.sin(a)))
        if disabled:
            p.setPen(QPen(QColor(200, 60, 60), 3))
            p.drawLine(int(box.left()) + 8, int(box.top()) + 8,
                       int(box.right()) - 8, int(box.bottom()) - 8)

    def _noproc_scene(self, p, t, disabled, caption, color, bold):
        y0, pw, ph = 80, 72, 108
        inr = QRectF(44, y0, pw, ph)
        outw, outh = (pw, ph) if disabled else (58, 88)
        outr = QRectF(self.width() - 44 - outw, y0 + (ph - outh) / 2, outw, outh)
        box = QRectF((self.width() - 76) / 2, y0 + (ph - 76) / 2, 76, 76)
        yy = int(y0 + ph / 2)
        p.setPen(QPen(QColor(170, 170, 170), 1.6))
        for x1, x2 in ((inr.right() + 6, box.left() - 6),
                       (box.right() + 6, outr.left() - 6)):
            p.drawLine(int(x1), yy, int(x2), yy)
            p.drawLine(int(x2), yy, int(x2) - 6, yy - 4)
            p.drawLine(int(x2), yy, int(x2) - 6, yy + 4)
        draw_manga_page(p, inr.toRect(), variant=0)
        k = _ease((t - 0.2) / 0.3)
        if k > 0:
            base = p.opacity()
            p.setOpacity(base * k)
            draw_manga_page(p, outr.toRect(), variant=0)
            p.setOpacity(base)
        self._pipeline(p, box, disabled)
        f = p.font()
        f.setPointSizeF(8)
        p.setFont(f)
        p.setPen(QColor(130, 130, 130))
        p.drawText(QRectF(inr.left() - 10, y0 + ph + 6, pw + 20, 14),
                   Qt.AlignHCenter, '输入')
        p.drawText(QRectF(outr.left() - 10, y0 + ph + 6, outw + 20, 14),
                   Qt.AlignHCenter, '输出（原样）' if disabled else '输出（已适配）')
        self._caption(p, caption, color, bold)

    def _sc_np_off(self, p, t):
        """不勾选：按设备配置处理图片。"""
        self._noproc_scene(p, t, False,
                           '按设备配置处理：缩放、调整画面', QColor(120, 120, 120), False)

    def _sc_np_on(self, p, t):
        """勾选：图片原样打包，跳过所有处理。"""
        self._noproc_scene(p, t, True,
                           '图片原样输出，跳过所有处理', QColor(34, 139, 34), True)

    # ================= 删除输入 =================
    # 代码语义（comic2ebook.py:2105 options.delete）：转换完成后删除
    # 输入文件/目录，此操作不可恢复

    def _mini_page(self, p, rect, label):
        p.setPen(QPen(QColor(160, 160, 160), 1))
        p.setBrush(QColor(252, 252, 250))
        p.drawRoundedRect(rect, 3, 3)
        inner = rect.adjusted(8, 8, -8, -8)
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(190, 190, 190))
        y = inner.top()
        while y + 3 <= inner.bottom() - 4:
            p.drawRect(QRectF(inner.left(), y, inner.width(), 3))
            y += 8
        f = p.font()
        f.setPointSizeF(8)
        p.setFont(f)
        p.setPen(QColor(120, 120, 120))
        p.drawText(QRectF(rect.left() - 8, rect.bottom() + 3, rect.width() + 16, 14),
                   Qt.AlignHCenter, label)

    def _del_scene(self, p, t, delete):
        y0, w, h, gap = 76, 56, 80, 12
        xs = [30 + i * (w + gap) for i in range(3)]
        out = QRectF(self.width() - 40 - 72, y0 - 10, 72, 100)
        k_out = _ease((t - 0.15) / 0.25)
        k_del = _ease((t - 0.5) / 0.35) if delete else 0
        base = p.opacity()
        # 箭头：输入 → 输出
        yy = int(y0 + h / 2)
        p.setPen(QPen(QColor(170, 170, 170), 1.6))
        p.drawLine(xs[-1] + w + 8, yy, int(out.left()) - 8, yy)
        p.drawLine(int(out.left()) - 8, yy, int(out.left()) - 14, yy - 4)
        p.drawLine(int(out.left()) - 8, yy, int(out.left()) - 14, yy + 4)
        # 输出弹出
        if k_out > 0:
            p.setOpacity(base * k_out)
            draw_manga_page(p, out.toRect(), variant=0)
            f = p.font()
            f.setPointSizeF(8)
            p.setFont(f)
            p.setPen(QColor(120, 120, 120))
            p.drawText(QRectF(out.left() - 8, out.bottom() + 3, out.width() + 16, 14),
                       Qt.AlignHCenter, '输出')
            p.setOpacity(base)
        # 输入文件（可逐个打叉渐隐）
        for i, x in enumerate(xs):
            d = min(max(k_del * 3 - i * 0.6, 0.0), 1.0)
            p.setOpacity(base * (1 - d))
            self._mini_page(p, QRectF(x, y0, w, h), f'输入 {i + 1}')
            if 0.25 < d < 1:
                c = QRectF(x, y0, w, h).center()
                p.setPen(QPen(QColor(200, 60, 60), 2.4))
                p.drawLine(int(c.x()) - 8, int(c.y()) - 8, int(c.x()) + 8, int(c.y()) + 8)
                p.drawLine(int(c.x()) - 8, int(c.y()) + 8, int(c.x()) + 8, int(c.y()) - 8)
        p.setOpacity(base)
        return k_del >= 1

    def _sc_del_off(self, p, t):
        """不勾选：输入文件原样保留。"""
        self._del_scene(p, t, delete=False)
        self._caption(p, '不勾选：转换后输入文件保留', QColor(120, 120, 120), False)

    def _sc_del_on(self, p, t):
        """勾选：转换完成后删除输入文件。"""
        done = self._del_scene(p, t, delete=True)
        if done:
            self._caption(p, '输入文件已删除（不可恢复！）', QColor(200, 60, 60), True)
        else:
            self._caption(p, '转换完成，正在删除输入文件……', _ACCENT)

    # ================= 输出拆分 =================
    # 代码语义（KCC_gui.py:317 → batchsplit=2；comic2ebook.py:1335）：
    # 不勾选=自动模式（输出自动拆分）；勾选=分卷模式（每个子目录单独一卷）

    def _folder_tree(self, p, x, y):
        rows = [('漫画（源目录）', QColor(90, 90, 90)),
                ('├─ 第 1 卷/', QColor(120, 120, 120)),
                ('├─ 第 2 卷/', QColor(120, 120, 120)),
                ('└─ 第 3 卷/', QColor(120, 120, 120))]
        f = p.font()
        f.setPointSizeF(9)
        p.setFont(f)
        for i, (r, c) in enumerate(rows):
            p.setPen(c)
            p.drawText(QRectF(x, y + i * 22, 160, 18), Qt.AlignLeft, r)

    def _os_arrow(self, p):
        yy = 128
        p.setPen(QPen(QColor(170, 170, 170), 1.6))
        p.drawLine(196, yy, 244, yy)
        p.drawLine(244, yy, 238, yy - 4)
        p.drawLine(244, yy, 238, yy + 4)

    def _sc_os_off(self, p, t):
        """不勾选：自动模式，输出自动拆分。"""
        self._folder_tree(p, 36, 84)
        self._os_arrow(p)
        k = _ease((t - 0.2) / 0.3)
        if k > 0:
            base = p.opacity()
            p.setOpacity(base * k)
            draw_manga_page(p, QRect(278, 76, 72, 104), variant=0)
            f = p.font()
            f.setPointSizeF(8)
            p.setFont(f)
            p.setPen(QColor(120, 120, 120))
            p.drawText(QRectF(268, 184, 92, 14), Qt.AlignHCenter, '输出（自动）')
            p.setOpacity(base)
        self._caption(p, '自动模式：输出自动拆分')

    def _sc_os_on(self, p, t):
        """勾选：分卷模式，每个子目录输出为单独一卷。"""
        self._folder_tree(p, 36, 84)
        self._os_arrow(p)
        base = p.opacity()
        for i in range(3):
            k = _ease((t - 0.15 - i * 0.12) / 0.25)
            if k <= 0:
                continue
            p.setOpacity(base * k)
            x = 258 + i * 48
            draw_manga_page(p, QRect(x, 76, 42, 64), variant=i % 3)
            f = p.font()
            f.setPointSizeF(8)
            p.setFont(f)
            p.setPen(QColor(120, 120, 120))
            p.drawText(QRectF(x - 4, 144, 50, 14), Qt.AlignHCenter, f'第 {i + 1} 卷')
        p.setOpacity(base)
        if _ease((t - 0.39) / 0.25) >= 1:
            self._caption(p, '分卷模式：每个子目录单独输出一卷', QColor(34, 139, 34), True)
        else:
            self._caption(p, '子目录逐个输出为独立的卷……', _ACCENT)

    # ================= 首先旋转 =================
    # 代码语义（image.py:435 rotatefirst）：跨页拆分半勾选（拆分+旋转）时，
    # 旋转版跨页排在拆分页面之前（-kcc-a）还是之后（-kcc-d，默认）

    def _rot_thumb(self, p, cx, cy):
        """旋转 90° 的跨页缩略图（横版），中心在 (cx,cy)。"""
        p.save()
        p.translate(cx, cy)
        p.rotate(90)
        p.scale(0.52, 0.52)
        draw_spread(p, QPoint(0, 0), 92, 138, 4)
        p.restore()

    def _sc_rf_off(self, p, t):
        """不勾选：旋转跨页排在拆分页面之后。"""
        y, w, h = 78, 64, 96
        xs = [92, 192, 292]
        draw_manga_page(p, QRect(xs[0] - w // 2, y, w, h), variant=0)
        draw_manga_page(p, QRect(xs[1] - w // 2, y, w, h), variant=1)
        k = _ease((t - 0.2) / 0.3)
        if k > 0:
            base = p.opacity()
            p.setOpacity(base * k)
            self._rot_thumb(p, xs[2], y + h // 2)
            p.setOpacity(base)
        self._order_badges(p, min(t / 0.6, 1.0),
                           [QPoint(xs[0], y - 12), QPoint(xs[1], y - 12),
                            QPoint(xs[2], y - 12)])
        self._caption(p, '顺序：左页 → 右页 → 旋转跨页（最后）')

    def _sc_rf_on(self, p, t):
        """勾选：旋转跨页排在最前。"""
        y, w, h = 78, 64, 96
        xs = [92, 192, 292]
        k = _ease((t - 0.2) / 0.4)
        rot_x = xs[2] + (xs[0] - xs[2]) * k
        l_x = xs[0] + (xs[1] - xs[0]) * k
        r_x = xs[1] + (xs[2] - xs[1]) * k
        draw_manga_page(p, QRect(int(l_x - w / 2), y, w, h), variant=0)
        draw_manga_page(p, QRect(int(r_x - w / 2), y, w, h), variant=1)
        self._rot_thumb(p, int(rot_x), y + h // 2)
        if k >= 1:
            self._order_badges(p, _ease((t - 0.65) / 0.3),
                               [QPoint(xs[0], y - 12), QPoint(xs[1], y - 12),
                                QPoint(xs[2], y - 12)])
            self._caption(p, '顺序：旋转跨页（最前）→ 左页 → 右页',
                          QColor(34, 139, 34), True)
        else:
            self._caption(p, '旋转跨页移到最前……', _ACCENT)

    # ================= 向右旋转 =================
    # 代码语义（image.py:218/247 rotateright）：跨页默认逆时针旋转 90°
    # （PIL rotate(90)）；勾选后改为顺时针（向右）旋转 90°（rotate(-90)）

    def _rr_scene(self, p, t, cw, caption, color, bold):
        angle = (90 if cw else -90) * _ease((t - 0.2) / 0.45)
        center = QPoint(self.width() // 2, (self.height() - 2) // 2)
        p.save()
        p.translate(center)
        s = 1.0 - 0.28 * _ease((t - 0.2) / 0.45)
        p.scale(s, s)
        p.rotate(angle)
        draw_spread(p, QPoint(0, 0), 122, 182, 0)
        p.restore()
        # 旋转方向由动画本身体现，无需额外标记
        self._caption(p, caption, color, bold)

    def _sc_rr_off(self, p, t):
        """不勾选：跨页逆时针旋转 90°（默认）。"""
        self._rr_scene(p, t, False, '默认：跨页逆时针旋转 90°',
                       QColor(120, 120, 120), False)

    def _sc_rr_on(self, p, t):
        """勾选：跨页改为顺时针（向右）旋转 90°。"""
        self._rr_scene(p, t, True, '向右旋转：跨页顺时针旋转 90°',
                       QColor(34, 139, 34), True)

    # ================= 智能封面裁剪 =================
    # 代码语义（image.py:636 crop_main_cover）：宽幅图（宽/高>1.83）时
    # 裁出封面区域（从左到右阅读取偏右的一段），丢弃其余部分

    def _wide_book(self, p, rect):
        """画一本横版宽幅封面：封底 | 书脊 | 封面。"""
        w = rect.width()
        back = QRectF(rect.left(), rect.top(), w / 3, rect.height())
        spine = QRectF(rect.left() + w / 3, rect.top(), w / 3, rect.height())
        front = QRectF(rect.left() + 2 * w / 3, rect.top(), w / 3, rect.height())
        p.setPen(QPen(QColor(176, 176, 176), 1))
        p.setBrush(QColor(210, 218, 226))
        p.drawRect(back)
        p.setBrush(QColor(150, 160, 172))
        p.drawRect(spine)
        draw_manga_page(p, front.toRect(), variant=0)
        f = p.font()
        f.setPointSizeF(8)
        p.setFont(f)
        p.setPen(QColor(110, 110, 110))
        p.drawText(back, Qt.AlignCenter, '封底')
        p.setPen(QColor(240, 240, 240))
        p.drawText(spine, Qt.AlignCenter, '书脊')

    def _sc_scc_off(self, p, t):
        """不勾选：宽幅原图完整保留。"""
        rect = QRectF((self.width() - 252) / 2, 92, 252, 120)
        self._wide_book(p, rect)
        self._caption(p, '宽幅原图完整保留：封底 + 书脊 + 封面')

    def _sc_scc_on(self, p, t):
        """勾选：裁出封面区域，丢弃其余部分。"""
        rect = QRectF((self.width() - 252) / 2, 92, 252, 120)
        crop = QRectF(rect.left() + rect.width() * 0.52, rect.top(),
                      rect.width() * 0.31, rect.height())
        k1 = _ease(t / 0.28)            # 取景框出现
        k2 = _ease((t - 0.34) / 0.3)    # 框外渐隐
        k3 = _ease((t - 0.58) / 0.32)   # 封面区移到中央放大
        base = p.opacity()
        if k3 <= 0:
            if k2 > 0:
                # 框外部分渐隐：分两段重画（裁剪框左侧、右侧）
                p.setOpacity(base * (1 - k2))
                p.save()
                p.setClipRect(QRectF(rect.left(), rect.top(),
                                     crop.left() - rect.left(), rect.height()))
                self._wide_book(p, rect)
                p.restore()
                p.save()
                p.setClipRect(QRectF(crop.right(), rect.top(),
                                     rect.right() - crop.right(), rect.height()))
                self._wide_book(p, rect)
                p.restore()
                p.setOpacity(base)
                # 框内部分保持
                p.save()
                p.setClipRect(crop)
                self._wide_book(p, rect)
                p.restore()
            else:
                self._wide_book(p, rect)
            if k1 > 0:
                p.setPen(QPen(_ACCENT, 2))
                p.setBrush(Qt.NoBrush)
                p.drawRect(crop)
        else:
            # 裁出的封面区域移到中央并放大为竖版（与原图封面一致的画风）
            tw, th = 96, 144
            tx = crop.left() + (self.width() / 2 - tw / 2 - crop.left()) * k3
            ty = crop.top() + (74 - crop.top()) * k3
            dw = crop.width() + (tw - crop.width()) * k3
            dh = crop.height() + (th - crop.height()) * k3
            draw_manga_page(p, QRectF(tx, ty, dw, dh).toRect(), variant=0)
        if k3 >= 1:
            self._caption(p, '裁出封面区域，丢弃其余部分', QColor(34, 139, 34), True)
        elif k1 > 0:
            self._caption(p, '定位封面区域并裁切……', _ACCENT)
        else:
            self._caption(p, '宽幅原图：封底 + 书脊 + 封面')

    # ================= 封面填充 =================
    # 代码语义（image.py:630 coverfill）：封面按设备宽高比居中裁剪后
    # 填满整个屏幕（ImageOps.fit）；默认仅等比缩放（thumbnail），可能留边

    def _cf_screen(self, p, rect):
        p.setPen(QPen(QColor(120, 120, 120), 2))
        p.setBrush(QColor(238, 238, 238))
        p.drawRoundedRect(rect, 6, 6)

    def _sc_cf_off(self, p, t):
        """不勾选：封面等比缩放完整放入屏幕，可能留有边距。"""
        screen = QRectF((self.width() - 140) / 2, 34, 140, 210)
        self._cf_screen(p, screen)
        cover = QRectF(screen.left(), screen.top() + 12, 140, 186)
        draw_manga_page(p, cover.toRect(), variant=0)
        self._caption(p, '默认：完整保留封面，上下留有边距')

    def _sc_cf_on(self, p, t):
        """勾选：封面居中裁剪后填满屏幕。"""
        screen = QRectF((self.width() - 140) / 2, 34, 140, 210)
        self._cf_screen(p, screen)
        k = _ease((t - 0.2) / 0.4)
        cw = 140 + (157 - 140) * k
        ch = 186 + (210 - 186) * k
        cover = QRectF(screen.left() + (140 - cw) / 2,
                       screen.top() + (210 - ch) / 2 + 12 * (1 - k), cw, ch)
        p.save()
        p.setClipRect(screen.adjusted(1, 1, -1, -1))
        draw_manga_page(p, cover.toRect(), variant=0)
        p.restore()
        if k >= 1:
            self._caption(p, '填满屏幕：左右边缘被裁掉', QColor(34, 139, 34), True)
        elif k > 0:
            self._caption(p, '放大至填满屏幕……', _ACCENT)
        else:
            self._caption(p, '原始封面')

    # ================= 反转方向 =================
    # 代码语义（comic2ebook.py:414 invertdirection）：仅反转 EPUB 的
    # 翻页方向（page-progression-direction），页面内容顺序不变

    def _id_scene(self, p, t, invert, caption, color, bold):
        y, w, h, gap = 74, 72, 108, 24
        xs = [self.width() / 2 - w - gap, self.width() / 2, self.width() / 2 + w + gap]
        # 日漫（不勾选）：从右向左阅读，书页从左往右排为 3、2、1；
        # 反转后：从左向右阅读，排为 1、2、3
        labels = ['第 1 页', '第 2 页', '第 3 页'] if invert else \
                 ['第 3 页', '第 2 页', '第 1 页']
        variants = [0, 1, 2] if invert else [2, 1, 0]
        for i, cx in enumerate(xs):
            draw_manga_page(p, QRect(int(cx - w / 2), y, w, h), variant=variants[i])
            f = p.font()
            f.setPointSizeF(9)
            f.setBold(True)
            p.setFont(f)
            p.setPen(_ACCENT)
            p.drawText(QRectF(cx - w / 2, y - 20, w, 16), Qt.AlignCenter,
                       labels[i])
        # 翻页方向箭头（页面下方）
        ay = y + h + 30
        x0, x1 = int(xs[0] - w / 2), int(xs[2] + w / 2)
        p.setPen(QPen(_ACCENT, 2.2))
        p.drawLine(x0, ay, x1, ay)
        d = 1 if invert else -1
        ex = x1 if invert else x0
        p.drawLine(ex, ay, ex - 9 * d, ay - 6)
        p.drawLine(ex, ay, ex - 9 * d, ay + 6)
        f.setPointSizeF(8)
        f.setBold(False)
        p.setFont(f)
        p.setPen(QColor(130, 130, 130))
        p.drawText(QRectF(x0, ay + 8, x1 - x0, 14), Qt.AlignCenter, '翻页方向')
        self._caption(p, caption, color, bold)

    def _sc_id_off(self, p, t):
        """不勾选：翻页方向与「从右向左」设置一致（以日漫为例：右→左）。"""
        self._id_scene(p, t, False, '以日漫为例：不勾选时保持右→左翻页',
                       QColor(120, 120, 120), False)

    def _sc_id_on(self, p, t):
        """勾选：翻页方向反转，页面顺序不变（以日漫为例：变为左→右）。"""
        self._id_scene(p, t, True, '日漫反转为左→右翻页，页面顺序不变',
                       QColor(34, 139, 34), True)

    # ================= 轻小说模式 =================
    # 代码语义（comic2ebook.py:977/1630/1892 lightnovel）：仅调整图片尺寸，
    # 保留原始文件结构（不重组为标准 EPUB 结构）

    def _ln_tree(self, p, x, y, rows):
        f = p.font()
        f.setPointSizeF(9)
        p.setFont(f)
        for i, (text, c) in enumerate(rows):
            p.setPen(c)
            p.drawText(QRectF(x, y + i * 20, 170, 16), Qt.AlignLeft, text)

    def _sc_ln_off(self, p, t):
        """不勾选：重组为标准 EPUB 结构。"""
        g = QColor(120, 120, 120)
        d = QColor(90, 90, 90)
        self._ln_tree(p, 24, 74, [('小说/', d), ('├─ 第 1 章.xhtml', g),
                                  ('├─ 第 2 章.xhtml', g), ('└─ 插图/', g)])
        self._ln_tree(p, 226, 74, [('OEBPS/', d), ('├─ Text/', g),
                                   ('├─ Images/', g), ('└─ content.opf', g)])
        p.setPen(QPen(QColor(170, 170, 170), 1.6))
        p.drawLine(198, 112, 222, 112)
        p.drawLine(222, 112, 216, 108)
        p.drawLine(222, 112, 216, 116)
        self._caption(p, '默认：重组为标准 EPUB 目录结构')

    def _sc_ln_on(self, p, t):
        """勾选：保留原始结构，仅调整图片尺寸。"""
        g = QColor(120, 120, 120)
        d = QColor(90, 90, 90)
        rows = [('小说/', d), ('├─ 第 1 章.xhtml', g),
                ('├─ 第 2 章.xhtml', g), ('└─ 插图/', g)]
        self._ln_tree(p, 24, 74, rows)
        self._ln_tree(p, 226, 74, rows)
        p.setPen(QPen(QColor(170, 170, 170), 1.6))
        p.drawLine(198, 112, 222, 112)
        p.drawLine(222, 112, 216, 108)
        p.drawLine(222, 112, 216, 116)
        # 图片尺寸标注变化
        k = _ease((t - 0.2) / 0.35)
        f = p.font()
        f.setPointSizeF(8)
        p.setFont(f)
        if k < 1:
            p.setPen(QColor(150, 150, 150))
            p.drawText(QRectF(24, 168, 170, 14), Qt.AlignLeft,
                       '插图 2400px（原尺寸）')
            if k > 0:
                base = p.opacity()
                p.setOpacity(base * k)
                p.setPen(_ACCENT)
                p.drawText(QRectF(226, 168, 170, 14), Qt.AlignLeft,
                           '插图 → 适配设备尺寸')
                p.setOpacity(base)
        else:
            p.setPen(QColor(150, 150, 150))
            p.drawText(QRectF(24, 168, 170, 14), Qt.AlignLeft,
                       '插图 2400px（原尺寸）')
            p.setPen(_ACCENT)
            p.drawText(QRectF(226, 168, 170, 14), Qt.AlignLeft,
                       '插图 → 适配设备尺寸')
        if k >= 1:
            self._caption(p, '结构原样保留，仅图片缩小', QColor(34, 139, 34), True)
        else:
            self._caption(p, '保留原始文件结构……', _ACCENT)

    # ================= 单页横屏 =================
    # 代码语义（comic2ebook.py:494 onepagelandscape）：横屏时所有页的
    # page-spread 属性写为 center（单页居中视口），默认为 left/right 配对

    def _opl_screen(self, p, rect):
        p.setPen(QPen(QColor(120, 120, 120), 2))
        p.setBrush(QColor(238, 238, 238))
        p.drawRoundedRect(rect, 6, 6)

    def _sc_opl_off(self, p, t):
        """不勾选：双页横屏，左右两页各一个视口。"""
        screen = QRectF((self.width() - 268) / 2, 70, 268, 150)
        self._opl_screen(p, screen)
        draw_manga_page(p, QRect(int(screen.left()) + 14, int(screen.top()) + 10,
                                 116, 130), variant=0)
        draw_manga_page(p, QRect(int(screen.right()) - 130, int(screen.top()) + 10,
                                 116, 130), variant=1)
        self._caption(p, '双页横屏：左右两页各一个视口')

    def _sc_opl_on(self, p, t):
        """勾选：单页横屏，单页使用单个居中视口。"""
        screen = QRectF((self.width() - 268) / 2, 70, 268, 150)
        self._opl_screen(p, screen)
        k = _ease((t - 0.15) / 0.35)
        base = p.opacity()
        # 两侧区域压暗，突出居中视口
        p.setOpacity(base * k)
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(120, 120, 120, 90))
        p.drawRect(QRectF(screen.left() + 2, screen.top() + 2, 66, 146))
        p.drawRect(QRectF(screen.right() - 68, screen.top() + 2, 66, 146))
        p.setOpacity(base)
        draw_manga_page(p, QRect(int(screen.left()) + 86, int(screen.top()) + 10,
                                 96, 130), variant=0)
        self._caption(p, '单页横屏：单页居中视口', QColor(34, 139, 34), True)

    # ================= 壁纸模式 =================
    # 代码语义（KCC_gui.py:1073 toggleWallpaperBox）：自动勾选适合
    # KOReader 壁纸的选项（图像文件夹/仅旋转/不旋转/放大/无损 PNG）

    _WP_ROWS = ['输出格式：图像文件夹', '跨页拆分：仅旋转', '不旋转',
                '拉伸/放大', '无损 PNG']

    def _wp_row(self, p, x, y, text, prog):
        """一行选项：复选框 + 文字，prog∈[0,1] 为打勾动画进度。"""
        box = QRectF(x, y, 15, 15)
        p.setPen(QPen(QColor(160, 160, 160), 1.4))
        p.setBrush(QColor(255, 255, 255))
        p.drawRoundedRect(box, 3, 3)
        if prog > 0:
            p.setPen(QPen(_ACCENT, 2.2))
            x0, y0 = box.left(), box.top()
            p.drawLine(int(x0 + 3), int(y0 + 8),
                       int(x0 + 3 + 3.5 * min(prog * 2, 1)),
                       int(y0 + 8 + 3.5 * min(prog * 2, 1)))
            k2 = max(prog * 2 - 1, 0)
            p.drawLine(int(x0 + 6.5), int(y0 + 11.5),
                       int(x0 + 6.5 + 6 * k2), int(y0 + 11.5 - 8 * k2))
        f = p.font()
        f.setPointSizeF(9.5)
        p.setFont(f)
        p.setPen(QColor(90, 90, 90))
        p.drawText(QRectF(x + 24, y - 1, 220, 18), Qt.AlignLeft, text)

    def _sc_wp_off(self, p, t):
        """不勾选：选项保持手动设置。"""
        for i, text in enumerate(self._WP_ROWS):
            self._wp_row(p, 108, 62 + i * 32, text, 0)
        self._caption(p, '不勾选：各项选项保持手动设置')

    def _sc_wp_on(self, p, t):
        """勾选：自动勾选适合 KOReader 壁纸的选项组合。"""
        n = len(self._WP_ROWS)
        done = True
        for i, text in enumerate(self._WP_ROWS):
            k = _ease((t - 0.08 - i * 0.13) / 0.12)
            self._wp_row(p, 108, 62 + i * 32, text, k)
            if k < 1:
                done = False
        if done:
            self._caption(p, '一键配好 KOReader 壁纸所需的选项组合',
                          QColor(34, 139, 34), True)
        else:
            self._caption(p, '自动勾选适合壁纸的选项……', _ACCENT)

    # ================= 保留 ComicInfo.xml =================
    # 代码语义（comic2ebook.py:1182 keepcomicinfo）：仅 CBZ 输出时，
    # 把原始 ComicInfo.xml 保留在输出文件中

    def _ci_scene(self, p, t, keep, caption, color, bold):
        inr = QRectF(56, 84, 64, 92)
        outr = QRectF(self.width() - 56 - 64, 84, 64, 92)
        self._mini_page(p, inr, '输入 CBZ')
        self._mini_page(p, outr, '输出 CBZ')
        yy = int(inr.top() + inr.height() / 2)
        p.setPen(QPen(QColor(170, 170, 170), 1.6))
        p.drawLine(int(inr.right()) + 8, yy, int(outr.left()) - 8, yy)
        p.drawLine(int(outr.left()) - 8, yy, int(outr.left()) - 14, yy - 4)
        p.drawLine(int(outr.left()) - 8, yy, int(outr.left()) - 14, yy + 4)
        # ComicInfo.xml 文档芯片
        x0 = inr.right() + 26
        if keep:
            k = _ease((t - 0.2) / 0.4)
            cx = x0 + (outr.left() - 26 - x0) * k
            cy = yy - 40
        else:
            k = _ease((t - 0.2) / 0.4)
            cx = x0
            cy = yy - 40 + 34 * k
        base = p.opacity()
        p.setOpacity(base * (1 if keep else 1 - k))
        chip = QRectF(cx - 46, cy - 12, 92, 24)
        p.setPen(QPen(QColor(180, 140, 60), 1))
        p.setBrush(QColor(255, 248, 230))
        p.drawRoundedRect(chip, 12, 12)
        f = p.font()
        f.setPointSizeF(8)
        p.setFont(f)
        p.setPen(QColor(150, 110, 40))
        p.drawText(chip, Qt.AlignCenter, 'ComicInfo.xml')
        if not keep and 0.3 < k < 1:
            p.setPen(QPen(QColor(200, 60, 60), 2.2))
            p.drawLine(int(cx) - 7, int(cy) - 7, int(cx) + 7, int(cy) + 7)
            p.drawLine(int(cx) - 7, int(cy) + 7, int(cx) + 7, int(cy) - 7)
        p.setOpacity(base)
        self._caption(p, caption, color, bold)

    def _sc_ci_off(self, p, t):
        """不勾选：输出中不包含原始 ComicInfo.xml。"""
        self._ci_scene(p, t, False, '不勾选：丢弃原始 ComicInfo.xml',
                       QColor(120, 120, 120), False)

    def _sc_ci_on(self, p, t):
        """勾选：原始 ComicInfo.xml 保留在输出中。"""
        self._ci_scene(p, t, True, '原始 ComicInfo.xml 保留在输出 CBZ 中',
                       QColor(34, 139, 34), True)

    # ================= 自定义 JPEG 质量 =================
    # 代码语义（comic2ebook.py:1721 jpegquality）：不勾选=默认 85
    # （KS/KCS 设备 90）；勾选=使用自定义值（0~95），越低体积越小画质越差

    def _jpeg_page(self, p, rect, artifact):
        """画一页漫画，artifact∈[0,1] 时叠加马赛克块模拟 JPEG 压缩失真。"""
        draw_manga_page(p, rect, variant=0)
        if artifact > 0:
            p.setPen(Qt.NoPen)
            step = 14
            for yy in range(rect.top() + 6, rect.bottom() - 6, step):
                for xx in range(rect.left() + 6, rect.right() - 6, step):
                    v = ((xx * 7 + yy * 13) % 41) - 20
                    g = 128 + v
                    p.setBrush(QColor(g, g, g, int(70 * artifact)))
                    p.drawRect(QRectF(xx, yy, step, step))
            p.setBrush(Qt.NoBrush)

    def _sc_jq_off(self, p, t):
        """不勾选：默认 JPEG 质量。"""
        rect = QRect(int((self.width() - 108) / 2), 44, 108, 162)
        self._jpeg_page(p, rect, 0)
        f = p.font()
        f.setPointSizeF(9)
        f.setBold(True)
        p.setFont(f)
        p.setPen(QColor(90, 90, 90))
        p.drawText(QRectF(0, rect.bottom() + 8, self.width(), 16),
                   Qt.AlignHCenter, 'JPEG 质量：默认 85')
        self._caption(p, '默认质量 85（KS/KCS 设备为 90）')

    def _sc_jq_on(self, p, t):
        """勾选：自定义 JPEG 质量，越低体积越小、画质越差。"""
        k = _ease((t - 0.2) / 0.45)
        rect = QRect(int((self.width() - 108) / 2), 44, 108, 162)
        self._jpeg_page(p, rect, k)
        q = int(85 - 45 * k)
        f = p.font()
        f.setPointSizeF(9)
        f.setBold(True)
        p.setFont(f)
        p.setPen(_ACCENT)
        p.drawText(QRectF(0, rect.bottom() + 8, self.width(), 16),
                   Qt.AlignHCenter, f'JPEG 质量：{q}')
        if k >= 1:
            self._caption(p, '自定义质量（0~95）：越低体积越小、画质越差',
                          QColor(34, 139, 34), True)
        else:
            self._caption(p, '调低质量，体积减小、失真增加……', _ACCENT)

    # ================= 不量化 =================
    # 代码语义（comic2ebook.py:758 noquantize）：PNG 输出默认量化到
    # 16 色（4 位，PIL quantize 自带抖动）以减小体积；勾选后保留完整
    # 256 级灰阶（8 位），体积翻倍。墨水屏只有 16 级灰度，通常无需勾选

    def _dither_gradient(self, w, h):
        """16 级灰阶 + Bayer 抖动的渐变图（模拟量化后的实际观感），缓存。"""
        key = (w, h)
        img = self._DITHER_CACHE.get(key)
        if img is None:
            img = QImage(w, h, QImage.Format_RGB32)
            bayer = ((0, 8, 2, 10), (12, 4, 14, 6), (3, 11, 1, 9), (15, 7, 13, 5))
            for yy in range(h):
                for xx in range(w):
                    pos = xx / (w - 1) * 15
                    lo = int(pos)
                    frac = pos - lo
                    hi = min(lo + 1, 15) if frac * 16 > bayer[yy % 4][xx % 4] else lo
                    g = int(hi * 235 / 15)
                    img.setPixelColor(xx, yy, QColor(g, g, g))
            self._DITHER_CACHE[key] = img
        return img

    _DITHER_CACHE = {}

    def _gray_page(self, p, rect, smooth_opacity):
        """灰阶渐变页：底层为 16 级抖动量化，smooth_opacity 控制平滑层。"""
        p.setPen(QPen(QColor(176, 176, 176), 1))
        p.setBrush(QColor(253, 253, 251))
        p.drawRoundedRect(rect, 2, 2)
        inner = rect.adjusted(14, 14, -14, -14)
        p.drawImage(inner, self._dither_gradient(inner.width(), inner.height()))
        if smooth_opacity > 0:
            base = p.opacity()
            p.setOpacity(base * smooth_opacity)
            grad = QLinearGradient(inner.topLeft(), inner.topRight())
            grad.setColorAt(0, QColor(0, 0, 0))
            grad.setColorAt(1, QColor(235, 235, 235))
            p.fillRect(inner, grad)
            p.setOpacity(base)

    def _size_bar(self, p, y, frac, label):
        """页面下方的体积对比条。"""
        f = p.font()
        f.setPointSizeF(8)
        p.setFont(f)
        x = (self.width() - 140) / 2
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(220, 220, 220))
        p.drawRect(QRectF(x, y, 140, 10))
        p.setBrush(_ACCENT)
        p.drawRect(QRectF(x, y, 140 * frac, 10))
        p.setPen(QColor(130, 130, 130))
        p.drawText(QRectF(0, y + 13, self.width(), 14), Qt.AlignHCenter, label)
        p.setBrush(Qt.NoBrush)

    def _sc_nq_off(self, p, t):
        """不勾选：16 级灰阶 + 抖动，体积小，屏幕上几乎无差别。"""
        rect = QRect(int((self.width() - 150) / 2), 44, 150, 168)
        self._gray_page(p, rect, 0)
        self._size_bar(p, rect.bottom() + 8, 0.4, '4 位（16 级）· 体积小')
        self._caption(p, '默认：对齐墨水屏 16 级灰度，屏上几乎无差别')

    def _sc_nq_on(self, p, t):
        """勾选：不量化，保留 256 级灰阶，体积翻倍。"""
        k = _ease((t - 0.25) / 0.4)
        rect = QRect(int((self.width() - 150) / 2), 44, 150, 168)
        self._gray_page(p, rect, k)
        self._size_bar(p, rect.bottom() + 8, 0.4 + 0.6 * k,
                       '8 位（256 级）· 体积翻倍' if k >= 1 else '体积增大……')
        if k >= 1:
            self._caption(p, '不量化：256 级灰阶，体积翻倍', QColor(34, 139, 34), True)
        else:
            self._caption(p, '保留更多灰阶……', _ACCENT)

    # ================= WebP =================
    # 代码语义（comic2ebook.py:1730 webp_output）：有损 WebP 替换 JPG、
    # 无损 WebP 替换 PNG；PDF 与 Kindle MOBI/AZW3 输出不生效

    def _webp_row(self, p, y, src, dst, frac, k):
        f = p.font()
        f.setPointSizeF(9.5)
        f.setBold(True)
        p.setFont(f)
        p.setPen(QColor(90, 90, 90))
        p.drawText(QRectF(60, y, 70, 18), Qt.AlignLeft, src)
        p.setPen(QPen(QColor(170, 170, 170), 1.6))
        p.drawLine(134, y + 9, 170, y + 9)
        p.drawLine(170, y + 9, 164, y + 5)
        p.drawLine(170, y + 9, 164, y + 13)
        if k > 0:
            base = p.opacity()
            p.setOpacity(base * k)
            p.setPen(_ACCENT)
            p.drawText(QRectF(178, y, 110, 18), Qt.AlignLeft, dst)
            # 体积条
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(200, 200, 200))
            p.drawRect(QRectF(300, y + 3, 80, 12))
            p.setBrush(_ACCENT)
            p.drawRect(QRectF(300, y + 3, 80 * frac, 12))
            p.setOpacity(base)
        else:
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(200, 200, 200))
            p.drawRect(QRectF(300, y + 3, 80, 12))

    def _sc_wp2_off(self, p, t):
        """不勾选：JPG/PNG 原格式输出。"""
        self._webp_row(p, 100, 'JPG', '', 1.0, 0)
        self._webp_row(p, 140, 'PNG', '', 1.0, 0)
        f = p.font()
        f.setPointSizeF(9.5)
        f.setBold(True)
        p.setFont(f)
        p.setPen(QColor(90, 90, 90))
        p.drawText(QRectF(178, 100, 110, 18), Qt.AlignLeft, 'JPG')
        p.drawText(QRectF(178, 140, 110, 18), Qt.AlignLeft, 'PNG')
        self._caption(p, '默认：JPG / PNG 原格式输出')

    def _sc_wp2_on(self, p, t):
        """勾选：JPG→有损 WebP，PNG→无损 WebP。"""
        k1 = _ease((t - 0.15) / 0.3)
        k2 = _ease((t - 0.4) / 0.3)
        self._webp_row(p, 100, 'JPG', 'WebP（有损）', 0.7, k1)
        self._webp_row(p, 140, 'PNG', 'WebP（无损）', 0.85, k2)
        if k2 >= 1:
            self._caption(p, '体积进一步缩小，质量设置同样生效',
                          QColor(34, 139, 34), True)
        else:
            self._caption(p, '替换为 WebP 格式……', _ACCENT)

    # ================= 强制 EBOK =================
    # 代码语义（comic2ebook.py:2123 ebok）：Kindle MOBI 标记为 EBOK
    # （图书）而非 PDOC（个人文档），影响在 Kindle 上的归类

    def _eb_library(self, p, book_section, k):
        """Kindle 书库：图书 / 文档 两个分区，书出现在指定分区。"""
        sx, sy, sw, sh = 90, 44, 240, 190
        p.setPen(QPen(QColor(120, 120, 120), 2))
        p.setBrush(QColor(250, 250, 250))
        p.drawRoundedRect(QRectF(sx, sy, sw, sh), 6, 6)
        f = p.font()
        f.setPointSizeF(9)
        f.setBold(True)
        p.setFont(f)
        p.setPen(QColor(90, 90, 90))
        p.drawText(QRectF(sx + 12, sy + 8, 100, 16), Qt.AlignLeft, '图书')
        p.drawText(QRectF(sx + 12, sy + 96, 100, 16), Qt.AlignLeft, '文档')
        p.setPen(QPen(QColor(210, 210, 210), 1))
        p.drawLine(sx + 12, sy + 88, sx + sw - 12, sy + 88)
        # 书
        by = sy + 28 if book_section == 0 else sy + 116
        base = p.opacity()
        p.setOpacity(base * k)
        draw_manga_page(p, QRect(sx + 16, by, 34, 50), variant=0)
        f.setPointSizeF(8)
        f.setBold(False)
        p.setFont(f)
        p.setPen(QColor(110, 110, 110))
        p.drawText(QRectF(sx + 58, by + 16, 160, 16), Qt.AlignLeft,
                   '我的漫画.mobi')
        p.setOpacity(base)

    def _sc_eb_off(self, p, t):
        """不勾选：MOBI 标记为 PDOC，归入「文档」。"""
        self._eb_library(p, 1, _ease((t - 0.15) / 0.3))
        self._caption(p, '默认 PDOC：出现在 Kindle 的「文档」里')

    def _sc_eb_on(self, p, t):
        """勾选：MOBI 标记为 EBOK，归入「图书」。"""
        self._eb_library(p, 0, _ease((t - 0.15) / 0.3))
        if _ease((t - 0.15) / 0.3) >= 1:
            self._caption(p, 'EBOK：出现在 Kindle 的「图书」里',
                          QColor(34, 139, 34), True)
        else:
            self._caption(p, '标记为 EBOK……', _ACCENT)

    # ================= 临时目录 =================
    # 代码语义（comic2ebook.py:919 tempdir）：不勾选=系统盘上的专用
    # 临时目录；勾选=在源文件所在盘上创建临时目录

    def _td_drive(self, p, rect, label, sub, active):
        p.setPen(QPen(_ACCENT if active else QColor(160, 160, 160), 1.6))
        p.setBrush(QColor(245, 248, 255) if active else QColor(246, 246, 246))
        p.drawRoundedRect(rect, 6, 6)
        f = p.font()
        f.setPointSizeF(11)
        f.setBold(True)
        p.setFont(f)
        p.setPen(_ACCENT if active else QColor(110, 110, 110))
        p.drawText(QRectF(rect.left(), rect.top() + 10, rect.width(), 20),
                   Qt.AlignHCenter, label)
        f.setPointSizeF(8)
        f.setBold(False)
        p.setFont(f)
        p.setPen(QColor(130, 130, 130))
        p.drawText(QRectF(rect.left(), rect.top() + 34, rect.width(), 14),
                   Qt.AlignHCenter, sub)

    def _td_scene(self, p, t, on_source, caption, color, bold):
        c_rect = QRectF(52, 74, 130, 60)
        d_rect = QRectF(self.width() - 52 - 130, 74, 130, 60)
        self._td_drive(p, c_rect, 'C:', '系统盘', not on_source)
        self._td_drive(p, d_rect, 'D:', '源文件所在盘', on_source)
        f = p.font()
        f.setPointSizeF(8)
        p.setFont(f)
        p.setPen(QColor(120, 120, 120))
        p.drawText(QRectF(d_rect.left() - 15, d_rect.bottom() + 8, 160, 14),
                   Qt.AlignHCenter, '漫画.cbz（源文件）')
        # 临时目录芯片
        k = _ease((t - 0.2) / 0.35)
        base = p.opacity()
        p.setOpacity(base * k)
        host = d_rect if on_source else c_rect
        chip = QRectF(host.left() + 8, host.bottom() + 30, host.width() - 16, 22)
        p.setPen(QPen(QColor(180, 140, 60), 1))
        p.setBrush(QColor(255, 248, 230))
        p.drawRoundedRect(chip, 11, 11)
        p.setPen(QColor(150, 110, 40))
        p.drawText(chip, Qt.AlignCenter, 'KCC 临时目录')
        p.setOpacity(base)
        self._caption(p, caption, color, bold)

    def _sc_td_off(self, p, t):
        """不勾选：临时目录在系统盘。"""
        self._td_scene(p, t, False, '默认：使用系统盘上的专用临时目录',
                       QColor(120, 120, 120), False)

    def _sc_td_on(self, p, t):
        """勾选：临时目录建在源文件所在盘。"""
        self._td_scene(p, t, True, '在源文件所在盘上创建临时目录',
                       QColor(34, 139, 34), True)

    # ================= PNG 兼容模式 =================
    # 代码语义（comic2ebook.py:764 pnglegacy）：PNG 输出用兼容性更好的
    # 8 位灰度 PNG 代替 4 位调色板 PNG（作用于 forcepng 的 PNG 输出路径）

    def _pl_scene(self, p, t, legacy, caption, color, bold):
        rect = QRect(int((self.width() - 130) / 2), 40, 130, 168)
        self._gray_page(p, rect, 0)
        k = _ease((t - 0.2) / 0.35)
        chip = QRectF((self.width() - 200) / 2, rect.bottom() + 10, 200, 26)
        base = p.opacity()
        if legacy and k < 1:
            # 旧芯片淡出
            p.setOpacity(base * (1 - k))
            self._pl_chip(p, chip, '4 位 PNG（调色板）', QColor(150, 150, 150))
            p.setOpacity(base * k)
            self._pl_chip(p, chip, '8 位 PNG（灰度）', _ACCENT)
            p.setOpacity(base)
        elif legacy:
            self._pl_chip(p, chip, '8 位 PNG（灰度）', _ACCENT)
        else:
            self._pl_chip(p, chip, '4 位 PNG（调色板）', QColor(150, 150, 150))
        self._caption(p, caption, color, bold)

    def _pl_chip(self, p, rect, text, color):
        p.setPen(QPen(color, 1.4))
        p.setBrush(QColor(250, 250, 250))
        p.drawRoundedRect(rect, 13, 13)
        f = p.font()
        f.setPointSizeF(9)
        f.setBold(True)
        p.setFont(f)
        p.setPen(color)
        p.drawText(rect, Qt.AlignCenter, text)

    def _sc_pl_off(self, p, t):
        """不勾选：4 位调色板 PNG（默认）。"""
        self._pl_scene(p, t, False, '默认：4 位调色板 PNG，体积更小',
                       QColor(120, 120, 120), False)

    def _sc_pl_on(self, p, t):
        """勾选：8 位灰度 PNG，兼容性更好。"""
        self._pl_scene(p, t, True, '8 位灰度 PNG，兼容性更好',
                       QColor(34, 139, 34), True)

    # ================= 强制 PNG RGB =================
    # 代码语义（image.py:468 force_png_rgb）：全彩图片也用无损 PNG 保存
    # （默认仅黑白图走 PNG），会显著增加文件体积

    def _prgb_scene(self, p, t, png, caption, color, bold):
        rect = QRect(int((self.width() - 120) / 2), 36, 120, 160)
        draw_manga_page(p, rect, variant=0)
        k = _ease((t - 0.2) / 0.35) if png else 1
        frac = 0.45 + 0.55 * k if png else 0.45
        label = ('PNG · 无损 · 体积显著增大' if k >= 1 else '体积增大……') \
            if png else 'JPEG · 有损 · 体积小'
        self._size_bar(p, rect.bottom() + 10, frac, label)
        self._caption(p, caption, color, bold)

    def _sc_prgb_off(self, p, t):
        """不勾选：全彩图片保存为 JPEG。"""
        self._prgb_scene(p, t, False, '全彩图片默认保存为 JPEG（有损）',
                         QColor(120, 120, 120), False)

    def _sc_prgb_on(self, p, t):
        """勾选：全彩图片保存为无损 PNG。"""
        self._prgb_scene(p, t, True, '全彩图片也保存为无损 PNG',
                         QColor(34, 139, 34), True)

    # ================= 旧版面板视图 =================
    # 代码语义（comic2ebook.py:160/1685 legacypanelview）：启用 KCC 6 的
    # 旧版面板视图（放大格固定按 1.5x），新版按设备分辨率精确计算

    def _lpv_scene(self, p, t, legacy, caption, color, bold):
        page = self._page_rect()
        draw_manga_page(p, page.toRect(), variant=2)
        frames = self._quad_frames(page)
        k = _ease((t - 0.15) / 0.35)
        cam = frames[0]
        if k > 0:
            path = QPainterPath()
            path.addRect(QRectF(self.rect()))
            path.addRoundedRect(cam, 4, 4)
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(30, 30, 30, int(110 * k)))
            p.drawPath(path)
            p.setBrush(Qt.NoBrush)
            p.setPen(QPen(QColor(255, 255, 255, int(220 * k)), 4))
            p.drawRoundedRect(cam, 4, 4)
            p.setPen(QPen(_ACCENT, 2))
            p.drawRoundedRect(cam, 4, 4)
            # 放大方式徽标
            text = 'KCC 6 · 1.5x' if legacy else '新版 · 精确适配'
            bw = 26 + len(text) * 9
            badge = QRectF(cam.right() - bw, cam.top() - 9, bw, 16)
            p.setPen(Qt.NoPen)
            p.setBrush(_ACCENT)
            p.drawRoundedRect(badge, 8, 8)
            f = p.font()
            f.setPointSizeF(8)
            f.setBold(True)
            p.setFont(f)
            p.setPen(QColor(255, 255, 255))
            p.drawText(badge, Qt.AlignCenter, text)
            p.setBrush(Qt.NoBrush)
        self._caption(p, caption, color, bold)

    def _sc_lpv_off(self, p, t):
        """不勾选：新版面板视图（按设备精确计算）。"""
        self._lpv_scene(p, t, False, '默认：新版面板视图方式',
                        QColor(120, 120, 120), False)

    def _sc_lpv_on(self, p, t):
        """勾选：KCC 6 旧版面板视图（固定 1.5x 放大格）。"""
        self._lpv_scene(p, t, True, 'KCC 6 旧版方式：固定 1.5x 放大格',
                        QColor(34, 139, 34), True)

    # ================= PDF 宽度渲染 =================
    # 代码语义（comic2ebook.py:808 pdfwidth）：矢量 PDF 竖版页默认按设备
    # 高度渲染；勾选后按设备宽度渲染（横版页始终按高度）

    def _pdfw_scene(self, p, t, by_width, caption, color, bold):
        screen = QRectF((self.width() - 140) / 2, 34, 140, 210)
        self._cf_screen(p, screen)
        k = _ease((t - 0.2) / 0.4)
        # 页面：默认按高度铺满（宽 112）；按宽度渲染后宽 140、高超出
        pw = 112 + (140 - 112) * (k if by_width else 0)
        ph = pw * 210 / 112
        page = QRectF(screen.left() + (140 - pw) / 2,
                      screen.top() + (210 - ph) / 2, pw, ph)
        p.save()
        p.setClipRect(screen.adjusted(1, 1, -1, -1))
        draw_manga_page(p, page.toRect(), variant=0)
        p.restore()
        self._caption(p, caption, color, bold)

    def _sc_pdfw_off(self, p, t):
        """不勾选：按设备高度渲染，整页可见。"""
        self._pdfw_scene(p, t, False, '默认：按设备高度渲染，整页可见',
                         QColor(120, 120, 120), False)

    def _sc_pdfw_on(self, p, t):
        """勾选：按设备宽度渲染，页面撑满宽度。"""
        self._pdfw_scene(p, t, True, '按设备宽度渲染：撑满宽度，上下超出',
                         QColor(34, 139, 34), True)

    # ================= 旧版提取 =================
    # 代码语义（comic2ebook.py:821/952 legacyextract）：PDF/EPUB 图片
    # 提取方式——默认整页渲染为图片；旧版直接抽取页面内嵌的原始图片

    def _le_scene(self, p, t, legacy, caption, color, bold):
        inr = QRectF(60, 80, 76, 110)
        self._mini_page(p, inr, 'PDF 页面')
        outr = QRectF(self.width() - 60 - 76, 80, 76, 110)
        yy = int(inr.top() + inr.height() / 2)
        p.setPen(QPen(QColor(170, 170, 170), 1.6))
        p.drawLine(int(inr.right()) + 8, yy, int(outr.left()) - 8, yy)
        p.drawLine(int(outr.left()) - 8, yy, int(outr.left()) - 14, yy - 4)
        p.drawLine(int(outr.left()) - 8, yy, int(outr.left()) - 14, yy + 4)
        k = _ease((t - 0.2) / 0.35)
        base = p.opacity()
        if k > 0:
            p.setOpacity(base * k)
            draw_manga_page(p, outr.toRect(), variant=0)
            f = p.font()
            f.setPointSizeF(8)
            p.setFont(f)
            p.setPen(QColor(120, 120, 120))
            p.drawText(QRectF(outr.left() - 8, outr.bottom() + 3,
                              outr.width() + 16, 14), Qt.AlignHCenter,
                       '整页图片' if not legacy else '内嵌原图')
            p.setOpacity(base)
        if legacy and k > 0:
            # 从页面中滑出的图片标记
            p.setOpacity(base * k)
            sx = inr.right() + (outr.left() - inr.right()) * k
            p.setPen(QPen(_ACCENT, 1.6, Qt.DashLine))
            p.setBrush(Qt.NoBrush)
            p.drawRect(QRectF(sx - 20, inr.top() + 16, 40, 52))
            p.setOpacity(base)
        self._caption(p, caption, color, bold)

    def _sc_le_off(self, p, t):
        """不勾选：整页渲染为图片（推荐）。"""
        self._le_scene(p, t, False, '默认：整页渲染为图片（推荐）',
                       QColor(120, 120, 120), False)

    def _sc_le_on(self, p, t):
        """勾选：直接抽取页面内嵌的原始图片。"""
        self._le_scene(p, t, True, '旧版提取：直接抽取页面内嵌的原图',
                       QColor(34, 139, 34), True)


class DemoCard(QFrame):
    """演示卡片：圆角白底 + 投影 + 淡入上浮。"""

    def __init__(self, parent=None):
        super().__init__(parent, Qt.ToolTip | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_ShowWithoutActivating)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(28)
        shadow.setOffset(0, 5)
        shadow.setColor(QColor(0, 0, 0, 70))
        self.setGraphicsEffect(shadow)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(_SHADOW + 12, _SHADOW + 10, _SHADOW + 12, _SHADOW + 12)
        lay.setSpacing(6)
        self.title = QLabel()
        f = self.title.font()
        f.setPointSizeF(11.5)
        f.setBold(True)
        self.title.setFont(f)
        self.subtitle = QLabel()
        self.subtitle.setStyleSheet('color:#666;')
        self.canvas = DemoCanvas('spread')
        lay.addWidget(self.title)
        lay.addWidget(self.subtitle)
        lay.addWidget(self.canvas)
        self.layout().activate()
        self.adjustSize()
        self.setFixedSize(self.sizeHint())

        self._anim_opacity = QPropertyAnimation(self, b'windowOpacity', self)
        self._anim_pos = QPropertyAnimation(self, b'pos', self)
        for a in (self._anim_opacity, self._anim_pos):
            a.setDuration(200)
            a.setEasingCurve(QEasingCurve.OutCubic)

    def configure(self, title, subtitle, demo):
        self.title.setText(title)
        self.subtitle.setText(subtitle)
        self.canvas.demo = demo
        # 文本变化后强制重新布局，确保后续量到的尺寸是最终尺寸
        self.layout().activate()
        self.adjustSize()
        self.setFixedSize(self.sizeHint())

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        body = self.rect().adjusted(_SHADOW, _SHADOW, -_SHADOW, -_SHADOW)
        p.setPen(QPen(QColor(0, 0, 0, 26), 1))
        p.setBrush(QColor(255, 255, 255, 252))
        p.drawRoundedRect(body, 12, 12)
        p.end()

    def popup(self, pos):
        for a in (self._anim_opacity, self._anim_pos):
            a.stop()
        self.move(pos + QPoint(0, 8))
        self.setWindowOpacity(0.0)
        self.show()
        # 显示后按实际尺寸做最终钳制，保证完整落在屏幕内
        screen = QApplication.screenAt(pos) or QApplication.primaryScreen()
        area = screen.availableGeometry()
        fw, fh = self.frameGeometry().width(), self.frameGeometry().height()
        final = QPoint(max(area.left() + 4, min(pos.x(), area.right() - fw - 4)),
                       max(area.top() + 4, min(pos.y(), area.bottom() - fh - 4)))
        if os.environ.get('KCC_DEMO_AUTO'):
            with open(os.path.expanduser('~/kcc_demo_debug.log'), 'a', encoding='utf-8') as fp:
                fp.write(f'pos={pos.x()},{pos.y()} fw={fw} fh={fh} '
                         f'area={area.left()},{area.top()},{area.right()},{area.bottom()} '
                         f'final={final.x()},{final.y()}\n')
        if final != pos:
            self.move(final + QPoint(0, 8))
        self.canvas.start()
        self._anim_opacity.setStartValue(0.0)
        self._anim_opacity.setEndValue(1.0)
        self._anim_pos.setStartValue(final + QPoint(0, 8))
        self._anim_pos.setEndValue(final)
        self._anim_opacity.start()
        self._anim_pos.start()

    def dismiss(self):
        for a in (self._anim_opacity, self._anim_pos):
            a.stop()
        self._anim_opacity.setStartValue(self.windowOpacity())
        self._anim_opacity.setEndValue(0.0)
        self._anim_opacity.setDuration(140)
        self._anim_opacity.start()
        self._anim_opacity.finished.connect(self._after_dismiss)

    def _after_dismiss(self):
        try:
            self._anim_opacity.finished.disconnect(self._after_dismiss)
        except RuntimeError:
            pass
        if self.windowOpacity() < 0.05:
            self.canvas.stop()
            self.hide()


class _HoverFilter(QObject):
    """转发目标控件的 Enter/Leave 事件。"""

    def __init__(self, manager, key, parent):
        super().__init__(parent)
        self._manager = manager
        self._key = key
        parent.installEventFilter(self)

    def eventFilter(self, obj, event):
        t = event.type()
        if t == QEvent.Enter:
            self._manager.show(self._key, obj)
        elif t == QEvent.Leave:
            self._manager.hide_soon()
        return False


_SPECS = {
    'rotateBox': ('跨页拆分 · 动画演示', '横向双页跨页的三种处理方式', 'spread'),
    'qualityBox': ('面板视图 · 动画演示', '把整页漫画逐格放大，三种档位', 'panel'),
    'mangaBox': ('从右向左 · 动画演示', '切换漫画的阅读方向', 'manga'),
    'webtoonBox': ('条漫模式 · 动画演示', '拼接为长条后按屏高沿格子间隙切成一屏一屏', 'webtoon'),
    'croppingBox': ('裁剪模式 · 动画演示', '不裁剪 / 裁白边 / 页码定界裁剪', 'crop'),
    'upscaleBox': ('拉伸/放大 · 动画演示', '小图适配屏幕的三种策略', 'upscale'),
    'colorBox': ('彩色模式 · 动画演示', '灰度（墨水屏）或保留彩色', 'color'),
    'borderBox': ('黑/白边距 · 动画演示', '补边时边距颜色的三种策略', 'border'),
    'gammaBox': ('自定义伽马 · 动画演示', '调整画面中间调的明暗', 'gamma'),
    'spreadShiftBox': ('跨页偏移 · 动画演示', '配对起点后移一页，跨页正确拼合', 'spreadshift'),
    'interPanelCropBox': ('面板间裁剪 · 动画演示', '裁掉分格之间的空白带', 'interpanel'),
    'autocontrastBox': ('自定义自动对比度 · 动画演示', '拉伸画面的明暗范围', 'autocontrast'),
    'noRotateBox': ('不旋转 · 动画演示', '跨页拆分时锁定双页方向', 'norotate'),
    'vertical4PanelBox': ('纵向 4 面板 · 动画演示', '4 面板放大的阅读顺序\n前置：启用「面板视图 4/2/高清」或「旧版面板视图」（Webtoon 模式下无效）', 'v4panel'),
    'maximizeStrips': ('1x4 转 2x2 条带 · 动画演示', '条漫面板的两种排布', 'strips'),
    'eraseRainbowBox': ('彩虹纹消除 · 动画演示', '净化彩色墨水屏画面', 'rainbow'),
    'fileFusionBox': ('文件合并 · 动画演示', '多个文件合并为单个输出', 'filefusion'),
    'mozJpegBox': ('JPEG/PNG/mozJpeg · 动画演示', '输出图片格式的三种选择', 'imgformat'),
    'autoLevelBox': ('极限黑点 · 动画演示', '把最常见的暗色设为纯黑，文字更黑更实', 'autolevel'),
    'chunkSizeCheckBox': ('分卷大小 · 动画演示', '输出文件超过上限时拆分为多卷', 'chunksize'),
    'metadataTitleBox': ('元数据标题 · 动画演示', '电子书书名来源的三种方案', 'metatitle'),
    'disableProcessingBox': ('禁用处理 · 动画演示', '图片原样打包，忽略设备配置', 'noprocessing'),
    'deleteBox': ('删除输入 · 动画演示', '转换完成后删除输入文件（不可恢复）', 'deleteinput'),
    'outputSplit': ('输出拆分 · 动画演示', '源目录含子目录时的输出方式', 'outputsplit'),
    'rotateFirstBox': ('首先旋转 · 动画演示', '旋转版跨页在输出中的位置\n前置：跨页拆分为半勾选（拆分+旋转）', 'rotatefirst'),
    'rotateRightBox': ('向右旋转 · 动画演示', '跨页按相反方向旋转', 'rotateright'),
    'smartCoverCropBox': ('智能封面裁剪 · 动画演示', '从宽幅图片中裁出封面区域', 'smartcover'),
    'coverFillBox': ('封面填充 · 动画演示', '封面居中裁剪后填满屏幕', 'coverfill'),
    'invertDirectionBox': ('反转方向 · 动画演示', '只反转翻页方向，页面顺序不变<br>方向以「从右向左」为基准取反，此处以日漫为例<br>💡 适用场景：内容是日漫（右→左），但想按左→右方向翻页', 'invertdir'),
    'lightnovelBox': ('轻小说模式 · 动画演示', '保留原始文件结构，仅调整图片尺寸', 'lightnovel'),
    'onePageLandscapeBox': ('单页横屏 · 动画演示', '横屏时的视口分配方式', 'onepagelandscape'),
    'wallpaperBox': ('壁纸模式 · 动画演示', '一键配好 KOReader 壁纸所需选项', 'wallpaper'),
    'keepComicInfoBox': ('保留 ComicInfo.xml · 动画演示', '原始元数据文件是否写入输出\n仅对 CBZ 输出生效', 'comicinfo'),
    'jpegQualityBox': ('自定义 JPEG 质量 · 动画演示', '质量与体积的取舍（0~95）', 'jpgq'),
    'noQuantizeBox': ('不量化 · 动画演示', 'PNG 保留完整灰阶\n作用于 PNG 输出（「JPEG/PNG/mozJpeg」半勾选时）\n💡 默认已按墨水屏 16 级灰度优化，通常无需勾选', 'noquant'),
    'webpBox': ('WebP · 动画演示', 'JPG/PNG 替换为 WebP，体积更小\nPDF 与 Kindle MOBI/AZW3 输出不生效', 'webp'),
    'ebokBox': ('强制 EBOK · 动画演示', 'MOBI 归入 Kindle「图书」而非「文档」，仅 MOBI 输出生效<br>💡 离线超过一个月后再联网，可能导致 USB 导入的书被删除', 'ebok'),
    'tempDirBox': ('临时目录 · 动画演示', '转换过程中的临时文件放在哪里', 'tempdir'),
    'pngLegacyBox': ('PNG 兼容模式 · 动画演示', '8 位灰度 PNG 代替 4 位调色板 PNG\n作用于 PNG 输出（「JPEG/PNG/mozJpeg」半勾选时）', 'pnglegacy'),
    'forcePngRgbBox': ('强制 PNG RGB · 动画演示', '全彩图片也保存为无损 PNG\n作用于 PNG 输出（「JPEG/PNG/mozJpeg」半勾选时）', 'pngrgb'),
    'legacyPanelViewBox': ('旧版面板视图 · 动画演示', 'KCC 6 的面板视图方式（固定 1.5x 放大格）<br>💡 适用于固件 5.19.2（回退前）和 5.19.3+', 'legacypv'),
    'pdfWidthBox': ('PDF 宽度渲染 · 动画演示', '矢量 PDF 按设备宽度而非高度渲染<br>💡 仅影响竖版页面，横版页始终按高度渲染', 'pdfwidth'),
    'legacyExtractBox': ('旧版提取 · 动画演示', '直接抽取 PDF/EPUB 内嵌的原始图片<br>💡 默认整页渲染出现问题时可尝试此项', 'legacyextract'),
}


class _DemoManager:
    def __init__(self):
        self._card = None
        self._filters = []
        self._hide_timer = QTimer()
        self._hide_timer.setSingleShot(True)
        self._hide_timer.setInterval(160)
        self._hide_timer.timeout.connect(self._do_hide)

    def show(self, key, widget):
        title, subtitle, demo = _SPECS[key]
        if self._card is None:
            self._card = DemoCard()
        self._hide_timer.stop()
        self._card.configure(title, subtitle, demo)
        pos = self._fixed_pos(widget, self._card.sizeHint())
        if not self._card.isVisible():
            self._card.popup(pos)
        else:
            self._card.move(pos)
            self._card.canvas.demo = demo

    def hide_soon(self):
        self._hide_timer.start()

    def _do_hide(self):
        if self._card is not None and self._card.isVisible():
            self._card.dismiss()

    @staticmethod
    def _fixed_pos(widget, size):
        """固定位置：主窗口上半部分，水平居中、紧贴工具栏下方。"""
        geo = widget.window().frameGeometry()
        x = geo.left() + (geo.width() - size.width()) // 2
        y = geo.top() + 46
        return QPoint(x, y)


def install_demos(gui):
    """在支持的选项上安装悬停演示。失败静默，绝不影响主程序。"""
    manager = _DemoManager()
    for name in _SPECS:
        widget = getattr(gui, name, None)
        if widget is not None:
            manager._filters.append(_HoverFilter(manager, name, widget))
    gui._kcc_demo_manager = manager  # 防止被 GC

    auto = os.environ.get('KCC_DEMO_AUTO', '').strip()
    if auto:
        key = {'spread': 'rotateBox', 'panel': 'qualityBox', 'manga': 'mangaBox',
               'webtoon': 'webtoonBox', 'crop': 'croppingBox',
               'upscale': 'upscaleBox', 'color': 'colorBox',
               'border': 'borderBox', 'gamma': 'gammaBox',
               'spreadshift': 'spreadShiftBox', 'interpanel': 'interPanelCropBox',
               'autocontrast': 'autocontrastBox', 'norotate': 'noRotateBox',
               'v4panel': 'vertical4PanelBox', 'strips': 'maximizeStrips',
               'rainbow': 'eraseRainbowBox',
               'filefusion': 'fileFusionBox', 'imgformat': 'mozJpegBox',
               'autolevel': 'autoLevelBox', 'chunksize': 'chunkSizeCheckBox',
               'metatitle': 'metadataTitleBox',
               'noprocessing': 'disableProcessingBox',
               'deleteinput': 'deleteBox',
               'outputsplit': 'outputSplit', 'rotatefirst': 'rotateFirstBox',
               'rotateright': 'rotateRightBox',
               'smartcover': 'smartCoverCropBox',
               'coverfill': 'coverFillBox',
               'invertdir': 'invertDirectionBox',
               'lightnovel': 'lightnovelBox',
               'onepagelandscape': 'onePageLandscapeBox',
               'wallpaper': 'wallpaperBox',
               'comicinfo': 'keepComicInfoBox',
               'jpgq': 'jpegQualityBox', 'noquant': 'noQuantizeBox',
               'webp': 'webpBox', 'ebok': 'ebokBox',
               'tempdir': 'tempDirBox',
               'pnglegacy': 'pngLegacyBox', 'pngrgb': 'forcePngRgbBox',
               'legacypv': 'legacyPanelViewBox', 'pdfwidth': 'pdfWidthBox',
               'legacyextract': 'legacyExtractBox'}.get(auto)
        widget = getattr(gui, key, None) if key else None
        if widget is not None:
            QTimer.singleShot(1200, lambda: manager.show(key, widget))
