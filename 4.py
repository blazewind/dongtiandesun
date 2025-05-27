from PIL import Image
import os

def add_stamp_to_image(original_path, stamp_path, position, output_dir, opacity=0.5):
    # 打开原始图片和印章图片
    base_image = Image.open(original_path)
    stamp = Image.open(stamp_path)

    # 确保印章图片有透明通道
    if stamp.mode != 'RGBA':
        stamp = stamp.convert('RGBA')

    # 创建一个透明度遮罩
    alpha = stamp.getchannel('A')
    # 调整透明度
    alpha = alpha.point(lambda x: int(x * opacity))
    stamp.putalpha(alpha)

    # 创建一个同样大小的透明图层
    transparent = Image.new('RGBA', base_image.size, (0, 0, 0, 0))
    # 将印章放在透明图层的指定位置
    transparent.paste(stamp, position, stamp)

    # 将透明图层与原图合并
    output_image = Image.alpha_composite(base_image.convert('RGBA'), transparent)

    # 转回JPG格式并保存
    output_image = output_image.convert('RGB')
    name_without_ext = os.path.splitext(os.path.basename(original_path))[0]
    output_path = os.path.join(output_dir, f"{name_without_ext}_印章.jpg")
    output_image.save(output_path, 'JPEG', quality=95)

    base_image.close()
    stamp.close()
    output_image.close()

# 获取当前脚本所在的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 创建输出目录（使用绝对路径）
output_dir = os.path.join(current_dir, "JPGOK")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"已创建输出目录: {output_dir}")

# 印章路径和位置坐标
stamp_path = os.path.join(current_dir, "./yinzhang.png")
position = (1773, 1678)

# 遍历当前目录下的所有jpg文件
for filename in os.listdir(current_dir):
    if filename.lower().endswith(('.jpg', '.jpeg')):
        input_path = os.path.join(current_dir, filename)
        add_stamp_to_image(input_path, stamp_path, position, output_dir, opacity=0.7)
        print(f"已处理: {filename}")

# from PIL import Image
# import os


# def add_stamp_to_image(original_path, stamp_path, position, output_dir, opacity=0.5):
#     # 打开原始图片和印章图片
#     base_image = Image.open(original_path)
#     stamp = Image.open(stamp_path)
#
#     # 确保印章图片有透明通道
#     if stamp.mode != 'RGBA':
#         stamp = stamp.convert('RGBA')
#
#     # 创建一个透明度遮罩
#     alpha = stamp.getchannel('A')
#     # 调整透明度
#     alpha = alpha.point(lambda x: int(x * opacity))
#     stamp.putalpha(alpha)
#
#     # 创建一个同样大小的透明图层
#     transparent = Image.new('RGBA', base_image.size, (0, 0, 0, 0))
#     # 将印章放在透明图层的指定位置
#     transparent.paste(stamp, position, stamp)
#
#     # 将透明图层与原图合并
#     output_image = Image.alpha_composite(base_image.convert('RGBA'), transparent)
#
#     # 转回JPG格式并保存
#     output_image = output_image.convert('RGB')
#     name_without_ext = os.path.splitext(os.path.basename(original_path))[0]
#     output_path = os.path.join(output_dir, f"{name_without_ext}_印章.jpg")
#     output_image.save(output_path, 'JPEG', quality=95)
#
#     base_image.close()
#     stamp.close()
#     output_image.close()


# def main():
#     # 获取用户输入
#     jpg_dir = input("请输入JPG文件所在目录路径（直接回车默认使用当前目录）: ").strip()
#     if not jpg_dir:
#         jpg_dir = os.path.dirname(os.path.abspath(__file__))
#
#     stamp_path = input("请输入印章PNG文件的完整路径: ").strip()
#     if not os.path.exists(stamp_path):
#         print("错误：找不到印章文件")
#         return
#
#     # 创建输出目录
#     output_dir = os.path.join(jpg_dir, "JPGOK")
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)
#         print(f"已创建输出目录: {output_dir}")
#
#     # 印章位置坐标
#     position = (1773, 1678)
#     opacity = 0.7
#
#     # 检查并处理JPG文件
#     if not os.path.exists(jpg_dir):
#         print("错误：找不到JPG文件目录")
#         return
#
#     jpg_count = 0
#     for filename in os.listdir(jpg_dir):
#         if filename.lower().endswith(('.jpg', '.jpeg')):
#             input_path = os.path.join(jpg_dir, filename)
#             add_stamp_to_image(input_path, stamp_path, position, output_dir, opacity)
#             print(f"已处理: {filename}")
#             jpg_count += 1
#
#     print(f"\n处理完成！共处理了 {jpg_count} 个文件")
#     print(f"处理后的文件保存在: {output_dir}")
#
#
# if __name__ == "__main__":
#     main()