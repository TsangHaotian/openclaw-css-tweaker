import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
import re
import os
import webbrowser


class RoundedButton(tk.Canvas):
    """圆角按钮组件"""
    def __init__(self, parent, text, command=None, bg="#e94560", fg="white",
                 font=("Microsoft YaHei UI", 10, "bold"), width=100, height=36,
                 corner_radius=8, hover_bg=None, **kwargs):
        super().__init__(parent, width=width, height=height,
                        highlightthickness=0, bg=parent.cget('bg'), **kwargs)

        self.command = command
        self.bg = bg
        self.fg = fg
        self.font = font
        self.corner_radius = corner_radius
        self.hover_bg = hover_bg or self._lighten_color(bg)
        self.text = text
        self.width = width
        self.height = height
        self.is_hovered = False

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)

        self._draw_button()

    def _lighten_color(self, color):
        """使颜色变亮"""
        if color.startswith('#'):
            r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
            r = min(255, r + 30)
            g = min(255, g + 30)
            b = min(255, b + 30)
            return f'#{r:02x}{g:02x}{b:02x}'
        return color

    def _draw_button(self):
        """绘制圆角按钮"""
        self.delete("all")

        color = self.hover_bg if self.is_hovered else self.bg
        r = self.corner_radius
        w = self.width
        h = self.height

        # 绘制圆角矩形
        points = [
            r, 0, w - r, 0, w, 0,
            w, r, w, h - r, w, h,
            w - r, h, r, h, 0, h,
            0, h - r, 0, r, 0, 0
        ]
        self.create_polygon(points, fill=color, smooth=True, tags="button")

        # 绘制文字
        self.create_text(w // 2, h // 2, text=self.text, fill=self.fg,
                        font=self.font, tags="text")

    def _on_enter(self, event):
        self.is_hovered = True
        self._draw_button()
        self.config(cursor="hand2")

    def _on_leave(self, event):
        self.is_hovered = False
        self._draw_button()

    def _on_click(self, event):
        if self.command:
            self.command()


