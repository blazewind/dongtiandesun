# @OS:Windows 11
# @Python:3.12.5
# @Coding: UTF-8
# @功能：批量转换Word文档为PDF
# @时间：2025/5/22-11:11
import os
from win32com import client
from datetime import datetime
import time
import sys

def word_to_pdf(word_app, word_path, pdf_path, max_retries=3):
    """
    将Word文档转换为PDF
    :param word_app: Word应用程序实例
    :param word_path: Word文档路径
    :param pdf_path: 输出PDF路径
    :param max_retries: 最大重试次数
    """
    doc = None
    for attempt in range(max_retries):
        try:
            # 打开Word文档
            doc = word_app.Documents.Open(word_path)
            # 另存为PDF
            doc.SaveAs(pdf_path, FileFormat=17)  # 17表示PDF格式
            # 关闭文档
            doc.Close()
            return True
        except Exception as e:
            if doc:
                try:
                    doc.Close()
                except:
                    pass
            print(f"第 {attempt + 1} 次尝试转换失败：{str(e)}")
            if attempt < max_retries - 1:
                print("等待后重试...")
                time.sleep(2)  # 等待2秒后重试
            else:
                print(f"转换失败: {os.path.basename(word_path)}")
                return False
    return False

def batch_convert_to_pdf(template_name="numbers.docx"):
    """
    批量转换Word文档为PDF
    :param template_name: 要排除的模板文件名
    """
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 创建以当前日期命名的PDF文件夹
    today = datetime.now().strftime("%Y%m%d")
    pdf_folder = os.path.join(current_dir, f"{today}PDF")
    
    # 如果文件夹不存在则创建
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)
        print(f"创建文件夹: {pdf_folder}")

    # 获取需要转换的文件列表
    files_to_convert = [
        f for f in os.listdir(current_dir)
        if (f.endswith(".doc") or f.endswith(".docx"))
        and f != template_name
        and not f.startswith("~$")  # 排除临时文件
    ]

    if not files_to_convert:
        print("没有找到需要转换的Word文档")
        return

    # 创建Word应用程序实例
    word_app = None
    try:
        word_app = client.Dispatch("Word.Application")
        word_app.Visible = False
        word_app.DisplayAlerts = False

        total_files = len(files_to_convert)
        converted_count = 0
        
        # 显示进度条
        for idx, file in enumerate(files_to_convert, 1):
            word_path = os.path.join(current_dir, file)
            pdf_name = os.path.splitext(file)[0] + ".pdf"
            pdf_path = os.path.join(pdf_folder, pdf_name)
            
            print(f"\n[{idx}/{total_files}] 正在转换: {file}")
            if word_to_pdf(word_app, word_path, pdf_path):
                converted_count += 1
                print(f"成功转换: {file} -> {pdf_name}")

        print(f"\n转换完成！共成功转换 {converted_count}/{total_files} 个文件")

    except Exception as e:
        print(f"发生错误：{str(e)}")
    finally:
        if word_app:
            try:
                word_app.Quit()
            except:
                pass
            # 确保Word进程被完全关闭
            os.system("taskkill /F /IM WINWORD.EXE /T >nul 2>&1")

if __name__ == "__main__":
    batch_convert_to_pdf()