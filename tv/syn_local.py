import os
import subprocess
import datetime
import re
import shutil
import filecmp

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

# 5. 同步文件
print("正在同步IPTV文件...")
files_to_sync = ['iptv4.txt', 'iptv4.m3u', 'iptv6.txt', 'iptv6.m3u']
source_dir = '/docker/iptv4/'

for file_name in files_to_sync:
    source_path = os.path.join(source_dir, file_name)
    target_path = os.path.join(script_path, file_name)
    
    if os.path.exists(source_path):
        try:
            # 检查目标文件是否存在且内容是否相同
            if os.path.exists(target_path):
                if filecmp.cmp(source_path, target_path, shallow=False):
                    print(f"文件 {file_name} 内容相同，跳过同步")
                    continue
                else:
                    print(f"文件 {file_name} 内容不同，进行覆盖同步")
            else:
                print(f"目标文件 {file_name} 不存在，进行首次同步")
            
            shutil.copy2(source_path, target_path)
            print(f"成功同步文件: {file_name} 从 {source_dir} 到 {script_path}")
        except Exception as e:
            print(f"同步文件 {file_name} 时出错: {str(e)}")
    else:
        print(f"警告：源文件 {source_path} 不存在，跳过同步")

# 6. 下载文件列表 - 已移至 iptv_download_merge.py
print("跳过下载文件步骤，请使用 iptv_download_merge.py 进行文件下载")

# 7. 合并文件 - 已移至 iptv_download_merge.py
print("跳过文件合并步骤，请使用 iptv_download_merge.py 进行文件合并")

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

# 8.5 执行 Python 脚本
def execute_python_script(script_name):
    print(f"正在执行 {script_name}...")
    try:
        script_path_full = os.path.join(script_path, script_name)
        if os.path.exists(script_path_full):
            # 根据操作系统选择 Python 命令
            if os.name == 'nt':  # Windows
                python_cmd = 'python'
            else:  # Linux
                python_cmd = 'python3'
            
            command = f'{python_cmd} "{script_path_full}"'
            try:
                run_command(command, cwd=script_path)  # 添加 cwd 参数
                print(f"{script_name} 执行完成")
            except Exception as e:
                print(f"{script_name} 执行出错: {str(e)}")
                if os.name == 'nt':  # 只在 Windows 上尝试备选命令
                    alt_python_cmd = 'python3'
                    alt_command = f'{alt_python_cmd} "{script_path_full}"'
                    try:
                        run_command(alt_command, cwd=script_path)
                        print(f"{script_name} 使用备选命令执行完成")
                    except Exception as e2:
                        print(f"{script_name} 备选命令执行也失败: {str(e2)}")
                        return False
                else:
                    return False
        else:
            print(f"警告：{script_name} 文件不存在")
            return False
    except Exception as e:
        print(f"执行 {script_name} 时出错: {str(e)}")
        return False
    return True

# 依次执行三个Python脚本
scripts_to_execute = ['indexnow-live.py', 'indexnow-www.py']
for script in scripts_to_execute:
    success = execute_python_script(script)
    if not success:
        print(f"警告：{script} 执行失败，继续执行下一个脚本")

# 9. 提交更改并推送到 GitHub
print("正在提交更改并推送...")
try:
    output = run_command('git status', cwd=repo_root)
    print(f"Git 状态:\n{output}")

    if "nothing to commit" not in output:
        output = run_command('git add .', cwd=repo_root)
        print(f"Git add 输出:\n{output}")

        commit_message = f"更新IPTV4/IPV6最新可用直播源和相关文件-by_debian100 {current_time}"
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