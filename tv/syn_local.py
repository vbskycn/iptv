import os
import subprocess
import requests
import datetime
import re

# 获取脚本所在目录
script_path = os.path.dirname(os.path.abspath(__file__))
# 获取仓库根目录（脚本所在目录的上一级）
repo_root = os.path.dirname(script_path)

def run_command(command, cwd=None):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=cwd)
    output, error = process.communicate()
    if process.returncode != 0:
        print(f"错误: {error.decode('utf-8')}")
        exit(1)
    return output.decode('utf-8').strip()

def print_current_time(message):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{message} {current_time}")

# 1. 获取脚本所在路径和系统时间日期
print(f"脚本所在路径：{script_path}")
print_current_time("系统时间：")

# 2. 切换到程序所在目录
os.chdir(script_path)
print("切换到程序所在目录...")

# 3. 设置 Git 用户名和邮箱
run_command('git config user.name "vbskycn"', cwd=repo_root)
run_command('git config user.email "zhoujie218@gmail.com"', cwd=repo_root)

# 4. 执行 Git 操作，放弃本地更改并拉取最新代码
print("正在执行 Git 操作...")
run_command('git fetch origin', cwd=repo_root)
run_command('git reset --hard origin/master', cwd=repo_root)
run_command('git clean -fd', cwd=repo_root)
run_command('git pull', cwd=repo_root)

# 5. 下载文件列表
print("正在下载文件...")
files_to_download = [
    {
        "url": "https://mycode.zhoujie218.top/me/jxdx_hd.txt",
        "filename": "jxdx_hd.txt"
    },
    {
        "url": "https://mycode.zhoujie218.top/me/jxdx_hd.m3u",
        "filename": "jxdx_hd.m3u"
    },
    # 在这里添加更多的文件下载信息
    # 例如：
    # {
    #     "url": "https://example.com/another_file.txt",
    #     "filename": "another_file.txt"
    # },
]

for file_info in files_to_download:
    url = file_info["url"]
    filename = file_info["filename"]
    file_path = os.path.join(script_path, filename)

    print(f"正在下载 {filename} 文件...")
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"成功下载并保存 {filename} 到 {file_path}")
    else:
        print(f"下载失败 {filename}, 状态码: {response.status_code}")
        exit(1)

# 6. 同步文件
print("正在同步文件...")
files_to_sync = ['iptv4.txt', 'iptv4.m3u', 'iptv6.txt', 'iptv6.m3u']
for file in files_to_sync:
    source = f"/docker/iptv4/{file}"
    destination = os.path.join(script_path, file)
    run_command(f'cp {source} {destination}')

# 7. 合并文件
print("正在合并文件...")
output_file = os.path.join(script_path, 'hd.txt')

# 定义文件合并顺序
merge_order = ['iptv6.txt', 'iptv4.txt']

replacements = {
    'iptv6.txt': 'ip6,#genre#',
    'iptv4.txt': 'ip4,#genre#'
}

with open(output_file, 'w', encoding='utf-8') as outfile:
    for filename in merge_order:
        filepath = os.path.join(script_path, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as infile:
                content = infile.read()
                if filename in replacements:
                    content = content.replace(',#genre#', replacements[filename])
                outfile.write(content)
                outfile.write('\n')
        else:
            print(f'警告：文件 {filepath} 不存在，已跳过')

print(f'文件已合并到 {output_file}')

# 8. 更新 README.md 文件
print("正在更新 README.md 文件...")
readme_path = os.path.join(repo_root, 'README.md')
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

try:
    with open(readme_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    print(f"README.md 文件内容长度: {len(content)} 字符")

    # 更新 IPTV6 时间
    iptv6_pattern = r'<!-- UPDATE_TIME_IPTV6 -->本次更新时间:.*?<!-- END_UPDATE_TIME_IPTV6 -->'
    new_iptv6 = f'<!-- UPDATE_TIME_IPTV6 -->本次更新时间: {current_time}<!-- END_UPDATE_TIME_IPTV6 -->'
    content, iptv6_count = re.subn(iptv6_pattern, new_iptv6, content)

    # 更新 IPTV4 时间
    iptv4_pattern = r'<!-- UPDATE_TIME_IPTV4 -->本次更新时间:.*?<!-- END_UPDATE_TIME_IPTV4 -->'
    new_iptv4 = f'<!-- UPDATE_TIME_IPTV4 -->本次更新时间: {current_time}<!-- END_UPDATE_TIME_IPTV4 -->'
    content, iptv4_count = re.subn(iptv4_pattern, new_iptv4, content)

    print(f"IPTV6 更新: {'成功' if iptv6_count > 0 else '失败'}")
    print(f"IPTV4 更新: {'成功' if iptv4_count > 0 else '失败'}")

    if iptv6_count > 0 or iptv4_count > 0:
        with open(readme_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"README.md 文件更新后内容长度: {len(content)} 字符")
        print("README.md 文件已更新")
    else:
        print("没有找到需要更新的时间标记，README.md 文件未修改")

except Exception as e:
    print(f"更新 README.md 文件时出错: {str(e)}")
    exit(1)

# 9. 提交更改并推送到 GitHub
print("正在提交更改并推送...")
try:
    output = run_command('git status', cwd=repo_root)
    print(f"Git 状态:\n{output}")

    if "nothing to commit" not in output:
        output = run_command('git add .', cwd=repo_root)
        print(f"Git add 输出:\n{output}")

        commit_message = f"debian100 {current_time} - 同步IPTV4仓库文件和处理新文件"
        output = run_command(f'git commit -m "{commit_message}"', cwd=repo_root)
        print(f"Git commit 输出:\n{output}")

        output = run_command('git push', cwd=repo_root)
        print(f"Git push 输出:\n{output}")

        print("更改已成功提交并推送到 GitHub")
    else:
        print("没有需要提交的更改")

except Exception as e:
    print(f"Git 操作失败: {str(e)}")
    exit(1)

print("脚本执行完成")