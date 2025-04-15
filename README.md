# streamlit-effmap
根据excel表格数据生成效率map图
可以访问的地址：http://121.36.209.159:8501/
笔者服务器系统版本：CentOS 7.6 64bit
部署方法：
1.使用FileZilla上传文件
文件结构目录为：
  streamlit-effmap
    ├── efficiency_map.py  #功能代码
    ├── app.py  #主程序入口
    ├── temp_uploads/
    └── output/
2.安装Python3
3.进入项目目录
4.配置虚拟环境
5.新建配置文件（设置端口号）
6.配置服务器的防火墙和安全组
7.运行主程序入口
  streamlit run app.py --server.port 8501 --server.address 0.0.0.0
8.访问ip
![picture](https://github.com/user-attachments/assets/08e72df0-97bb-4dd7-bf71-a03f9598ab00)
