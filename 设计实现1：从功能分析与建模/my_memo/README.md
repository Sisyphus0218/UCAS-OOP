# My Memo

My Memo 是一个用简单的便签软件。使用 Python 编写，主要使用了 PyQt5 开发图形界面。

## 环境配置

创建虚拟环境，比如使用 Conda：

```
conda create -n memo_env python=3.11
conda activate memo_env
```

cd 到 my_memo 目录，安装剩余的包

```
pip install -r requirements.txt
```

注：主要使用的包有 PyQt5，Pillow 和 beautifulsoup4

## 项目结构

文件夹说明：

| 文件夹 | 描述                                                         |
| ------ | ------------------------------------------------------------ |
| assets | 在便签中插入图片后，程序会在该文件夹下创建图片副本。删除便签后，相应的图片副本也会自动删除。 |
| icon   | 便签使用的图标。                                             |
| memo   | 便签文件。                                                   |

重要文件说明：

| 文件                   | 描述                                       |
| ---------------------- | ------------------------------------------ |
| memo_app.py            | 主程序，管理所有窗口以及便签信息           |
| memo.py                | 便签列表窗口和便签窗口                     |
| memo_item.py           | 便签列表项                                 |
| memo_setting_window.py | 便签设置窗口                               |
| memo_info.json         | 便签信息，包括便签名、便签包含的图片路径等 |

