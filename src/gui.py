import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.font import Font
from pathlib import Path
import json
from typing import Dict, List, Any
import threading
from file_organizer import FileOrganizer
import os
import sys
import logging

class ModernTheme:
    """现代化主题配置"""
    BACKGROUND = "#f0f0f0"
    BUTTON_BG = "#2196F3"
    BUTTON_FG = "white"
    HOVER_BG = "#1976D2"
    FONT = ("Microsoft YaHei UI", 10)
    TITLE_FONT = ("Microsoft YaHei UI", 12, "bold")

class FileOrganizerGUI:
    """文件整理工具的图形界面"""
    
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("智能文件整理工具")
        self.window.geometry("900x700")
        self.window.configure(bg=ModernTheme.BACKGROUND)
        
        # 设置窗口图标
        try:
            # 尝试多个可能的图标路径
            possible_paths = [
                Path("assets/icon.ico"),  # 直接运行时的路径
                Path("../assets/icon.ico"),  # 从src目录运行时的路径
                Path(os.path.dirname(sys.executable)) / "assets/icon.ico",  # 打包后的路径
                Path(sys._MEIPASS) / "assets/icon.ico" if hasattr(sys, '_MEIPASS') else None  # PyInstaller打包后的路径
            ]
            
            icon_set = False
            for path in possible_paths:
                if path and path.exists():
                    self.window.iconbitmap(str(path))
                    icon_set = True
                    break
                    
            if not icon_set:
                logging.warning("未找到图标文件")
                
        except Exception as e:
            logging.warning(f"无法加载图标: {str(e)}")
            
        # 创建文件整理器实例
        self.organizer = FileOrganizer()
        
        # 初始化变量
        self.is_organizing = False
        self.undo_stack = []
        
        self._setup_styles()
        self._create_widgets()
        self._load_rules()
        self._setup_shortcuts()
        
    def _setup_styles(self):
        """设置自定义样式"""
        style = ttk.Style()
        style.configure("Modern.TButton",
                       font=ModernTheme.FONT,
                       padding=5)
        style.configure("Modern.TLabel",
                       font=ModernTheme.FONT,
                       background=ModernTheme.BACKGROUND)
        style.configure("Title.TLabel",
                       font=ModernTheme.TITLE_FONT,
                       background=ModernTheme.BACKGROUND)
        style.configure("Modern.Treeview",
                       font=ModernTheme.FONT,
                       rowheight=25)
        style.configure("Modern.Treeview.Heading",
                       font=ModernTheme.FONT)
                       
    def _setup_shortcuts(self):
        """设置键盘快捷键"""
        self.window.bind("<Control-n>", lambda e: self._add_rule_dialog())
        self.window.bind("<Control-d>", lambda e: self._remove_rule())
        self.window.bind("<Control-e>", lambda e: self._edit_rule_dialog())
        self.window.bind("<Control-o>", lambda e: self._browse_directory())
        self.window.bind("<Control-z>", lambda e: self._undo_last_operation())
        
    def _browse_directory(self):
        """打开目录选择对话框"""
        directory = filedialog.askdirectory()
        if directory:
            self.directory_var.set(directory)
            
    def _load_rules(self):
        """加载并显示分类规则"""
        self.rules_tree.delete(*self.rules_tree.get_children())
        for category, extensions in self.organizer.rules.items():
            self.rules_tree.insert("", tk.END, values=(category, ", ".join(extensions)))
            
    def _add_rule_dialog(self):
        """显示添加规则对话框"""
        dialog = tk.Toplevel(self.window)
        dialog.title("添加规则")
        dialog.geometry("400x200")
        dialog.configure(bg=ModernTheme.BACKGROUND)
        
        ttk.Label(dialog, 
                 text="类别名称：",
                 style="Modern.TLabel").grid(row=0, column=0, padx=5, pady=5)
        category_var = tk.StringVar()
        ttk.Entry(dialog, 
                 textvariable=category_var,
                 font=ModernTheme.FONT).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, 
                 text="文件扩展名：\n(用逗号分隔，如 .txt,.doc)",
                 style="Modern.TLabel").grid(row=1, column=0, padx=5, pady=5)
        extensions_var = tk.StringVar()
        ttk.Entry(dialog, 
                 textvariable=extensions_var,
                 font=ModernTheme.FONT).grid(row=1, column=1, padx=5, pady=5)
        
        def save_rule():
            category = category_var.get().strip()
            extensions = [ext.strip() for ext in extensions_var.get().split(",")]
            if category and extensions:
                self.organizer.add_rule(category, extensions)
                self._load_rules()
                dialog.destroy()
            else:
                messagebox.showerror("错误", "类别名称和扩展名不能为空")
                
        ttk.Button(dialog, 
                  text="保存",
                  style="Modern.TButton",
                  command=save_rule).grid(row=2, column=0, columnspan=2, pady=20)
        
        # 使对话框模态
        dialog.transient(self.window)
        dialog.grab_set()
        
    def _remove_rule(self):
        """删除选中的规则"""
        selected = self.rules_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要删除的规则")
            return
            
        category = self.rules_tree.item(selected[0])["values"][0]
        if messagebox.askyesno("确认", f"确定要删除 {category} 的规则吗？"):
            self.organizer.remove_rule(category)
            self._load_rules()
            
    def _edit_rule_dialog(self):
        """显示编辑规则对话框"""
        selected = self.rules_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要编辑的规则")
            return
            
        item = self.rules_tree.item(selected[0])
        category = item["values"][0]
        extensions = item["values"][1].split(", ")
        
        dialog = tk.Toplevel(self.window)
        dialog.title("编辑规则")
        dialog.geometry("400x200")
        dialog.configure(bg=ModernTheme.BACKGROUND)
        
        ttk.Label(dialog, 
                 text="类别名称：",
                 style="Modern.TLabel").grid(row=0, column=0, padx=5, pady=5)
        category_var = tk.StringVar(value=category)
        ttk.Entry(dialog, 
                 textvariable=category_var,
                 font=ModernTheme.FONT).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, 
                 text="文件扩展名：\n(用逗号分隔)",
                 style="Modern.TLabel").grid(row=1, column=0, padx=5, pady=5)
        extensions_var = tk.StringVar(value=",".join(extensions))
        ttk.Entry(dialog, 
                 textvariable=extensions_var,
                 font=ModernTheme.FONT).grid(row=1, column=1, padx=5, pady=5)
        
        def save_changes():
            new_category = category_var.get().strip()
            new_extensions = [ext.strip() for ext in extensions_var.get().split(",")]
            if new_category and new_extensions:
                if new_category != category:
                    self.organizer.remove_rule(category)
                self.organizer.add_rule(new_category, new_extensions)
                self._load_rules()
                dialog.destroy()
            else:
                messagebox.showerror("错误", "类别名称和扩展名不能为空")
                
        ttk.Button(dialog, 
                  text="保存",
                  style="Modern.TButton",
                  command=save_changes).grid(row=2, column=0, columnspan=2, pady=20)
        
        # 使对话框模态
        dialog.transient(self.window)
        dialog.grab_set()
        
    def _create_widgets(self):
        """创建GUI组件"""
        # 创建主框架
        main_frame = ttk.Frame(self.window, padding="20", style="Modern.TFrame")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.grid_columnconfigure(1, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, 
                              text="智能文件整理工具", 
                              style="Title.TLabel")
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 选择目录部分
        dir_frame = ttk.Frame(main_frame)
        dir_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        dir_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(dir_frame, 
                 text="选择要整理的目录：", 
                 style="Modern.TLabel").grid(row=0, column=0, sticky=tk.W)
        
        self.directory_var = tk.StringVar()
        directory_entry = ttk.Entry(dir_frame, 
                                  textvariable=self.directory_var, 
                                  font=ModernTheme.FONT,
                                  width=50)
        directory_entry.grid(row=0, column=1, padx=10, sticky=(tk.W, tk.E))
        
        browse_btn = ttk.Button(dir_frame, 
                              text="浏览", 
                              style="Modern.TButton",
                              command=self._browse_directory)
        browse_btn.grid(row=0, column=2)
        
        # 规则管理部分
        rules_label = ttk.Label(main_frame, 
                              text="文件分类规则", 
                              style="Title.TLabel")
        rules_label.grid(row=2, column=0, sticky=tk.W, pady=(0, 10))
        
        # 搜索框
        search_frame = ttk.Frame(main_frame)
        search_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(search_frame, 
                 text="搜索规则：", 
                 style="Modern.TLabel").grid(row=0, column=0, sticky=tk.W)
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self._filter_rules)
        search_entry = ttk.Entry(search_frame, 
                               textvariable=self.search_var,
                               font=ModernTheme.FONT)
        search_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # 规则列表
        rules_frame = ttk.Frame(main_frame)
        rules_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        rules_frame.grid_columnconfigure(0, weight=1)
        rules_frame.grid_rowconfigure(0, weight=1)
        
        self.rules_tree = ttk.Treeview(rules_frame, 
                                     columns=("类别", "扩展名"),
                                     show="headings",
                                     style="Modern.Treeview")
        self.rules_tree.heading("类别", text="类别")
        self.rules_tree.heading("扩展名", text="扩展名")
        self.rules_tree.column("类别", width=200)
        self.rules_tree.column("扩展名", width=400)
        self.rules_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 滚动条
        scrollbar = ttk.Scrollbar(rules_frame, 
                                orient=tk.VERTICAL, 
                                command=self.rules_tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.rules_tree.configure(yscrollcommand=scrollbar.set)
        
        # 规则操作按钮
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=5, column=0, columnspan=3, pady=20)
        
        ttk.Button(btn_frame, 
                  text="添加规则 (Ctrl+N)", 
                  style="Modern.TButton",
                  command=self._add_rule_dialog).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, 
                  text="删除规则 (Ctrl+D)", 
                  style="Modern.TButton",
                  command=self._remove_rule).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, 
                  text="编辑规则 (Ctrl+E)", 
                  style="Modern.TButton",
                  command=self._edit_rule_dialog).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, 
                  text="导入规则", 
                  style="Modern.TButton",
                  command=self._import_rules).grid(row=0, column=3, padx=5)
        ttk.Button(btn_frame, 
                  text="导出规则", 
                  style="Modern.TButton",
                  command=self._export_rules).grid(row=0, column=4, padx=5)
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, 
                                          variable=self.progress_var,
                                          maximum=100)
        self.progress_bar.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 操作按钮
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=7, column=0, columnspan=3, pady=(0, 10))
        
        ttk.Button(action_frame, 
                  text="预览整理结果", 
                  style="Modern.TButton",
                  command=self._preview_organization).grid(row=0, column=0, padx=5)
        ttk.Button(action_frame, 
                  text="开始整理", 
                  style="Modern.TButton",
                  command=self._start_organize).grid(row=0, column=1, padx=5)
        ttk.Button(action_frame, 
                  text="撤销上次操作 (Ctrl+Z)", 
                  style="Modern.TButton",
                  command=self._undo_last_operation).grid(row=0, column=2, padx=5)
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_label = ttk.Label(main_frame, 
                               textvariable=self.status_var,
                               style="Modern.TLabel")
        status_label.grid(row=8, column=0, columnspan=3, sticky=tk.W)
        
        # 配置主窗口的网格权重
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        
    def _filter_rules(self, *args):
        """根据搜索条件过滤规则列表"""
        search_text = self.search_var.get().lower()
        self.rules_tree.delete(*self.rules_tree.get_children())
        
        for category, extensions in self.organizer.rules.items():
            if (search_text in category.lower() or 
                search_text in ", ".join(extensions).lower()):
                self.rules_tree.insert("", tk.END, values=(category, ", ".join(extensions)))
                
    def _import_rules(self):
        """导入规则"""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    rules = json.load(f)
                self.organizer.rules = rules
                self._load_rules()
                messagebox.showinfo("成功", "规则导入成功！")
            except Exception as e:
                messagebox.showerror("错误", f"导入规则失败：{str(e)}")
                
    def _export_rules(self):
        """导出规则"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.organizer.rules, f, ensure_ascii=False, indent=4)
                messagebox.showinfo("成功", "规则导出成功！")
            except Exception as e:
                messagebox.showerror("错误", f"导出规则失败：{str(e)}")
                
    def _preview_organization(self):
        """预览文件整理结果"""
        directory = self.directory_var.get()
        if not directory:
            messagebox.showwarning("警告", "请先选择要整理的目录")
            return
            
        try:
            preview = self.organizer.preview_organization(directory)
            preview_window = tk.Toplevel(self.window)
            preview_window.title("整理预览")
            preview_window.geometry("600x400")
            preview_window.configure(bg=ModernTheme.BACKGROUND)
            
            text_widget = tk.Text(preview_window, 
                                font=ModernTheme.FONT,
                                wrap=tk.WORD,
                                bg=ModernTheme.BACKGROUND,
                                fg="black")
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            text_widget.tag_configure("bold", font=(ModernTheme.FONT[0], ModernTheme.FONT[1], "bold"))
            
            for category, files in preview.items():
                text_widget.insert(tk.END, f"\n{category}:\n", "bold")
                for file in files:
                    text_widget.insert(tk.END, f"  - {file}\n")
                    
            text_widget.configure(state="disabled")
            
            # 使预览窗口模态
            preview_window.transient(self.window)
            preview_window.grab_set()
            
        except Exception as e:
            messagebox.showerror("错误", f"预览失败：{str(e)}")
            
    def _undo_last_operation(self):
        """撤销上次操作"""
        if not self.undo_stack:
            messagebox.showinfo("提示", "没有可撤销的操作")
            return
            
        try:
            operation = self.undo_stack.pop()
            self.organizer.undo_operation(operation)
            messagebox.showinfo("成功", "已撤销上次操作")
        except Exception as e:
            messagebox.showerror("错误", f"撤销失败：{str(e)}")
            
    def _update_progress(self, current: int, total: int):
        """更新进度条"""
        progress = (current / total) * 100
        self.progress_var.set(progress)
        self.window.update()
        
    def _start_organize(self):
        """开始整理文件"""
        if self.is_organizing:
            messagebox.showwarning("警告", "文件整理正在进行中")
            return
            
        directory = self.directory_var.get()
        if not directory:
            messagebox.showwarning("警告", "请先选择要整理的目录")
            return
            
        def organize_thread():
            try:
                self.is_organizing = True
                self.status_var.set("正在整理文件...")
                
                stats = self.organizer.organize_directory(
                    directory, 
                    progress_callback=self._update_progress
                )
                
                result_message = (
                    f"整理完成！\n"
                    f"总文件数：{stats['总文件数']}\n"
                    f"已整理：{stats['已整理']}\n"
                    f"跳过：{stats['跳过']}\n"
                    f"错误：{stats['错误']}"
                )
                
                messagebox.showinfo("完成", result_message)
                self.status_var.set("就绪")
                self.progress_var.set(0)
                
            except Exception as e:
                messagebox.showerror("错误", f"整理文件时出错：{str(e)}")
                self.status_var.set("出错")
            finally:
                self.is_organizing = False
                
        threading.Thread(target=organize_thread, daemon=True).start()
        
    def run(self):
        """运行GUI程序"""
        self.window.mainloop()

if __name__ == "__main__":
    app = FileOrganizerGUI()
    app.run() 