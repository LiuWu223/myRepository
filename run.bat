@echo off
echo 当前目录:%~dp0
cd %~dp0
TIMEOUT /T 2

if exist "venv" (
	echo "已经安装好python虚拟环境"
	echo 激活虚拟环境
	call "./venv/Scripts/activate"
	TIMEOUT /T 2
) else (
 
	call "./envir_config"
	TIMEOUT /T 2
	call "./envir_config"
	TIMEOUT /T 2
	call "./envir_config"
	TIMEOUT /T 2
)

echo 复制公共接口文件到虚拟环境中
xcopy common venv\Lib\site-packages\self_api\ /s /e /y

python run_task.py
cmd 