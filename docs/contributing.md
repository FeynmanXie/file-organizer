# 贡献指南

欢迎为智能文件整理工具做出贡献！这份文档将帮助你了解如何参与项目开发。

## 目录

1. [行为准则](#行为准则)
2. [开始贡献](#开始贡献)
3. [开发流程](#开发流程)
4. [提交规范](#提交规范)
5. [代码规范](#代码规范)
6. [测试规范](#测试规范)
7. [文档规范](#文档规范)
8. [发布流程](#发布流程)

## 行为准则

### 基本原则

- 尊重所有贡献者
- 友善交流
- 接受建设性批评
- 关注问题本身
- 包容不同观点

### 不当行为

- 人身攻击
- 骚扰言论
- 歧视言论
- 垃圾信息
- 恶意破坏

## 开始贡献

### 准备工作

1. Fork项目仓库
2. 克隆你的Fork:
```bash
git clone https://github.com/your-username/file-organizer.git
```

3. 添加上游仓库:
```bash
git remote add upstream https://github.com/original-owner/file-organizer.git
```

4. 创建虚拟环境:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

5. 安装依赖:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 选择任务

1. 查看Issues
   - 寻找带有"good first issue"标签的任务
   - 阅读任务描述和讨论
   - 在开始工作前留言

2. 提出新想法
   - 创建新Issue
   - 详细描述功能或问题
   - 等待维护者反馈

## 开发流程

### 分支管理

1. 主要分支
   - `main`: 稳定版本
   - `develop`: 开发版本
   - `feature/*`: 新功能
   - `bugfix/*`: 错误修复
   - `release/*`: 发布准备

2. 开发新功能
```bash
git checkout develop
git pull upstream develop
git checkout -b feature/your-feature
```

3. 修复bug
```bash
git checkout develop
git pull upstream develop
git checkout -b bugfix/bug-description
```

### 开发步骤

1. 编写代码
   - 遵循代码规范
   - 添加必要注释
   - 保持代码简洁

2. 本地测试
   - 运行单元测试
   - 检查代码风格
   - 验证功能

3. 提交更改
   - 遵循提交规范
   - 保持提交原子性
   - 写清晰的提交信息

4. 推送更改
```bash
git push origin your-branch
```

5. 创建Pull Request
   - 填写PR模板
   - 关联相关Issue
   - 等待代码审查

## 提交规范

### 提交信息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 类型(type)

- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建/工具

### 范围(scope)

- `gui`: 图形界面
- `core`: 核心功能
- `utils`: 工具函数
- `docs`: 文档
- `tests`: 测试

### 示例

```
feat(gui): 添加文件拖放支持

- 支持将文件/文件夹拖放到主窗口
- 自动开始文件分类预览
- 添加拖放提示效果

Closes #123
```

## 代码规范

### Python规范

1. 代码风格
   - 遵循PEP 8
   - 使用4空格缩进
   - 限制行长度为79字符

2. 命名规范
   - 类名使用CamelCase
   - 函数和变量使用snake_case
   - 常量使用大写字母

3. 文档字符串
   - 所有公共API都需要文档
   - 使用Google风格
   - 包含参数和返回值说明

### 示例

```python
def process_file(file_path: str) -> bool:
    """
    处理单个文件。

    Args:
        file_path: 要处理的文件路径。

    Returns:
        bool: 处理是否成功。

    Raises:
        FileNotFoundError: 文件不存在。
    """
    pass
```

## 测试规范

### 测试原则

1. 测试覆盖
   - 所有新功能都需要测试
   - 所有bug修复都需要测试用例
   - 保持高测试覆盖率

2. 测试类型
   - 单元测试
   - 集成测试
   - 功能测试

### 编写测试

1. 测试文件命名
   - `test_*.py`
   - `*_test.py`

2. 测试类命名
   - `Test*`

3. 测试方法命名
   - `test_*`

### 示例

```python
class TestFileOrganizer:
    def setup_method(self):
        self.organizer = FileOrganizer()

    def test_organize_directory(self):
        # 准备测试数据
        # 执行测试
        # 验证结果
        pass
```

## 文档规范

### 文档类型

1. 代码文档
   - 文档字符串
   - 行内注释
   - 模块文档

2. API文档
   - 接口说明
   - 参数描述
   - 示例代码

3. 用户文档
   - 安装指南
   - 使用教程
   - 常见问题

### 文档风格

1. 清晰简洁
   - 使用简单的语言
   - 避免专业术语
   - 提供具体示例

2. 结构合理
   - 层次分明
   - 重点突出
   - 易于导航

3. 及时更新
   - 同步代码变化
   - 修正错误信息
   - 补充新功能

## 发布流程

### 版本号规范

使用语义化版本：
- 主版本号：不兼容的API修改
- 次版本号：向下兼容的功能性新增
- 修订号：向下兼容的问题修正

### 发布步骤

1. 准备工作
   - 更新版本号
   - 更新CHANGELOG
   - 更新文档

2. 测试验证
   - 运行所有测试
   - 检查代码覆盖率
   - 进行手动测试

3. 创建发布
   - 创建发布分支
   - 打包代码
   - 发布到PyPI

4. 发布后
   - 合并到main分支
   - 创建版本标签
   - 更新develop分支 