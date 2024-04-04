import os

# 获取文件大小
file_size = os.path.getsize('/root/iptv/dsyy/itvlist.txt')

# 如果文件大小小于 5KB，则退出脚本
if file_size < 5 * 1024:
    print("File size is less than 5KB. Exiting the script.")
    exit()

# 打开原始文件进行读取
with open('/root/iptv/dsyy/itvlist.txt', 'r') as original_file:
    original_content = original_file.read()

# 检查是否存在JD,#genre#
if 'HD,#genre#' in original_content:
    print("HD,#genre# already exists before ,#genre#, no need to modify.")
    exit()

# 在原始内容中进行修改
lines = original_content.split('\n')
modified_lines = []
for line in lines:
    if ',#genre#' in line:
        line = line.replace(',#genre#', 'JD,#genre#')
    modified_lines.append(line)

# 将修改后的内容写入到新的文件中
modified_content = '\n'.join(modified_lines)
with open('/root/iptv/dsyy/itvlist_modified.txt', 'w') as modified_file:
    modified_file.write(modified_content)

# 打开 hd.txt 文件，删除指定行后的内容并写入新内容
with open('/root/iptv/dsyy/hd.txt', 'r') as hd_file:
    lines = hd_file.readlines()

# 找到指定行并删除之后的内容
found_line = False
modified_lines = []
for line in lines:
    if "rtsp://115.153.254.81/PLTV/88888888/224/3221227003/88888888.smil" in line:
        found_line = True
        # 找到目标行后，停止添加内容到 modified_lines 中
        modified_lines.append(line)  # 添加目标行本身
        break
    # 将当前行添加到 modified_lines 中
    modified_lines.append(line)

# 将修改后的内容写入到 hd.txt 文件中
with open('/root/iptv/dsyy/hd.txt', 'w') as hd_file:
    hd_file.writelines(modified_lines)

# 如果 modified_content 不为空，追加到 hd.txt 文件的最后一行
if modified_content.strip():  # 检查 modified_content 是否为空或只包含空白字符
    # 打开 hd.txt 文件，追加修改后的内容到最后一行
    with open('/root/iptv/dsyy/hd.txt', 'a') as hd_file:
        hd_file.write('\n' + modified_content)
