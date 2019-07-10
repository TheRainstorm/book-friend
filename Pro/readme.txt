cd 到目录为此文件夹目录

virtualenv env #新建名为env的虚拟环境

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

将ChineseAnalyzer.py whoosh_cn_backend.py 复制到
env\Lib\site-packages\haystack\backends