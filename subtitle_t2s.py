# 字幕繁简转换工具
# 用法：将 .srt 文件拖拽到本程序上，或使用命令行：subtitle_t2s.exe <字幕文件>
import opencc
import os
import sys
import json
import re
import glob

# -----------------------------------------------------------
# 配置加载
# -----------------------------------------------------------
def get_config_path():
    exe_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    p = os.path.join(exe_dir, "config.json")
    if os.path.isfile(p):
        return p
    script_dir = os.path.dirname(os.path.abspath(__file__))
    p = os.path.join(script_dir, "config.json")
    if os.path.isfile(p):
        return p
    return None


def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# -----------------------------------------------------------
# 编码检测
# -----------------------------------------------------------
def detect_encoding(filepath):
    try:
        import chardet
        with open(filepath, "rb") as f:
            raw = f.read()
        result = chardet.detect(raw)
        enc = result.get("encoding", "").lower()
        if enc:
            if "gb2312" in enc or "gbk" in enc or "gb18030" in enc:
                return "gbk"
            if "utf-8" in enc or "utf8" in enc:
                return "utf-8"
            if "utf-16" in enc or "utf16" in enc:
                return "utf-16"
            return enc
    except ImportError:
        pass

    for enc in ("utf-8", "utf-8-sig", "gbk", "big5"):
        try:
            with open(filepath, "r", encoding=enc) as f:
                f.read()
            return enc
        except (UnicodeDecodeError, UnicodeError):
            continue
    return "utf-8"


def read_subtitle(filepath):
    enc = detect_encoding(filepath)
    with open(filepath, "r", encoding=enc, errors="replace") as f:
        return f.read(), enc


# -----------------------------------------------------------
# 核心转换
# -----------------------------------------------------------
def convert(text, rules):
    cc = opencc.OpenCC("t2s")
    text = cc.convert(text)
    for old, new in rules.items():
        text = text.replace(old, new)
    return text


# -----------------------------------------------------------
# 单文件处理
# -----------------------------------------------------------
def process_file(filepath, rules, output_dir):
    filename = os.path.basename(filepath)
    stem, ext = os.path.splitext(filename)
    out_name = f"{stem}_简中{ext}"
    out_path = os.path.join(output_dir, out_name)

    text, src_enc = read_subtitle(filepath)
    result = convert(text, rules)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(result)

    return out_path


# -----------------------------------------------------------
# 主流程
# -----------------------------------------------------------
def show_file_dialog():
    try:
        from tkinter import Tk, filedialog
    except ImportError:
        return None

    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    files = filedialog.askopenfilenames(
        title="选择字幕文件",
        filetypes=[("字幕文件", "*.srt *.ass *.ssa"), ("所有文件", "*.*")],
    )
    root.destroy()
    return list(files) if files else None


def show_error(title, message):
    try:
        from tkinter import Tk, messagebox
        root = Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        messagebox.showerror(title, message)
        root.destroy()
    except ImportError:
        pass


def main():
    config_path = get_config_path()
    if config_path is None:
        show_error("错误", "找不到 config.json 配置文件")
        sys.exit(1)

    try:
        config = load_config(config_path)
    except Exception as e:
        show_error("错误", f"配置文件解析失败:\n{e}")
        sys.exit(1)

    rules = config.get("rules", {})

    args = sys.argv[1:]
    if not args:
        files = show_file_dialog()
        if not files:
            sys.exit(0)
    else:
        files = []
        for arg in args:
            if os.path.isfile(arg):
                files.append(arg)
            elif os.path.isdir(arg):
                for ext in ("*.srt", "*.ass", "*.ssa"):
                    files.extend(glob.glob(os.path.join(arg, ext)))
            else:
                matched = glob.glob(arg)
                if matched:
                    files.extend(m)

    if not files:
        show_error("提示", "未找到任何字幕文件")
        sys.exit(1)

    errors = []
    for i, f in enumerate(files, 1):
        out_dir = os.path.dirname(f)
        try:
            out_path = process_file(f, rules, out_dir)
            if not sys.argv[0].endswith(".exe"):
                print(f"  [{i}/{len(files)}] {os.path.basename(f)} -> {out_path}")
        except Exception as e:
            err = f"{os.path.basename(f)} -> 失败: {e}"
            errors.append(err)
            if not sys.argv[0].endswith(".exe"):
                print(f"  {err}")

    if sys.argv[0].endswith(".exe") and errors:
        show_error("转换完成（有错误）", "\n".join(errors))
    elif not sys.argv[0].endswith(".exe"):
        print(f"\n全部完成！共处理 {len(files)} 个文件")
        input("按回车退出...")


if __name__ == "__main__":
    main()
