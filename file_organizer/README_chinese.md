# 语言

[English](README.md) | [中文](README_chinese.md)

# 智能文件整理工具

## 项目简介

这是一个基于Python开发的智能文件整理工具，旨在帮助用户自动整理和分类文件夹中的文件。通过可自定义的规则系统，用户可以轻松地将各种类型的文件自动分类到不同的目录中。

本工具采用现代化的图形用户界面，支持实时预览、进度显示、操作撤销等功能，让文件整理工作变得简单高效。

### 主要特点

- 自动识别和分类各种类型的文件
- 可自定义文件分类规则
- 现代化的图形用户界面
- 详细的整理过程日志
- 防止文件名冲突
- 支持批量处理
- 实时进度显示
- 文件整理预览
- 支持撤销操作
- 规则导入/导出功能
- 规则搜索功能
- 快捷键支持

## 系统要求

### 基本要求

- 操作系统：Windows 7或更高版本 / macOS 10.12或更高版本 / Linux (主流发行版)
- Python版本：3.6或更高版本
- 磁盘空间：至少50MB可用空间
- 内存：至少2GB RAM

### Python依赖

- tkinter >= 8.6
- pathlib >= 1.0.1
- typing >= 3.7.4
- dataclasses >= 0.8 (Python 3.6)

## 详细安装步骤

1. 确保系统已安装Python 3.6或更高版本：
```bash
python --version
```

2. 下载或克隆项目：
```bash
git clone https://github.com/FeynmanXie/file-organizer.git
cd file-organizer
```

3. 创建虚拟环境（推荐）：
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

4. 安装依赖包：
```bash
pip install -r requirements.txt
```

5. 验证安装：
```bash
cd project/src
python gui.py
```

## 使用指南

### 基本使用

1. 启动程序：
   - 双击运行 `project/src/gui.py`
   - 或在命令行中运行：
     ```bash
     cd project/src
     python gui.py
     ```

2. 选择要整理的目录：
   - 点击"浏览"按钮
   - 或使用快捷键 Ctrl+O
   - 选择需要整理的文件夹

3. 管理分类规则：
   - 查看现有规则
   - 使用搜索框快速查找规则
   - 添加/编辑/删除规则
   - 导入/导出规则配置

4. 整理文件：
   - 点击"预览整理结果"查看文件将如何被分类
   - 点击"开始整理"执行文件整理
   - 使用"撤销上次操作"恢复文件位置

### 快捷键

- Ctrl+N：添加新规则
- Ctrl+D：删除规则
- Ctrl+E：编辑规则
- Ctrl+O：打开目录
- Ctrl+Z：撤销上次操作

### 默认分类规则

程序默认包含以下分类：

| 类别 | 文件扩展名 |
|------|------------|
| 文档 | .doc, .docx, .pdf, .txt, .md |
| 图片 | .jpg, .jpeg, .png, .gif, .bmp |
| 音频 | .mp3, .wav, .flac, .m4a |
| 视频 | .mp4, .avi, .mkv, .mov |
| 压缩文件 | .zip, .rar, .7z, .tar, .gz |
| 程序 | .exe, .msi, .app |
| 代码 | .py, .java, .cpp, .js, .html, .css |

### 自定义规则

1. 添加规则：
   - 点击"添加规则"按钮
   - 输入类别名称
   - 输入文件扩展名（用逗号分隔）
   - 点击保存

2. 编辑规则：
   - 选择要编辑的规则
   - 点击"编辑规则"按钮
   - 修改类别名称或扩展名
   - 点击保存

3. 删除规则：
   - 选择要删除的规则
   - 点击"删除规则"按钮
   - 确认删除

4. 导入/导出规则：
   - 点击"导入规则"从其他配置文件导入规则
   - 点击"导出规则"保存当前规则配置

## 项目结构

```
project/
├── src/          # 源代码
│   ├── file_organizer.py  # 核心功能实现
│   └── gui.py            # 图形界面实现
├── tests/        # 测试代码
├── docs/         # 文档
├── config/       # 配置文件
│   └── rules.json       # 分类规则配置
├── assets/       # 静态资源
│   └── icon.ico        # 程序图标
├── logs/         # 日志文件
└── README.md     # 项目说明
```

## 开发者指南

### 环境设置

1. 克隆项目并设置开发环境：
```bash
git clone https://github.com/FeynmanXie/file-organizer.git
cd file-organizer
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

2. 安装开发依赖：
```bash
pip install pytest pytest-cov pylint black
```

### 代码风格

- 遵循PEP 8规范
- 使用Black进行代码格式化
- 使用pylint进行代码质量检查
- 保持函数和方法的文档字符串更新

### 测试

运行测试：
```bash
pytest tests/
```

生成测试覆盖率报告：
```bash
pytest --cov=src tests/
```

## 故障排除

### 常见问题

1. 程序无法启动
   - 检查Python版本是否满足要求
   - 确认所有依赖包已正确安装
   - 检查日志文件中的错误信息

2. 无法选择目录
   - 确认用户对目标目录有读写权限
   - 检查目录路径是否包含特殊字符

3. 规则不生效
   - 检查规则格式是否正确
   - 确认文件扩展名前有点号(.)
   - 验证rules.json文件的完整性

4. 文件整理失败
   - 检查目标目录的写入权限
   - 确认没有文件被其他程序占用
   - 查看日志文件了解详细错误信息

### 日志位置

日志文件保存在 `logs` 目录下，格式为 `file_organizer_YYYYMMDD.log`。

## 安全注意事项

1. 文件安全
   - 在整理重要文件前先备份
   - 程序不会删除任何文件，只会移动文件位置
   - 如果目标位置存在同名文件，会自动重命名

2. 权限要求
   - 程序需要对源目录和目标目录有读写权限
   - 不建议使用管理员权限运行程序

## 更新日志

### v1.0.0 (2025-01-12)
- 初始版本发布
- 实现基本的文件整理功能
- 添加图形用户界面
- 支持自定义规则
- 添加预览和撤销功能

### v1.1.0 (计划中，最多下个月更新)
- 添加更多文件类型支持
- 优化性能
- 改进用户界面
- 添加批量规则导入功能

## 贡献指南

我们欢迎各种形式的贡献，包括但不限于：

- 报告问题和建议
- 提交代码改进
- 完善文档
- 添加新功能
- 修复bug

### 贡献步骤

1. Fork项目
2. 创建特性分支
3. 提交改动
4. 推送到分支
5. 创建Pull Request

### 提交规范

- 使用清晰的提交信息
- 保持提交粒度适中
- 确保代码通过所有测试
- 更新相关文档

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 作者

[Feynman]
- Email: woshixieruiman@gmail.com
- GitHub: [@FeynmanXie](https://github.com/FeynmanXie)

## 致谢

感谢所有为这个项目做出贡献的开发者。 