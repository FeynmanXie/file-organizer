import os
import shutil
import logging
from datetime import datetime
from pathlib import Path
import json
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass

@dataclass
class FileOperation:
    """文件操作记录"""
    operation_type: str  # "move" 或 "rename"
    source_path: Path
    target_path: Path
    
class FileOrganizer:
    """智能文件整理工具的核心类"""
    
    def __init__(self, config_path: str = "../config/rules.json"):
        """初始化文件整理器
        
        Args:
            config_path: 配置文件路径，包含文件分类规则
        """
        self.config_path = config_path
        self.rules = self._load_rules()
        self._setup_logging()
        self.operations_history: List[FileOperation] = []
        
    def _setup_logging(self):
        """设置日志记录"""
        log_dir = Path("../logs")
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"file_organizer_{datetime.now().strftime('%Y%m%d')}.log"
        logging.basicConfig(
            filename=str(log_file),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def _load_rules(self) -> Dict:
        """加载分类规则
        
        Returns:
            包含文件分类规则的字典
        """
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.warning(f"配置文件 {self.config_path} 不存在，使用默认规则")
            return self._get_default_rules()
            
    def _get_default_rules(self) -> Dict:
        """获取默认的分类规则
        
        Returns:
            默认的文件分类规则字典
        """
        return {
            "文档": [".doc", ".docx", ".pdf", ".txt", ".md"],
            "图片": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
            "音频": [".mp3", ".wav", ".flac", ".m4a"],
            "视频": [".mp4", ".avi", ".mkv", ".mov"],
            "压缩文件": [".zip", ".rar", ".7z", ".tar", ".gz"],
            "程序": [".exe", ".msi", ".app"],
            "代码": [".py", ".java", ".cpp", ".js", ".html", ".css"]
        }
        
    def preview_organization(self, directory: str) -> Dict[str, List[str]]:
        """预览文件整理结果
        
        Args:
            directory: 要整理的目录路径
            
        Returns:
            预览结果，格式为 {类别: [文件名列表]}
        """
        directory = Path(directory)
        if not directory.exists():
            raise FileNotFoundError(f"目录 {directory} 不存在")
            
        preview_results = {}
        
        for file_path in directory.glob("*"):
            if file_path.is_file():
                category = self._get_file_category(file_path)
                if category:
                    if category not in preview_results:
                        preview_results[category] = []
                    preview_results[category].append(file_path.name)
                    
        return preview_results
        
    def organize_directory(self, 
                         directory: str, 
                         create_dirs: bool = True,
                         progress_callback: Optional[Callable[[int, int], None]] = None) -> Dict:
        """整理指定目录下的文件
        
        Args:
            directory: 要整理的目录路径
            create_dirs: 是否创建分类目录
            progress_callback: 进度回调函数，接收当前处理的文件数和总文件数
            
        Returns:
            整理结果统计
        """
        directory = Path(directory)
        if not directory.exists():
            logging.error(f"目录 {directory} 不存在")
            raise FileNotFoundError(f"目录 {directory} 不存在")
            
        stats = {"总文件数": 0, "已整理": 0, "跳过": 0, "错误": 0}
        self.operations_history.clear()
        
        # 获取所有文件列表
        files = list(directory.glob("*"))
        total_files = len([f for f in files if f.is_file()])
        processed_files = 0
        
        # 遍历目录中的所有文件
        for file_path in files:
            if file_path.is_file():
                stats["总文件数"] += 1
                try:
                    category = self._get_file_category(file_path)
                    if category:
                        if create_dirs:
                            target_dir = directory / category
                            target_dir.mkdir(exist_ok=True)
                            
                            # 确保目标文件名不重复
                            target_path = self._get_unique_path(target_dir / file_path.name)
                            
                            # 记录操作
                            operation = FileOperation(
                                operation_type="move",
                                source_path=file_path,
                                target_path=target_path
                            )
                            
                            # 移动文件
                            shutil.move(str(file_path), str(target_path))
                            self.operations_history.append(operation)
                            
                            logging.info(f"已移动文件 {file_path.name} 到 {category}")
                            stats["已整理"] += 1
                        else:
                            logging.info(f"文件 {file_path.name} 应该移动到 {category}")
                            stats["已整理"] += 1
                    else:
                        logging.info(f"跳过文件 {file_path.name}：未找到匹配的类别")
                        stats["跳过"] += 1
                except Exception as e:
                    logging.error(f"处理文件 {file_path.name} 时出错: {str(e)}")
                    stats["错误"] += 1
                    
                processed_files += 1
                if progress_callback:
                    progress_callback(processed_files, total_files)
                    
        return stats
        
    def undo_operation(self, operation: FileOperation) -> None:
        """撤销文件操作
        
        Args:
            operation: 要撤销的操作
        """
        if operation.operation_type == "move":
            if operation.target_path.exists():
                # 确保源目录存在
                operation.source_path.parent.mkdir(parents=True, exist_ok=True)
                # 移动文件回原位置
                shutil.move(str(operation.target_path), str(operation.source_path))
                logging.info(f"已撤销移动操作：{operation.target_path} -> {operation.source_path}")
            else:
                raise FileNotFoundError(f"无法找到要撤销的文件：{operation.target_path}")
                
    def undo_last_operation(self) -> None:
        """撤销最后一次操作"""
        if self.operations_history:
            operation = self.operations_history.pop()
            self.undo_operation(operation)
        else:
            raise ValueError("没有可撤销的操作")
            
    def _get_file_category(self, file_path: Path) -> Optional[str]:
        """根据文件扩展名确定分类
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件类别，如果没有匹配的类别则返回None
        """
        extension = file_path.suffix.lower()
        for category, extensions in self.rules.items():
            if extension in extensions:
                return category
        return None
        
    def _get_unique_path(self, target_path: Path) -> Path:
        """确保目标路径不重复
        
        Args:
            target_path: 目标文件路径
            
        Returns:
            唯一的文件路径
        """
        if not target_path.exists():
            return target_path
            
        base = target_path.stem
        extension = target_path.suffix
        counter = 1
        
        while True:
            new_path = target_path.parent / f"{base}_{counter}{extension}"
            if not new_path.exists():
                return new_path
            counter += 1
            
    def add_rule(self, category: str, extensions: List[str]) -> None:
        """添加新的分类规则
        
        Args:
            category: 分类名称
            extensions: 文件扩展名列表
        """
        self.rules[category] = extensions
        self._save_rules()
        logging.info(f"已添加新规则：{category} -> {extensions}")
        
    def remove_rule(self, category: str) -> None:
        """删除分类规则
        
        Args:
            category: 要删除的分类名称
        """
        if category in self.rules:
            del self.rules[category]
            self._save_rules()
            logging.info(f"已删除规则：{category}")
        else:
            logging.warning(f"规则 {category} 不存在")
            
    def _save_rules(self) -> None:
        """保存分类规则到配置文件"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.rules, f, ensure_ascii=False, indent=4)
            logging.info("规则已保存到配置文件")
        except Exception as e:
            logging.error(f"保存规则时出错: {str(e)}") 