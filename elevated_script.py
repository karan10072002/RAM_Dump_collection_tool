import subprocess
import ctypes
import os
import sys

file_name = r"os_detection.py"
file_path = os.path.join(os.getcwd(), file_name)

def run_as_admin_UNIX(file_path):
    # _file_="for_linux_admin.py"
    if os.geteuid() != 0:
        subprocess.call(['sudo', 'python3', os.path.abspath(file_path)])
        sys.exit()

try:
    # trying to get windows admin privilages
    is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    if is_admin:
        command = f'python "{file_path}"'
        os.system(command)
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, file_name, None, 1)

except:
    # trying to get linux admin privilages
    run_as_admin_UNIX(file_path)



