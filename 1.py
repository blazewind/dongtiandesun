# @OS:Windows 11
# @Python:3.12.5
# @Coding: UTF-8
# @功能：批量生成号码归属证明
# @时间：2025/5/22-11:11


import pandas as pd
from docx import Document
from datetime import datetime,timedelta
import random
import os

# 生成随机日期
def random_date_between(start_date, end_date):
    """
    生成两个日期之间的随机日期
    :param start_date: 开始日期
    :param end_date: 结束日期
    :return: 随机日期
    """
    # 转换为时间戳
    time_between = end_date - start_date
    days_between = time_between.days
    
    # 生成随机天数
    random_days = random.randrange(days_between)
    
    # 生成随机日期
    random_date = start_date + timedelta(days=random_days)
    
    return random_date

# 设置开始和结束日期
start = datetime(2021, 1, 1)
end = datetime(2025, 3, 31)

# 生成随机日期
random_date = random_date_between(start, end)

# 提取年月日
r_year = random_date.year
r_month = random_date.month
r_day = random_date.day
# 读取Excel文件（请替换为你的实际文件名）
excel_file = 'data.xlsx'
# 如果第一行是标题行，可以这样读取Excel文件
df = pd.read_excel(excel_file, header=0)  # header=0 表示第一行是标题

# 提取并处理数据（假设第一行是标题行）
# 添加数据类型检查和空值处理
numbers = []
for num in df['NUMBERS'].tolist()[1:]:  # 跳过标题行
	if pd.isna(num):
		numbers.append('')  # 空值处理为空字符串
	else:
		numbers.append(str(num))  # 强制转换为字符串

# 修改 companies 的处理部分
companies = []
for comp in df['COMPANY'].tolist():  # 移除 [1:] 以包含第一行数据
    if pd.isna(comp):
        continue  # 跳过空值
    else:
        companies.append(str(comp))  # 强制转换为字符串

# 确保companies列表不为空
if not companies:
    raise ValueError("没有找到有效的公司名称，请检查Excel文件中的COMPANY列数据")

now = datetime.now()
# 分批处理NUMBERS列数据
batch_size = 10
total_batches = (len(numbers) + batch_size - 1) // batch_size
now = datetime.now()
year = now.year
month = now.month
day = now.day
def replace_text_in_paragraph(paragraph, replacements):
    """
    在段落中替换文本，保持格式
    :param paragraph: 段落对象
    :param replacements: 包含替换项的字典
    """
    paragraph_text = paragraph.text
    runs = paragraph.runs
    
    # 检查段落中是否包含任何需要替换的文本
    has_replacements = any(key in paragraph_text for key in replacements.keys())
    if not has_replacements:
        return
    
    # 存储所有运行的文本
    full_text = ''
    for run in runs:
        full_text += run.text
    
    # 执行所有替换
    new_text = full_text
    for key, value in replacements.items():
        if key in new_text:
            new_text = new_text.replace(key, str(value))
    
    # 将新文本分配给第一个运行，清除其他运行
    if runs:
        runs[0].text = new_text
        for run in runs[1:]:
            run.text = ''

# 如果需要确保公司名称不重复，可以在循环开始前添加：
#selected_companies = random.sample(companies, min(len(companies), total_batches))

# 添加文件名清理和重复检测函数
def clean_filename(filename):
    """清理文件名，移除不允许的字符"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '')
    return filename

def get_unique_filename(company_value, current_date, repeat_count=None):
    """
    生成唯一的文件名
    :param company_value: 公司名称
    :param current_date: 当前日期
    :param repeat_count: 重复次数（从1开始）
    """
    # 清理公司名称
    company_name = clean_filename(company_value)
    
    # 基础文件名
    if repeat_count is not None and repeat_count > 0:
        filename = f'{company_name}_号码归属证明_{current_date}_{repeat_count}.docx'
    else:
        filename = f'{company_name}_号码归属证明_{current_date}.docx'
    
    return filename

# 创建可用公司列表（初始包含所有公司）
available_companies = companies.copy()
# 记录公司使用次数
company_usage = {company: 0 for company in companies}

# 修改保存文档的部分
for batch_idx in range(total_batches):
    # 计算当前批次数范围
    start_idx = batch_idx * batch_size
    end_idx = min(start_idx + batch_size, len(numbers))

    # 获取当前批次数据
    current_numbers = numbers[start_idx:end_idx]

    # 合并NUMBERS列为单个字符串，用'、'分隔
    merged_numbers = '、'.join(current_numbers)

    # 读取DOCX模板文件
    template_file = 'numbers.docx'
    doc = Document(template_file)
    
    # 为每个批次生成新的随机日期
    random_date = random_date_between(start, end)
    r_year = random_date.year
    r_month = random_date.month
    r_day = random_date.day
    
    # 随机选择公司名称
    if not available_companies:
        # 如果所有公司都已使用过至少一次，则从所有公司中随机选择
        company_value = random.choice(companies)
    else:
        # 否则从未使用或使用次数较少的公司中选择
        company_value = random.choice(available_companies)
        if company_usage[company_value] == 0:  # 首次使用
            available_companies.remove(company_value)
    
    # 更新使用次数
    company_usage[company_value] += 1
    
    # 替换模板中的占位符
    replacements = {
        '{NUMBERS}': merged_numbers,
        '{COMPANY}': company_value,
        '{YEAR}': str(year),
        '{MONTH}': str(month),
        '{DAY}': str(day),
        '{rYEAR}': str(r_year),
        '{rMONTH}': str(r_month),
        '{rDAY}': str(r_day)
    }

    for paragraph in doc.paragraphs:
        replace_text_in_paragraph(paragraph, replacements)

    # 保存替换后的文档
    current_date = datetime.now().strftime('%Y%m%d')
    
    # 根据使用次数生成文件名
    if company_usage[company_value] > 1:
        # 如果是重复使用，添加序号（使用次数-1作为序号）
        output_file = get_unique_filename(company_value, current_date, company_usage[company_value] - 1)
    else:
        # 首次使用不添加序号
        output_file = get_unique_filename(company_value, current_date)
    
    doc.save(output_file)
    print(f'已生成文件：{output_file}')
    