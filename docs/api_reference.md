# API参考文档

## 目录

1. [FileOrganizer类](#fileorganizer类)
2. [FileOrganizerGUI类](#fileorganizergui类)
3. [工具函数](#工具函数)
4. [数据类型](#数据类型)
5. [异常类](#异常类)

## FileOrganizer类

### 类定义

```python
class FileOrganizer:
    """
    文件整理器的核心类，负责文件分类和整理操作。
    """
```

### 构造函数

```python
def __init__(self, rules_file: str = None):
    """
    初始化文件整理器。

    Args:
        rules_file (str, optional): 规则文件的路径。如果不提供，将使用默认规则。

    Raises:
        FileNotFoundError: 规则文件不存在。
        JSONDecodeError: 规则文件格式错误。
    """
```

### 公共方法

#### organize_directory

```python
def organize_directory(
    self,
    directory: str,
    progress_callback: Callable[[int, int], None] = None
) -> None:
    """
    整理指定目录下的文件。

    Args:
        directory (str): 要整理的目录路径。
        progress_callback (callable, optional): 进度回调函数，接收两个参数：
            - current (int): 当前处理的文件数
            - total (int): 总文件数

    Raises:
        FileNotFoundError: 目录不存在。
        PermissionError: 没有足够的权限。
        OSError: 文件操作失败。
    """
```

#### preview_organization

```python
def preview_organization(self, directory: str) -> dict:
    """
    预览文件整理结果。

    Args:
        directory (str): 要预览的目录路径。

    Returns:
        dict: 预览结果，格式为：
            {
                "category1": ["file1", "file2"],
                "category2": ["file3", "file4"]
            }

    Raises:
        FileNotFoundError: 目录不存在。
        PermissionError: 没有足够的权限。
    """
```

#### undo_last_operation

```python
def undo_last_operation(self) -> bool:
    """
    撤销上一次整理操作。

    Returns:
        bool: 撤销是否成功。

    Raises:
        OSError: 文件操作失败。
    """
```

#### add_rule

```python
def add_rule(self, category: str, extensions: List[str]) -> None:
    """
    添加新的分类规则。

    Args:
        category (str): 类别名称。
        extensions (List[str]): 文件扩展名列表。

    Raises:
        ValueError: 类别名称为空或扩展名格式错误。
    """
```

#### remove_rule

```python
def remove_rule(self, category: str) -> bool:
    """
    删除指定类别的规则。

    Args:
        category (str): 要删除的类别名称。

    Returns:
        bool: 删除是否成功。
    """
```

#### save_rules

```python
def save_rules(self, file_path: str) -> None:
    """
    保存当前规则到文件。

    Args:
        file_path (str): 保存路径。

    Raises:
        PermissionError: 没有写入权限。
        OSError: 文件操作失败。
    """
```

#### load_rules

```python
def load_rules(self, file_path: str) -> None:
    """
    从文件加载规则。

    Args:
        file_path (str): 规则文件路径。

    Raises:
        FileNotFoundError: 文件不存在。
        JSONDecodeError: 文件格式错误。
    """
```

## FileOrganizerGUI类

### 类定义

```python
class FileOrganizerGUI:
    """
    文件整理器的图形用户界面类。
    """
```

### 构造函数

```python
def __init__(self):
    """
    初始化图形界面。
    """
```

### 公共方法

#### run

```python
def run(self) -> None:
    """
    启动图形界面。
    """
```

### 私有方法

#### _browse_directory

```python
def _browse_directory(self) -> None:
    """
    打开目录选择对话框。
    """
```

#### _load_rules

```python
def _load_rules(self) -> None:
    """
    加载分类规则。
    """
```

#### _add_rule_dialog

```python
def _add_rule_dialog(self) -> None:
    """
    显示添加规则对话框。
    """
```

#### _edit_rule_dialog

```python
def _edit_rule_dialog(self, category: str) -> None:
    """
    显示编辑规则对话框。

    Args:
        category (str): 要编辑的规则类别。
    """
```

#### _remove_rule

```python
def _remove_rule(self) -> None:
    """
    删除选中的规则。
    """
```

#### _preview_organization

```python
def _preview_organization(self) -> None:
    """
    预览文件整理结果。
    """
```

#### _start_organization

```python
def _start_organization(self) -> None:
    """
    开始文件整理。
    """
```

#### _update_progress

```python
def _update_progress(self, current: int, total: int) -> None:
    """
    更新进度显示。

    Args:
        current (int): 当前处理的文件数。
        total (int): 总文件数。
    """
```

## 工具函数

### get_file_extension

```python
def get_file_extension(file_path: str) -> str:
    """
    获取文件扩展名。

    Args:
        file_path (str): 文件路径。

    Returns:
        str: 文件扩展名（包含点号）。
    """
```

### create_directory_if_not_exists

```python
def create_directory_if_not_exists(path: str) -> None:
    """
    如果目录不存在则创建。

    Args:
        path (str): 目录路径。

    Raises:
        PermissionError: 没有创建目录的权限。
    """
```

### setup_logging

```python
def setup_logging() -> logging.Logger:
    """
    配置日志系统。

    Returns:
        logging.Logger: 配置好的日志器实例。
    """
```

### validate_path

```python
def validate_path(path: str) -> bool:
    """
    验证路径是否有效且可访问。

    Args:
        path (str): 要验证的路径。

    Returns:
        bool: 路径是否有效。
    """
```

## 数据类型

### FileOperation

```python
@dataclass
class FileOperation:
    """
    文件操作记录。

    Attributes:
        operation_type (str): 操作类型（'move'或'copy'）。
        source_path (str): 源文件路径。
        target_path (str): 目标文件路径。
        timestamp (datetime): 操作时间戳。
    """
    operation_type: str
    source_path: str
    target_path: str
    timestamp: datetime = field(default_factory=datetime.now)
```

### Rule

```python
@dataclass
class Rule:
    """
    文件分类规则。

    Attributes:
        category (str): 类别名称。
        extensions (List[str]): 文件扩展名列表。
        enabled (bool): 规则是否启用。
    """
    category: str
    extensions: List[str]
    enabled: bool = True
```

## 异常类

### RuleValidationError

```python
class RuleValidationError(Exception):
    """
    规则验证错误。
    """
    pass
```

### FileOperationError

```python
class FileOperationError(Exception):
    """
    文件操作错误。

    Attributes:
        message (str): 错误信息。
        file_path (str): 相关文件路径。
    """
    def __init__(self, message: str, file_path: str):
        self.message = message
        self.file_path = file_path
        super().__init__(f"{message}: {file_path}")
```

### ConfigurationError

```python
class ConfigurationError(Exception):
    """
    配置错误。
    """
    pass
``` 