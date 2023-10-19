echo 创建python虚拟环境
python -m venv venv
TIMEOUT /T 2

echo 激活虚拟环境
call "./venv/Scripts/activate"
TIMEOUT /T 2

echo 更新pip版本
python -m pip install --upgrade pip
pip list
TIMEOUT /T 2

echo 安装python依赖包
pip install airtest
pip install --upgrade --pre uiautomator2
pip install pandas
pip install pytest
pip install pytest-assume
pip install pytest-repeat
pip install pytest-testreport
pip install pytest-rerunfailures
pip install openpyxl
pip install flask==2.3.3
pip install Flask-Cors==4.0.0
TIMEOUT /T 2

echo 查看当前python环境的依赖包
pip list
TIMEOUT /T 2

echo 复制公共接口文件到虚拟环境中
xcopy common venv\Lib\site-packages\self_api\ /s /e /y
