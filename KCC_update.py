# -*- coding: utf-8 -*-
"""汉化增强版的 Release 更新检查与提示（非上游功能）。

启动后在后台查询汉化增强版最新 Release。发现更新时，状态栏右侧显示
绿色提示；点击查看本次更新内容，并可前往对应 Release 页面下载。
"""

import re

import requests
from packaging.version import Version
from PySide6.QtCore import QThread, QUrl, Qt, Signal
from PySide6.QtGui import QDesktopServices, QCursor
from PySide6.QtWidgets import (QApplication, QDialog, QDialogButtonBox, QLabel,
                               QPushButton, QTextBrowser, QVBoxLayout)

from . import __version__

API_URL = 'https://api.github.com/repos/pretenderlu/kcc-chinese/releases/latest'
RELEASE_PREFIX = 'https://github.com/pretenderlu/kcc-chinese/releases/tag/'
CURRENT_FIX = 1  # 发布 vX.Y.Z-zh-enhanced-fixN 时同步改为 N
_TAG_RE = re.compile(r'^v?(\d+\.\d+\.\d+)-zh-enhanced(?:-fix(\d+))?$')


def release_version(tag):
    """返回 (上游版本, 修复编号)；非增强版标签返回 None。"""
    match = _TAG_RE.fullmatch(tag or '')
    if not match:
        return None
    return Version(match.group(1)), int(match.group(2) or 0)


def is_newer(tag, current_version=__version__, current_fix=CURRENT_FIX):
    """比较上游版本与 Fix 编号，旧版本的更高 Fix 不视为更新。"""
    latest = release_version(tag)
    if latest is None:
        return False
    latest_base, latest_fix = latest
    current_base = Version(current_version)
    return latest_base > current_base or (latest_base == current_base and latest_fix > current_fix)


class UpdateThread(QThread):
    updateAvailable = Signal(dict)

    def run(self):
        try:
            response = requests.get(API_URL, timeout=10, headers={
                'Accept': 'application/vnd.github+json',
                'User-Agent': 'KCC-Chinese-Enhanced',
            })
            response.raise_for_status()
            release = response.json()
            tag = release.get('tag_name', '')
            url = release.get('html_url', '')
            if not url.startswith(RELEASE_PREFIX) or not is_newer(tag):
                return
            self.updateAvailable.emit({
                'tag_name': tag,
                'html_url': url,
                'body': release.get('body') or '本次发布未提供更新说明。',
            })
        except Exception:
            # 网络不可用、API 限流或返回结构异常时不影响主程序
            pass


def show_update(window, release):
    """展示更新说明；确认后打开对应 Release 下载页面。"""
    dialog = QDialog(window)
    dialog.setWindowTitle('发现新版本')
    dialog.setModal(True)
    dialog.resize(680, 520)
    layout = QVBoxLayout(dialog)
    title = QLabel(f'<b>{release["tag_name"]}</b><br>本次更新内容如下：')
    title.setTextInteractionFlags(Qt.TextSelectableByMouse)
    layout.addWidget(title)
    notes = QTextBrowser()
    notes.setMarkdown(release['body'])
    notes.setOpenExternalLinks(True)
    layout.addWidget(notes, 1)
    hint = QLabel('点击“更新”将打开对应 Release 下载页面。')
    hint.setStyleSheet('color:#666;')
    layout.addWidget(hint)
    buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Yes |
                               QDialogButtonBox.StandardButton.Cancel)
    buttons.button(QDialogButtonBox.StandardButton.Yes).setText('更新')
    buttons.button(QDialogButtonBox.StandardButton.Cancel).setText('取消')
    buttons.accepted.connect(dialog.accept)
    buttons.rejected.connect(dialog.reject)
    layout.addWidget(buttons)
    if dialog.exec() == QDialog.DialogCode.Accepted:
        QDesktopServices.openUrl(QUrl(release['html_url']))


def install_updater(window):
    """在状态栏右侧安装更新提示，后台线程与按钮由主窗口持有。"""
    button = QPushButton('● 有更新')
    button.setFlat(True)
    button.setCursor(QCursor(Qt.PointingHandCursor))
    button.setStyleSheet(
        'QPushButton{border:none;color:#16a34a;font-weight:600;padding:0 8px;}'
        'QPushButton:hover{color:#15803d;text-decoration:underline;}')
    button.setToolTip('发现汉化增强版更新，点击查看更新内容')
    button.hide()
    window.statusBar().addPermanentWidget(button)

    thread = UpdateThread()
    thread.setParent(window)
    QApplication.instance().aboutToQuit.connect(thread.wait)
    window._kcc_update_thread = thread
    window._kcc_update_button = button
    window._kcc_update_release = None

    def present(release):
        window._kcc_update_release = release
        button.setText(f'● 新版本 {release["tag_name"]}')
        button.show()

    def open_details():
        if window._kcc_update_release is not None:
            show_update(window, window._kcc_update_release)

    thread.updateAvailable.connect(present)
    button.clicked.connect(open_details)
    thread.start()
