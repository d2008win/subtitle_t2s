# 字幕繁简转换工具

将繁体中文字幕文件（srt、ass、ssa）一键转换为简体中文，并自定义文字替换规则。

## 使用方法

### 方式一：直接双击

双击 `字幕繁简转换.exe`，弹出文件选择对话框，选择一个或多个字幕文件。

### 方式二：拖拽

将 `.srt` 字幕文件拖放到 `字幕繁简转换.exe` 上。

- **单个文件**：直接拖拽文件到 `.exe` 上
- **多个文件**：同时选中多个文件一起拖入
- **整个文件夹**：将包含字幕文件的文件夹拖入，自动处理其中所有 `.srt`、`.ass`、`.ssa` 文件

### 输出位置

转换后的文件生成在**原字幕文件所在的同一目录**下，文件名格式为 `原名_简中.srt`。原始文件不会被修改。

## 配置文件

同目录下的 `config.json` 是替换规则配置文件，用任意文本编辑器打开即可修改。

### 规则格式

`rules` 是一个键值对对象，键为查找内容，值为替换内容：

```json
{
  "rules": {
    "舉例1": "举例1",
    "舉例2": "举例2"
  }
}
```

新增规则直接在 `rules` 里加一行即可，规则**按书写顺序依次执行**。

## 自定义图标

将 `icon.ico` 文件放在 `subtitle_t2s/` 目录下，然后打包 。

## 自行打包

打包需要 Python 3.6+ 环境：

```
1、安装以下三个库：
pip install opencc-python-reimplemented
pip install chardet
pip install pyinstaller

2、输入命令行打包，即可生成字幕繁简转换.exe，配合config.json配置文件使用
pyinstaller --onefile --noconsole --icon=icon.ico --distpath . --add-data "config.json;." --clean --name "字幕繁简转换" subtitle_t2s.py
```

## 注意事项

- 转换后的文件统一输出为 UTF-8 编码
- 原始文件不会被修改
- 如果 `config.json` 不存在或格式错误，程序会弹出错误提示
