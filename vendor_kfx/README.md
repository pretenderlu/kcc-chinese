# vendor_kfx

来源：[HankunYu/kindle-comic-workaround-5.19.x](https://github.com/HankunYu/kindle-comic-workaround-5.19.x)
版本：`v1.3.1`(2026-10-23 发布)
授权：MIT（见上游 README；上游仓库未附带 LICENSE 文件）

包含文件：

- `kfx_writer.py` — KFX 单容器序列化器（入口 `generate_kfx()`)
- `kpf_generator.py` — Kindle YJ fragment 结构生成器（被 kfx_writer 依赖）

只依赖 Pillow 与标准库。文件保持上游原样未做修改，便于后续跟版对比。
由 `patch_cn.py` 在打补丁时拷入 `kcc/kindlecomicconverter/` 并注入接线代码。
