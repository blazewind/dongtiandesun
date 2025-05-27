import os
from pdf2image import convert_from_path
from datetime import datetime

def pdf_to_jpg(pdf_path, output_folder, dpi=300):
    """
    将PDF转换为JPG图片
    :param pdf_path: PDF文件路径
    :param output_folder: 输出文件夹路径
    :param dpi: 图片分辨率
    """
    try:
        # 转换PDF页面为图片
        images = convert_from_path(pdf_path, dpi=dpi)
        
        # 获取PDF文件名（不含扩展名）
        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        
        # 保存每一页为JPG
        for i, image in enumerate(images):
            # 如果只有一页，则不添加页码
            if len(images) == 1:
                image_path = os.path.join(output_folder, f"{pdf_name}.jpg")
            else:
                image_path = os.path.join(output_folder, f"{pdf_name}_第{i+1}页.jpg")
            image.save(image_path, "JPEG")
        return True
    except Exception as e:
        print(f"转换失败：{str(e)}")
        return False

def batch_convert_to_jpg():
    """
    批量转换PDF文件为JPG图片
    """
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 创建以当前日期命名的JPG文件夹
    today = datetime.now().strftime("%Y%m%d")
    jpg_folder = os.path.join(current_dir, f"{today}JPG")
    
    # 如果文件夹不存在则创建
    if not os.path.exists(jpg_folder):
        os.makedirs(jpg_folder)
        print(f"创建文件夹: {jpg_folder}")
    
    # 遍历当前目录下的所有PDF文档
    current_dir='20250527PDF'
    converted_count = 0
    for file in os.listdir(current_dir):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(current_dir, file)
            
            print(f"正在转换: {file}")
            if pdf_to_jpg(pdf_path, jpg_folder):
                converted_count += 1
                print(f"成功转换: {file}")
            else:
                print(f"转换失败: {file}")
    
    print(f"\n转换完成！共成功转换 {converted_count} 个PDF文件")

if __name__ == "__main__":
    batch_convert_to_jpg()