import tkinter as tk
from tkinter import messagebox
import random
import os
import sys
from PIL import Image, ImageDraw, ImageTk

# --- 核心辅助函数：处理打包后的资源路径 ---
def resource_path(relative_path):
    """ 获取资源绝对路径，兼容 PyInstaller 环境 """
    try:
        # 打包后指向临时根目录
        base_path = sys._MEIPASS
    except Exception:
        # 开发时指向项目根目录
        base_path = os.path.abspath(".")
    
    # 因为你的图片在 src 文件夹内，所以路径必须包含 src
    return os.path.join(base_path, "src", relative_path)

# GB 11533-2011 核心数据
VISION_DATA = [
    (4.0, "0.1", 72.72), (4.1, "0.12", 57.76), (4.2, "0.15", 45.88),
    (4.3, "0.2", 36.45), (4.4, "0.25", 28.95), (4.5, "0.3", 23.00),
    (4.6, "0.4", 18.27), (4.7, "0.5", 14.51), (4.8, "0.6", 11.53),
    (4.9, "0.8", 9.16),  (5.0, "1.0", 7.27),  (5.1, "1.2", 5.78),
    (5.2, "1.5", 4.59),  (5.3, "2.0", 3.64)
]

class VisionProfessionalSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("自我视力检查器")
        self.root.geometry("1200x900")
        
        self.px_per_mm = None
        self.mode = 1  
        self.zoom_scale = 1.0 
        self.current_index = 5
        self.tk_images = []
        self.original_imgs = {} 
        self.resize_timer = None
        
        self.setup_calibration_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def setup_calibration_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="屏幕校准", font=("微软雅黑", 20, "bold")).pack(pady=20)
        tk.Label(self.root, text="请测量蓝色方块的物理高度 (mm):", font=("微软雅黑", 12)).pack()
        
        self.calib_canvas = tk.Canvas(self.root, width=400, height=300, bg="white")
        self.calib_canvas.pack(pady=10)
        self.calib_canvas.create_rectangle(125, 75, 275, 225, fill="blue", outline="")
        
        self.entry = tk.Entry(self.root, font=("Arial", 16), width=10, justify='center')
        self.entry.pack(pady=10)
        self.entry.insert(0, "40")
        
        tk.Button(self.root, text="确认并进入系统", command=self.finish_calibration, 
                  bg="#4CAF50", fg="white", font=("微软雅黑", 12, "bold"), padx=30).pack(pady=10)

    def finish_calibration(self):
        try:
            val = float(self.entry.get())
            self.px_per_mm = 150 / val 
            self.load_resources()
            self.setup_main_screen()
        except:
            messagebox.showwarning("提示", "请输入有效数字")

    def load_resources(self):
        mapping = {2: "2.png", 3: "3.png", 4: "4.png", 5: "5.png", 6: "6.png", 7: "7.png"}
        for mode_id, filename in mapping.items():
            path = resource_path(filename)
            if os.path.exists(path):
                self.original_imgs[mode_id] = Image.open(path)
            else:
                # 若图片依然找不到，生成深灰色占位图
                placeholder = Image.new('RGB', (800, 600), color=(50, 50, 50))
                self.original_imgs[mode_id] = placeholder

    def setup_main_screen(self):
        self.clear_screen()
        for i in range(1, 8):
            self.root.bind(str(i), lambda e, m=i: self.set_mode(m))
        self.root.bind("<Left>", lambda e: self.change_mode(-1))
        self.root.bind("<Right>", lambda e: self.change_mode(1))
        self.root.bind("<MouseWheel>", self.handle_mouse_zoom)
        self.root.bind("<Up>", self.handle_up_key)
        self.root.bind("<Down>", self.handle_down_key)
        self.root.bind("<Configure>", self.on_window_resize)
        self.canvas = tk.Canvas(self.root, bg="white", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.status_bar = tk.Label(self.root, text="", bg="#1a1a1a", fg="#eee", font=("微软雅黑", 10), pady=3)
        self.status_bar.pack(fill=tk.X)
        self.refresh_display()

    def on_window_resize(self, event):
        if self.resize_timer: self.root.after_cancel(self.resize_timer)
        self.resize_timer = self.root.after(150, self.refresh_display)

    def handle_mouse_zoom(self, event):
        if self.mode == 1: return 
        if event.delta > 0: self.apply_zoom(1.1)
        else: self.apply_zoom(0.9)

    def handle_up_key(self, event):
        if self.mode == 1:
            if self.current_index > 0:
                self.current_index -= 1
                self.refresh_display()
        else:
            self.apply_zoom(1.1)

    def handle_down_key(self, event):
        if self.mode == 1:
            if self.current_index < len(VISION_DATA) - 1:
                self.current_index += 1
                self.refresh_display()
        else:
            self.apply_zoom(0.9)

    def apply_zoom(self, factor):
        self.zoom_scale *= factor
        self.zoom_scale = max(0.1, min(self.zoom_scale, 8.0))
        self.refresh_display()

    def set_mode(self, m):
        if self.mode != m:
            self.mode = m
            self.zoom_scale = 1.0 
            self.refresh_display()

    def change_mode(self, delta):
        new_mode = (self.mode + delta - 1) % 7 + 1
        self.set_mode(new_mode)

    def refresh_display(self):
        if not hasattr(self, 'canvas'): return
        self.canvas.delete("all")
        self.tk_images = []
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if w <= 10: return
        mode_names = ["1.标准视力表", "2.散光钟图", "3.红绿对比图", "4.蜂窝图1", "5.蜂窝图2", "6.交叉十字线", "7.Worth四点图"]
        self.status_bar.config(text=f"模式: {mode_names[self.mode-1]} | 快捷键: 1-7")
        self.canvas.config(bg="black" if self.mode in [3, 7] else "white")
        if self.mode == 1:
            self.draw_vision_chart(w, h)
        else:
            self.draw_external_image(w, h)

    def draw_external_image(self, w, h):
        img_orig = self.original_imgs.get(self.mode)
        if not img_orig: return
        limit_w, limit_h = w - 60, h - 100
        ratio = min(limit_w / img_orig.width, limit_h / img_orig.height, 1.0)
        final_w = int(img_orig.width * ratio * self.zoom_scale)
        final_h = int(img_orig.height * ratio * self.zoom_scale)
        if final_w < 1 or final_h < 1: return
        img_res = img_orig.resize((final_w, final_h), Image.Resampling.BILINEAR)
        tk_img = ImageTk.PhotoImage(img_res)
        self.tk_images.append(tk_img)
        self.canvas.create_image(w/2, h/2, image=tk_img)

    def draw_vision_chart(self, w, h):
        indices = [self.current_index - 1, self.current_index, self.current_index + 1]
        y_slots = [h * 0.25, h * 0.5, h * 0.75]
        for i, idx in enumerate(indices):
            if 0 <= idx < len(VISION_DATA):
                l_val, v_val, mm_size = VISION_DATA[idx]
                px_size = mm_size * self.px_per_mm 
                y_pos = y_slots[i]
                text_margin = 170 
                safe_l, safe_r = text_margin + (px_size / 2), w - (px_size / 2) - 60
                usable_w = safe_r - safe_l
                num = 1 if l_val <= 4.2 else (3 if l_val <= 4.5 else (5 if l_val <= 4.8 else 8))
                if usable_w > 0:
                    if num > 1:
                        step = usable_w / (num - 1)
                        for n in range(num): self.draw_single_e(safe_l + (n * step), y_pos, px_size)
                    else: self.draw_single_e(safe_l + usable_w/2, y_pos, px_size)
                self.canvas.create_rectangle(0, y_pos-80, text_margin, y_pos+80, fill="white", outline="")
                self.canvas.create_text(40, y_pos, text=f"V {v_val}", font=("Arial", 18, "bold"), anchor="w")
                self.canvas.create_text(110, y_pos, text=f"L {l_val}", font=("Arial", 14), anchor="w", fill="#444")
        self.canvas.create_text(w/2, h - 40, text="测量距离: 5米", font=("微软雅黑", 16, "bold"), fill="#d32f2f")

    def draw_single_e(self, x, y, size):
        sz = max(2, int(size))
        base = 500
        img = Image.new("RGBA", (base, base), (255, 255, 255, 0))
        d = ImageDraw.Draw(img)
        u = base/5
        for i in range(3): d.rectangle([0, i*u*2, base, i*u*2+u], fill="black")
        d.rectangle([0, 0, u, base], fill="black")
        img = img.rotate(random.choice([0, 90, 180, 270])).resize((sz, sz), Image.Resampling.LANCZOS)
        tk_img = ImageTk.PhotoImage(img)
        self.tk_images.append(tk_img)
        self.canvas.create_image(x, y, image=tk_img)

if __name__ == "__main__":
    root = tk.Tk()
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except: pass
    app = VisionProfessionalSystem(root)
    root.mainloop()