class OpenClawCSSTweaker:
    """OpenClaw CSS 美化工具 - 傻瓜式界面编辑器"""

    # 完整的可修改元素配置（根据官方教程）
    ELEMENTS = {
        "🎨 背景图片": {
            "selector": ".shell",
            "property": "background-image",
            "type": "image",
            "description": "全局背景图片",
        },
        "🎨 顶部导航栏": {
            "selector": ".topbar",
            "property": "background",
            "type": "color",
            "description": "顶部导航栏背景颜色",
            "default": "rgba(255, 192, 203, 0.5)"
        },
        "🎨 侧边栏": {
            "selector": ".nav",
            "property": "background",
            "type": "color",
            "important": True,
            "description": "左侧导航栏背景颜色",
            "default": "rgba(255, 192, 203, 0.5)"
        },
        "💬 AI回复气泡": {
            "selector": ".chat-bubble.has-copy",
            "property": "background",
            "type": "color",
            "description": "AI回复气泡背景色",
            "default": "rgba(0, 120, 255, 0.3)"
        },
        "📋 复制按钮(悬停)": {
            "selector": ".chat-bubble:hover .chat-copy-btn",
            "property": "background",
            "type": "color",
            "description": "气泡内复制按钮悬停颜色",
            "default": "rgba(238, 5, 5, 0.3)"
        },
        "💬 AI气泡(悬停)": {
            "selector": ".chat-bubble:hover",
            "property": "background",
            "type": "color",
            "description": "AI气泡悬停背景色",
            "default": "rgba(238, 5, 5, 0.3)"
        },
        "📁 文件操作框": {
            "selector": ".chat-bubble",
            "property": "background",
            "type": "color",
            "description": "文件操作回复框背景色",
            "default": "rgba(94, 5, 238, 0.3)"
        },
        "📝 工具卡片": {
            "selector": ".chat-tool-card",
            "property": "background",
            "type": "color",
            "description": "文件操作卡片内部背景色",
            "default": "rgba(5, 238, 44, 0.3)"
        },
        "📝 工具卡片(悬停)": {
            "selector": ".chat-tool-card:hover",
            "property": "background",
            "type": "color",
            "description": "工具卡片悬停背景色",
            "default": "rgba(234, 238, 5, 0.3)"
        },
        "👤 用户气泡": {
            "selector": ".chat-group.user .chat-bubble",
            "property": "background",
            "type": "color",
            "description": "用户发送气泡背景色",
            "default": "rgba(5, 238, 36, 0.3)"
        },
        "👤 用户气泡(悬停)": {
            "selector": ".chat-group.user .chat-bubble:hover",
            "property": "background",
            "type": "color",
            "description": "用户气泡悬停背景色",
            "default": "rgba(94, 5, 238, 0.3)"
        },
        "🎯 全局卡片颜色": {
            "selector": ":root",
            "property": "--card",
            "type": "css-var",
            "description": "全局卡片颜色变量(影响多个区域)",
            "default": "rgba(5, 238, 55, 0.3)"
        },
        "⌨️ 输入区域背景": {
            "selector": ".chat-compose",
            "property": "background",
            "type": "color",
            "important": True,
            "description": "底部输入区域背景",
            "default": "transparent"
        },
        "⌨️ 输入框": {
            "selector": ".chat-compose .chat-compose__field textarea",
            "property": "background",
            "type": "color",
            "important": True,
            "description": "输入框本身背景色",
            "default": "rgba(216, 9, 44, 0.3)"
        },
        "🔘 操作按钮": {
            "selector": ".chat-compose .chat-compose__actions .btn",
            "property": "background",
            "type": "color",
            "description": "新会话、发送按钮颜色",
            "default": "rgba(236, 233, 6, 0.3)"
        },
        "🖼️ 用户头像": {
            "selector": ".chat-avatar.user",
            "property": "background-image",
            "type": "image",
            "description": "用户头像图片",
        },
        "🖼️ AI头像": {
            "selector": ".chat-avatar.assistant",
            "property": "background-image",
            "type": "image",
            "description": "AI助手头像图片",
        }
    }

    # 预设颜色
    PRESET_COLORS = [
        ("粉色", "#FFC0CB"),
        ("蓝色", "#0078FF"),
        ("红色", "#EE0505"),
        ("绿色", "#05EE24"),
        ("紫色", "#5E05EE"),
        ("黄色", "#ECE906"),
        ("深红", "#D8092C"),
        ("橙色", "#FF8C00"),
        ("青色", "#00CED1"),
        ("白色", "#FFFFFF"),
    ]

    def __init__(self, root):
        self.root = root
        self.root.title("OpenClaw CSS 美化工具 v2.1")
        self.root.geometry("1100x750")
        self.root.minsize(900, 600)

        # 主题配色
        self.colors = {
            "bg_dark": "#1a1a2e",
            "bg_medium": "#16213e",
            "bg_light": "#0f3460",
            "bg_card": "#1e3a5f",
            "accent": "#e94560",
            "accent_hover": "#ff6b6b",
            "success": "#2ecc71",
            "success_hover": "#58d68d",
            "info": "#3498db",
            "text": "#eaeaea",
            "text_dim": "#a0a0a0",
            "border": "#2a4a6a"
        }

        self.current_file = None
        self.css_content = ""
        self.original_css = ""
        self.element_values = {}
        self.current_element = None
        self.current_hex = "#444444"
        self.opacity = 30

        self.setup_ui()

    def setup_ui(self):
        """构建主界面"""
        self.root.configure(bg=self.colors["bg_dark"])

        # 顶部标题栏
        self.create_header()

        # 主内容区
        main_frame = tk.Frame(self.root, bg=self.colors["bg_dark"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # 左侧：元素列表
        self.create_element_panel(main_frame)

        # 右侧：编辑区
        self.create_edit_panel(main_frame)

        # 底部状态栏
        self.create_status_bar()

    def create_header(self):
        """创建顶部标题栏"""
        header = tk.Frame(self.root, bg=self.colors["bg_medium"], height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        # 左侧标题
        title_frame = tk.Frame(header, bg=self.colors["bg_medium"])
        title_frame.pack(side=tk.LEFT, padx=20, pady=10)

        tk.Label(
            title_frame,
            text="🎨 OpenClaw CSS 美化工具",
            bg=self.colors["bg_medium"],
            fg=self.colors["text"],
            font=("Microsoft YaHei UI", 18, "bold")
        ).pack(side=tk.LEFT)

        tk.Label(
            title_frame,
            text="  v2.1",
            bg=self.colors["bg_medium"],
            fg=self.colors["accent"],
            font=("Microsoft YaHei UI", 12)
        ).pack(side=tk.LEFT, pady=(8, 0))

        # 右侧操作按钮
        btn_frame = tk.Frame(header, bg=self.colors["bg_medium"])
        btn_frame.pack(side=tk.RIGHT, padx=20, pady=15)

        # 导入按钮
        self.import_btn = RoundedButton(
            btn_frame, text="📁 导入CSS", command=self.import_css,
            bg=self.colors["bg_light"], fg=self.colors["text"],
            font=("Microsoft YaHei UI", 10, "bold"), width=95, height=34
        )
        self.import_btn.pack(side=tk.LEFT, padx=4)

        # 重置按钮
        self.reset_btn = RoundedButton(
            btn_frame, text="🔄 重置", command=self.reset_css,
            bg=self.colors["bg_card"], fg=self.colors["text"],
            font=("Microsoft YaHei UI", 10, "bold"), width=85, height=34
        )
        self.reset_btn.pack(side=tk.LEFT, padx=4)

        # 保存按钮
        self.save_btn = RoundedButton(
            btn_frame, text="💾 保存CSS", command=self.save_css,
            bg=self.colors["accent"], fg="white",
            font=("Microsoft YaHei UI", 10, "bold"), width=95, height=34
        )
        self.save_btn.pack(side=tk.LEFT, padx=4)

        # 关于按钮
        self.about_btn = RoundedButton(
            btn_frame, text="ℹ️ 关于", command=self.show_about,
            bg=self.colors["info"], fg="white",
            font=("Microsoft YaHei UI", 10, "bold"), width=75, height=34
        )
        self.about_btn.pack(side=tk.LEFT, padx=4)

    def show_about(self):
        """显示关于对话框"""
        about_window = tk.Toplevel(self.root)
        about_window.title("关于")
        about_window.geometry("420x380")
        about_window.resizable(False, False)
        about_window.configure(bg=self.colors["bg_medium"])

        # 居中显示
        about_window.transient(self.root)
        about_window.grab_set()

        # 图标和标题
        tk.Label(
            about_window,
            text="🎨 OpenClaw CSS 美化工具",
            bg=self.colors["bg_medium"],
            fg=self.colors["text"],
            font=("Microsoft YaHei UI", 16, "bold")
        ).pack(pady=(25, 5))

        tk.Label(
            about_window,
            text="版本 2.1",
            bg=self.colors["bg_medium"],
            fg=self.colors["accent"],
            font=("Microsoft YaHei UI", 11)
        ).pack(pady=(0, 15))

        # 分隔线
        tk.Frame(about_window, bg=self.colors["border"], height=1).pack(fill=tk.X, padx=30, pady=10)

        # 作者信息
        tk.Label(
            about_window,
            text="👨‍💻 作者",
            bg=self.colors["bg_medium"],
            fg=self.colors["text"],
            font=("Microsoft YaHei UI", 12, "bold")
        ).pack(pady=(10, 3))

        tk.Label(
            about_window,
            text="TsangHaotian",
            bg=self.colors["bg_medium"],
            fg=self.colors["text_dim"],
            font=("Microsoft YaHei UI", 11)
        ).pack()

        # 项目介绍
        tk.Label(
            about_window,
            text="📖 项目介绍",
            bg=self.colors["bg_medium"],
            fg=self.colors["text"],
            font=("Microsoft YaHei UI", 12, "bold")
        ).pack(pady=(15, 3))

        desc_text = "一个简单易用的 OpenClaw 界面美化工具\n无需了解CSS语法，图形化界面一键修改配色"
        tk.Label(
            about_window,
            text=desc_text,
            bg=self.colors["bg_medium"],
            fg=self.colors["text_dim"],
            font=("Microsoft YaHei UI", 10),
            justify=tk.CENTER
        ).pack()

        # GitHub 链接
        tk.Label(
            about_window,
            text="🔗 开源地址",
            bg=self.colors["bg_medium"],
            fg=self.colors["text"],
            font=("Microsoft YaHei UI", 12, "bold")
        ).pack(pady=(15, 3))

        def open_github():
            webbrowser.open("https://github.com/TsangHaotian/openclaw-css-tweaker")

        link_btn = RoundedButton(
            about_window,
            text="📦 GitHub: TsangHaotian/openclaw-css-tweaker",
            command=open_github,
            bg=self.colors["accent"],
            fg="white",
            font=("Microsoft YaHei UI", 9, "bold"),
            width=320, height=32, corner_radius=6
        )
        link_btn.pack(pady=10)

        # 关闭按钮
        close_btn = RoundedButton(
            about_window,
            text="关闭",
            command=about_window.destroy,
            bg=self.colors["bg_light"],
            fg=self.colors["text"],
            font=("Microsoft YaHei UI", 10),
            width=80, height=30, corner_radius=6
        )
        close_btn.pack(pady=15)

    def create_element_panel(self, parent):
        """创建左侧元素选择面板"""
        left_frame = tk.Frame(parent, bg=self.colors["bg_medium"], width=300)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_frame.pack_propagate(False)

        # 面板标题
        title_bar = tk.Frame(left_frame, bg=self.colors["bg_medium"])
        title_bar.pack(fill=tk.X, pady=(15, 10), padx=15)

        tk.Label(
            title_bar,
            text="📋 选择修改项目",
            bg=self.colors["bg_medium"],
            fg=self.colors["text"],
            font=("Microsoft YaHei UI", 13, "bold")
        ).pack(side=tk.LEFT)

        # 分类标签
        categories = {
            "全局样式": ["🎨 背景图片", "🎨 顶部导航栏", "🎨 侧边栏", "🎯 全局卡片颜色"],
            "AI回复区域": ["💬 AI回复气泡", "📋 复制按钮(悬停)", "💬 AI气泡(悬停)", "📁 文件操作框", "📝 工具卡片", "📝 工具卡片(悬停)"],
            "用户区域": ["👤 用户气泡", "👤 用户气泡(悬停)", "🖼️ 用户头像", "🖼️ AI头像"],
            "输入区域": ["⌨️ 输入区域背景", "⌨️ 输入框", "🔘 操作按钮"]
        }

        # 滚动区域
        canvas = tk.Canvas(left_frame, bg=self.colors["bg_medium"], highlightthickness=0)
        scrollbar = tk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg=self.colors["bg_medium"])

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=280)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # 鼠标滚轮绑定
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # 创建分类和按钮
        self.element_buttons = {}
        for category, elements in categories.items():
            # 分类标题
            cat_frame = tk.Frame(self.scrollable_frame, bg=self.colors["bg_medium"])
            cat_frame.pack(fill=tk.X, pady=(10, 5), padx=10)

            tk.Label(
                cat_frame,
                text=f"━━ {category} ━━",
                bg=self.colors["bg_medium"],
                fg=self.colors["accent"],
                font=("Microsoft YaHei UI", 10, "bold")
            ).pack(anchor=tk.W)

            # 元素按钮
            for element_name in elements:
                self.create_element_button(self.scrollable_frame, element_name)

    def create_element_button(self, parent, element_name):
        """创建单个元素选择按钮 - 圆润风格"""
        config = self.ELEMENTS[element_name]
        is_image = config["type"] == "image"

        btn_container = tk.Frame(parent, bg=self.colors["bg_medium"])
        btn_container.pack(fill=tk.X, pady=2, padx=10)

        # 使用Canvas绘制圆角背景
        btn_canvas = tk.Canvas(
            btn_container,
            width=255,
            height=36,
            highlightthickness=0,
            bg=self.colors["bg_medium"]
        )
        btn_canvas.pack()

        # 绘制圆角矩形背景
        def draw_rounded_rect(hover=False):
            btn_canvas.delete("all")
            color = self.colors["bg_card"] if not hover else self.colors["bg_light"]
            r = 8
            w, h = 255, 36
            points = [
                r, 0, w - r, 0, w, 0,
                w, r, w, h - r, w, h,
                w - r, h, r, h, 0, h,
                0, h - r, 0, r, 0, 0
            ]
            btn_canvas.create_polygon(points, fill=color, smooth=True)
            btn_canvas.create_text(15, h // 2, text=element_name, fill=self.colors["text"],
                                  font=("Microsoft YaHei UI", 10), anchor=tk.W)

            # 颜色预览标记
            if not is_image:
                current_color = self.element_values.get(element_name, "#444444")
                # 验证颜色格式，确保是有效的tkinter颜色
                valid_color = "#444444"
                if current_color.startswith("#") and len(current_color) >= 7:
                    valid_color = current_color[:7]
                elif current_color.startswith("rgba"):
                    rgba_match = re.search(r'rgba?\((\d+),\s*(\d+),\s*(\d+)', current_color)
                    if rgba_match:
                        r_val, g, b = rgba_match.groups()
                        valid_color = f"#{int(r_val):02x}{int(g):02x}{int(b):02x}"
                elif current_color.startswith("rgb"):
                    rgb_match = re.search(r'rgb\((\d+),\s*(\d+),\s*(\d+)', current_color)
                    if rgb_match:
                        r_val, g, b = rgb_match.groups()
                        valid_color = f"#{int(r_val):02x}{int(g):02x}{int(b):02x}"
                # 忽略var()、transparent等无效颜色
                btn_canvas.create_text(w - 15, h // 2, text="●", fill=valid_color,
                                      font=("Microsoft YaHei UI", 14), anchor=tk.E)

        draw_rounded_rect()

        def on_enter(e):
            draw_rounded_rect(hover=True)
            btn_canvas.config(cursor="hand2")

        def on_leave(e):
            draw_rounded_rect(hover=False)

        def on_click(e):
            self.select_element(element_name)

        btn_canvas.bind("<Enter>", on_enter)
        btn_canvas.bind("<Leave>", on_leave)
        btn_canvas.bind("<Button-1>", on_click)

        self.element_buttons[element_name] = btn_canvas
        self.element_values[element_name] = config.get("default", "")

    def create_edit_panel(self, parent):
        """创建右侧编辑面板"""
        right_frame = tk.Frame(parent, bg=self.colors["bg_medium"])
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 当前编辑标题
        self.edit_title = tk.Label(
            right_frame,
            text="👆 请选择左侧项目进行编辑",
            bg=self.colors["bg_medium"],
            fg=self.colors["text"],
            font=("Microsoft YaHei UI", 14, "bold")
        )
        self.edit_title.pack(pady=(20, 5), padx=20, anchor=tk.W)

        # 描述
        self.edit_desc = tk.Label(
            right_frame,
            text="导入CSS文件后，点击左侧项目即可修改",
            bg=self.colors["bg_medium"],
            fg=self.colors["text_dim"],
            font=("Microsoft YaHei UI", 10)
        )
        self.edit_desc.pack(padx=20, anchor=tk.W)

        # 编辑区域容器
        edit_container = tk.Frame(right_frame, bg=self.colors["bg_light"])
        edit_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        # 颜色编辑区
        self.color_frame = tk.Frame(edit_container, bg=self.colors["bg_light"])

        # 当前颜色显示
        color_row = tk.Frame(self.color_frame, bg=self.colors["bg_light"])
        color_row.pack(fill=tk.X, pady=20, padx=25)

        tk.Label(
            color_row,
            text="当前颜色:",
            bg=self.colors["bg_light"],
            fg=self.colors["text"],
            font=("Microsoft YaHei UI", 11)
        ).pack(side=tk.LEFT)

        self.color_preview = tk.Label(
            color_row,
            text="       ",
            bg="#444444",
            relief=tk.FLAT,
            borderwidth=0
        )
        self.color_preview.pack(side=tk.LEFT, padx=15)

        self.color_value_label = tk.Label(
            color_row,
            text="#444444",
            bg=self.colors["bg_light"],
            fg=self.colors["text_dim"],
            font=("Consolas", 11)
        )
        self.color_value_label.pack(side=tk.LEFT)

        # rgba 显示
        self.rgba_label = tk.Label(
            color_row,
            text="",
            bg=self.colors["bg_light"],
            fg=self.colors["accent"],
            font=("Consolas", 10)
        )
        self.rgba_label.pack(side=tk.LEFT, padx=15)

        # 透明度滑块
        opacity_row = tk.Frame(self.color_frame, bg=self.colors["bg_light"])
        opacity_row.pack(fill=tk.X, pady=15, padx=25)

        tk.Label(
            opacity_row,
            text="透明度:",
            bg=self.colors["bg_light"],
            fg=self.colors["text"],
            font=("Microsoft YaHei UI", 11)
        ).pack(side=tk.LEFT)

        self.opacity_var = tk.IntVar(value=30)
        self.opacity_slider = tk.Scale(
            opacity_row,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.opacity_var,
            bg=self.colors["bg_light"],
            fg=self.colors["text"],
            highlightthickness=0,
            troughcolor=self.colors["bg_dark"],
            length=250,
            command=self.on_opacity_change
        )
        self.opacity_slider.pack(side=tk.LEFT, padx=15)

        self.opacity_label = tk.Label(
            opacity_row,
            text="30%",
            bg=self.colors["bg_light"],
            fg=self.colors["accent"],
            font=("Microsoft YaHei UI", 11, "bold"),
            width=5
        )
        self.opacity_label.pack(side=tk.LEFT)

        # 预设颜色区
        preset_frame = tk.Frame(self.color_frame, bg=self.colors["bg_light"])
        preset_frame.pack(fill=tk.X, pady=15, padx=25)

        tk.Label(
            preset_frame,
            text="快速选色:",
            bg=self.colors["bg_light"],
            fg=self.colors["text"],
            font=("Microsoft YaHei UI", 11)
        ).pack(anchor=tk.W, pady=(0, 8))

        preset_grid = tk.Frame(preset_frame, bg=self.colors["bg_light"])
        preset_grid.pack(fill=tk.X)

        for i, (name, color) in enumerate(self.PRESET_COLORS):
            btn = tk.Button(
                preset_grid,
                text=name,
                bg=color,
                fg="white" if color in ["#000000", "#5E05EE", "#EE0505", "#0078FF", "#D8092C"] else "black",
                font=("Microsoft YaHei UI", 9),
                relief=tk.FLAT,
                width=7,
                cursor="hand2",
                command=lambda c=color: self.set_preset_color(c)
            )
            btn.grid(row=i // 5, column=i % 5, padx=3, pady=3)

        # 操作按钮 - 使用圆角按钮
        btn_row = tk.Frame(self.color_frame, bg=self.colors["bg_light"])
        btn_row.pack(fill=tk.X, pady=20, padx=25)

        self.pick_color_btn = RoundedButton(
            btn_row,
            text="🎨 拾色器",
            command=self.pick_color,
            bg=self.colors["accent"],
            fg="white",
            font=("Microsoft YaHei UI", 10, "bold"),
            width=95, height=38, corner_radius=10
        )
        self.pick_color_btn.pack(side=tk.LEFT, padx=5)

        self.apply_btn = RoundedButton(
            btn_row,
            text="✅ 应用修改",
            command=self.apply_change,
            bg=self.colors["success"],
            fg="white",
            font=("Microsoft YaHei UI", 10, "bold"),
            width=105, height=38, corner_radius=10
        )
        self.apply_btn.pack(side=tk.LEFT, padx=5)

        # 图片选择区（初始隐藏）
        self.image_frame = tk.Frame(edit_container, bg=self.colors["bg_light"])

        img_row = tk.Frame(self.image_frame, bg=self.colors["bg_light"])
        img_row.pack(fill=tk.X, pady=30, padx=25)

        tk.Label(
            img_row,
            text="图片文件:",
            bg=self.colors["bg_light"],
            fg=self.colors["text"],
            font=("Microsoft YaHei UI", 11)
        ).pack(side=tk.LEFT)

        self.image_path_var = tk.StringVar(value="未选择")
        self.image_path_entry = tk.Entry(
            img_row,
            textvariable=self.image_path_var,
            bg=self.colors["bg_dark"],
            fg=self.colors["text"],
            font=("Consolas", 10),
            width=30,
            relief=tk.FLAT
        )
        self.image_path_entry.pack(side=tk.LEFT, padx=15)

        self.pick_image_btn = RoundedButton(
            img_row,
            text="📁 选择图片",
            command=self.pick_image,
            bg=self.colors["accent"],
            fg="white",
            font=("Microsoft YaHei UI", 10, "bold"),
            width=95, height=34, corner_radius=8
        )
        self.pick_image_btn.pack(side=tk.LEFT, padx=5)

        # 图片应用按钮
        img_btn_row = tk.Frame(self.image_frame, bg=self.colors["bg_light"])
        img_btn_row.pack(fill=tk.X, pady=20, padx=25)

        self.apply_image_btn = RoundedButton(
            img_btn_row,
            text="✅ 应用图片",
            command=self.apply_image,
            bg=self.colors["success"],
            fg="white",
            font=("Microsoft YaHei UI", 10, "bold"),
            width=105, height=38, corner_radius=10
        )
        self.apply_image_btn.pack(side=tk.LEFT)

        # CSS代码预览
        preview_frame = tk.Frame(edit_container, bg=self.colors["bg_light"])
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=15, padx=25)

        tk.Label(
            preview_frame,
            text="📝 CSS 代码预览:",
            bg=self.colors["bg_light"],
            fg=self.colors["text"],
            font=("Microsoft YaHei UI", 11)
        ).pack(anchor=tk.W, pady=(0, 8))

        self.code_preview = tk.Text(
            preview_frame,
            bg=self.colors["bg_dark"],
            fg="#7ee787",
            font=("Consolas", 10),
            height=8,
            relief=tk.FLAT,
            padx=15,
            pady=10,
            wrap=tk.WORD
        )
        self.code_preview.pack(fill=tk.BOTH, expand=True)

    def create_status_bar(self):
        """创建底部状态栏"""
        status_bar = tk.Frame(self.root, bg=self.colors["bg_dark"], height=30)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        status_bar.pack_propagate(False)

        self.status_var = tk.StringVar(value="💡 提示: 请先导入CSS文件开始编辑")
        tk.Label(
            status_bar,
            textvariable=self.status_var,
            bg=self.colors["bg_dark"],
            fg=self.colors["text_dim"],
            font=("Microsoft YaHei UI", 9),
            anchor=tk.W
        ).pack(side=tk.LEFT, padx=15, pady=5)

        # 文件名显示
        self.file_label = tk.Label(
            status_bar,
            text="",
            bg=self.colors["bg_dark"],
            fg=self.colors["accent"],
            font=("Microsoft YaHei UI", 9),
            anchor=tk.E
        )
        self.file_label.pack(side=tk.RIGHT, padx=15, pady=5)

    def import_css(self):
        """导入CSS文件"""
        file_path = filedialog.askopenfilename(
            title="选择OpenClaw的CSS文件",
            filetypes=[("CSS文件", "*.css"), ("所有文件", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.css_content = f.read()
                self.original_css = self.css_content
                self.current_file = file_path

                filename = os.path.basename(file_path)
                self.status_var.set(f"✅ 已导入CSS文件")
                self.file_label.config(text=filename)
                self.edit_title.config(text="👆 请选择左侧项目进行编辑")
                self.edit_desc.config(text="点击左侧任意项目开始修改")

                # 解析现有颜色
                self.parse_existing_values()

                # 刷新左侧按钮显示
                self.refresh_element_buttons()

                messagebox.showinfo("成功", f"已成功导入:\n{filename}\n\n请点击左侧项目开始编辑！")

            except Exception as e:
                messagebox.showerror("错误", f"导入失败:\n{e}")

    def refresh_element_buttons(self):
        """刷新元素按钮显示"""
        for element_name, btn_canvas in self.element_buttons.items():
            config = self.ELEMENTS[element_name]
            is_image = config["type"] == "image"

            def redraw(canvas=btn_canvas, name=element_name, is_img=is_image):
                canvas.delete("all")
                color = self.colors["bg_card"]
                r = 8
                w, h = 255, 36
                points = [
                    r, 0, w - r, 0, w, 0,
                    w, r, w, h - r, w, h,
                    w - r, h, r, h, 0, h,
                    0, h - r, 0, r, 0, 0
                ]
                canvas.create_polygon(points, fill=color, smooth=True)
                canvas.create_text(15, h // 2, text=name, fill=self.colors["text"],
                                  font=("Microsoft YaHei UI", 10), anchor=tk.W)

                if not is_img:
                    current_color = self.element_values.get(name, "#444444")
                    # 验证颜色格式
                    valid_color = "#444444"
                    if current_color.startswith("#") and len(current_color) >= 7:
                        valid_color = current_color[:7]
                    elif current_color.startswith("rgba"):
                        rgba_match = re.search(r'rgba?\((\d+),\s*(\d+),\s*(\d+)', current_color)
                        if rgba_match:
                            r_val, g, b = rgba_match.groups()
                            valid_color = f"#{int(r_val):02x}{int(g):02x}{int(b):02x}"
                    elif current_color.startswith("rgb"):
                        rgb_match = re.search(r'rgb\((\d+),\s*(\d+),\s*(\d+)', current_color)
                        if rgb_match:
                            r_val, g, b = rgb_match.groups()
                            valid_color = f"#{int(r_val):02x}{int(g):02x}{int(b):02x}"
                    canvas.create_text(w - 15, h // 2, text="●", fill=valid_color,
                                      font=("Microsoft YaHei UI", 14), anchor=tk.E)

            redraw()

    def parse_existing_values(self):
        """解析CSS中已存在的值"""
        for element_name, config in self.ELEMENTS.items():
            selector = config["selector"]
            prop = config["property"]
            element_type = config["type"]

            if element_type == "css-var":
                pattern = rf'{prop}:\s*([^;]+);'
                match = re.search(pattern, self.css_content)
                if match:
                    self.element_values[element_name] = match.group(1).strip()
            else:
                block_start, block_end = self._find_css_block(selector)
                if block_start is not None and block_end is not None:
                    block = self.css_content[block_start:block_end]

                    if element_type == "image":
                        img_match = re.search(r'background-image:\s*url\([\'"]?([^\'"()]+)[\'"]?\)', block)
                        if img_match:
                            self.element_values[element_name] = img_match.group(1)
                    else:
                        bg_match = re.search(r'background:\s*([^;]+);', block)
                        if bg_match:
                            color_val = bg_match.group(1).strip()
                            color_val = color_val.replace('!important', '').strip()
                            self.element_values[element_name] = color_val

    def _find_css_block(self, selector):
        """查找CSS选择器块，严格匹配选择器名称"""
        escaped = selector.replace('.', r'\.')
        escaped = escaped.replace(' ', r'\s*')

        pattern1 = rf'(?:^|[\n\r])\s*{escaped}\s*\{{'
        match = re.search(pattern1, self.css_content, re.MULTILINE)
        if match:
            return self._extract_block(match)

        pattern2 = rf'(?:^|[\n\r])([^{{]*{escaped}[^{{]*\{{)'
        match = re.search(pattern2, self.css_content, re.MULTILINE)
        if match:
            return self._extract_block_from_merged(match)

        if selector.startswith('.'):
            alt_selector = selector[1:]
            alt_escaped = re.escape(alt_selector)

            pattern1 = rf'(?:^|[\n\r])\s*{alt_escaped}\s*\{{'
            match = re.search(pattern1, self.css_content, re.MULTILINE)
            if match:
                return self._extract_block(match)

            pattern2 = rf'(?:^|[\n\r])([^{{]*{alt_escaped}[^{{]*\{{)'
            match = re.search(pattern2, self.css_content, re.MULTILINE)
            if match:
                return self._extract_block_from_merged(match)

        return None, None

    def _extract_block_from_merged(self, match):
        """从合并选择器规则中提取CSS块"""
        selector_start = match.start(1)
        brace_pos = match.group(1).rfind('{')
        if brace_pos == -1:
            return None, None

        actual_start = selector_start + brace_pos + 1
        brace_count = 1
        i = actual_start

        while i < len(self.css_content):
            if self.css_content[i] == '{':
                brace_count += 1
            elif self.css_content[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    return actual_start, i
            i += 1

        return None, None

    def _extract_block(self, match):
        """从匹配位置提取CSS块"""
        start = match.end() - 1
        brace_count = 0
        i = start

        while i < len(self.css_content):
            if self.css_content[i] == '{':
                brace_count += 1
            elif self.css_content[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    block_start = match.end()
                    block_end = i
                    return block_start, block_end
            i += 1

        return None, None

    def select_element(self, element_name):
        """选择要编辑的元素"""
        if not self.css_content:
            messagebox.showwarning("提示", "请先导入CSS文件！")
            return

        self.current_element = element_name
        config = self.ELEMENTS[element_name]
        element_type = config["type"]

        self.edit_title.config(text=f"正在编辑: {element_name}")
        self.edit_desc.config(text=f"说明: {config['description']}")

        if element_type == "image":
            self.color_frame.pack_forget()
            self.image_frame.pack(fill=tk.X, pady=10)
            current = self.element_values.get(element_name, "未设置")
            self.image_path_var.set(current if current else "未设置")
        else:
            self.image_frame.pack_forget()
            self.color_frame.pack(fill=tk.X, pady=10)

            current = self.element_values.get(element_name, config.get("default", "#444444"))

            if current and current.startswith("rgba"):
                rgba_match = re.search(r'rgba?\((\d+),\s*(\d+),\s*(\d+),?\s*([\d.]+)?\)', current)
                if rgba_match:
                    r, g, b = rgba_match.group(1), rgba_match.group(2), rgba_match.group(3)
                    a = rgba_match.group(4) or "1"
                    hex_color = f"#{int(r):02x}{int(g):02x}{int(b):02x}"
                    opacity = int(float(a) * 100)
                    self.current_hex = hex_color
                    self.opacity = opacity
                    self.opacity_var.set(opacity)
                    self.update_color_display(hex_color)
            elif current and current.startswith("#"):
                self.current_hex = current
                self.update_color_display(current)

        self.update_code_preview()

    def update_color_display(self, hex_color):
        """更新颜色显示"""
        self.color_preview.config(bg=hex_color)
        self.color_value_label.config(text=hex_color)

        hex_val = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_val[i:i + 2], 16) for i in (0, 2, 4))
        opacity_val = self.opacity_var.get() / 100
        rgba_str = f"rgba({r}, {g}, {b}, {opacity_val:.1f})"
        self.rgba_label.config(text=rgba_str)

    def on_opacity_change(self, value):
        """透明度变化"""
        self.opacity_label.config(text=f"{int(float(value))}%")
        self.update_color_display(self.current_hex)

    def set_preset_color(self, hex_color):
        """设置预设颜色"""
        self.current_hex = hex_color
        self.update_color_display(hex_color)

    def pick_color(self):
        """打开颜色选择器"""
        color = colorchooser.askcolor(
            title="选择颜色",
            initialcolor=self.current_hex
        )
        if color[1]:
            self.current_hex = color[1]
            self.update_color_display(color[1])

    def pick_image(self):
        """选择图片文件"""
        file_path = filedialog.askopenfilename(
            title="选择图片",
            filetypes=[
                ("图片文件", "*.png *.jpg *.jpeg *.webp *.gif *.svg"),
                ("所有文件", "*.*")
            ]
        )
        if file_path:
            filename = os.path.basename(file_path)
            self.image_path_var.set(filename)
            self.status_var.set(f"已选择图片: {filename}")

    def apply_change(self):
        """应用颜色修改"""
        if not self.current_element or not self.css_content:
            return

        config = self.ELEMENTS[self.current_element]
        selector = config["selector"]
        prop = config["property"]
        element_type = config["type"]
        important = config.get("important", False)

        hex_val = self.current_hex.lstrip('#')
        r, g, b = tuple(int(hex_val[i:i + 2], 16) for i in (0, 2, 4))
        opacity_val = self.opacity_var.get() / 100
        new_value = f"rgba({r}, {g}, {b}, {opacity_val:.1f})"

        self._apply_css_change(selector, prop, new_value, important, element_type)

        self.element_values[self.current_element] = new_value
        self.refresh_element_buttons()
        self.update_code_preview()

        self.status_var.set(f"✅ 已修改: {self.current_element}")

    def apply_image(self):
        """应用图片修改"""
        if not self.current_element:
            return

        config = self.ELEMENTS[self.current_element]
        selector = config["selector"]
        image_path = self.image_path_var.get()

        if not image_path or image_path == "未设置":
            messagebox.showwarning("提示", "请先选择图片！")
            return

        self._apply_css_change(selector, "background-image", f"url('{image_path}')", False, "image")

        self.element_values[self.current_element] = image_path
        self.update_code_preview()

        self.status_var.set(f"✅ 已修改: {self.current_element}")

    def _apply_css_change(self, selector, prop, value, important, element_type):
        """修改CSS内容"""
        important_str = " !important" if important else ""

        if element_type == "css-var":
            pattern = rf'({prop}:\s*)[^;]+;'
            if re.search(pattern, self.css_content):
                self.css_content = re.sub(pattern, f'{prop}: {value};', self.css_content)
            else:
                root_match = re.search(r':root\s*\{', self.css_content)
                if root_match:
                    insert_pos = root_match.end()
                    self.css_content = (self.css_content[:insert_pos] +
                                        f"\n    {prop}: {value};" +
                                        self.css_content[insert_pos:])
        else:
            block_start, block_end = self._find_css_block(selector)

            if block_start is not None and block_end is not None:
                block = self.css_content[block_start:block_end]

                bg_pattern = r'background:\s*[^;]+;?'

                if prop == "background-image":
                    bg_pattern = r'background-image:\s*[^;]+;?'

                if re.search(bg_pattern, block):
                    new_block = re.sub(bg_pattern, f'{prop}: {value}{important_str};\n    ', block)
                else:
                    new_block = block.rstrip() + f"\n    {prop}: {value}{important_str};\n    "

                self.css_content = (self.css_content[:block_start] +
                                    new_block +
                                    self.css_content[block_end:])
            else:
                new_rule = f"\n\n{selector} {{\n    {prop}: {value}{important_str};\n}}\n"
                self.css_content += new_rule

    def update_code_preview(self):
        """更新CSS代码预览"""
        self.code_preview.delete('1.0', tk.END)

        if not self.current_element or not self.css_content:
            return

        config = self.ELEMENTS[self.current_element]
        selector = config["selector"]

        block_start, block_end = self._find_css_block(selector)

        if block_start is not None and block_end is not None:
            brace_pos = self.css_content.rfind('{', 0, block_start)
            if brace_pos != -1:
                line_start = self.css_content.rfind('\n', 0, brace_pos)
                if line_start == -1:
                    line_start = 0
                else:
                    line_start += 1
            else:
                line_start = block_start

            full_rule = self.css_content[line_start:block_end+1]
            self.code_preview.insert('1.0', full_rule)
        else:
            self.code_preview.insert('1.0', f"/* 未找到 {selector} 相关代码 */\n\n请在CSS文件中搜索该选择器。")

    def reset_css(self):
        """重置到原始CSS"""
        if self.original_css:
            if messagebox.askyesno("确认", "确定要重置所有修改吗？\n这将恢复到导入时的原始状态。"):
                self.css_content = self.original_css
                self.parse_existing_values()
                self.refresh_element_buttons()
                self.status_var.set("🔄 已重置到原始状态")
                if self.current_element:
                    self.select_element(self.current_element)

    def save_css(self):
        """保存CSS文件"""
        if not self.css_content:
            messagebox.showwarning("提示", "没有可保存的内容！")
            return

        save_path = filedialog.asksaveasfilename(
            title="保存CSS文件",
            initialfile=os.path.basename(self.current_file) if self.current_file else "style.css",
            defaultextension=".css",
            filetypes=[("CSS文件", "*.css")]
        )

        if save_path:
            try:
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write(self.css_content)

                self.status_var.set(f"✅ 已保存")
                messagebox.showinfo("成功", f"文件已保存到:\n{save_path}")

            except Exception as e:
                messagebox.showerror("错误", f"保存失败:\n{e}")


def main():
    root = tk.Tk()
    app = OpenClawCSSTweaker(root)
    root.mainloop()


if __name__ == '__main__':
    main()
