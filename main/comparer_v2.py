from tkinter import *
from tkinter import ttk
from collections import Counter  # 新增导入
def compare_data(f1, f2):
    result_text.delete(1.0, END)
    
    # 增强数据清洗逻辑（支持多种分隔符）
    list1 = [x.strip() for x in f1.replace("，", ",").split(",") if x.strip()]
    list2 = [x.strip() for x in f2.replace("，", ",").split(",") if x.strip()]
    
    # 新增：统计重复项具体值
    counter1 = Counter(list1)
    counter2 = Counter(list2)
    
    # 获取重复项列表（出现次数>1的项）
    dup_items1 = [item for item, count in counter1.items() if count > 1]
    dup_items2 = [item for item, count in counter2.items() if count > 1]
    
    set1, set2 = set(list1), set(list2)
    
    # 统计结果格式化输出
    result_text.insert(END, "▬▬▬ 数据统计结果 ▬▬▬\n\n")
    result_text.insert(END, f"▪ 数据列1条目总数: {len(list1)} (重复项: {len(list1)-len(set1)})\n")
    if dup_items1:
        result_text.insert(END, f"🔍 重复项具体值：{', '.join(dup_items1) if dup_items1 else '无'}\n\n")  # 新增
    
    result_text.insert(END, f"▪ 数据列2条目总数: {len(list2)} (重复项: {len(list2)-len(set2)})\n")
    if dup_items2:
        result_text.insert(END, f"🔍 重复项具体值：{', '.join(dup_items2) if dup_items2 else '无'}\n\n")  # 新增
    
    
    # 交集与差集分析
    common = set1 & set2
    result_text.insert(END, f"🔍 共有值 ({len(common)}个):\n{', '.join(common) or '无'}\n\n")
    
    diff1 = set1 - set2
    result_text.insert(END, f"🔍 仅数据列1有 ({len(diff1)}个):\n{', '.join(diff1) or '无'}\n\n")
    
    diff2 = set2 - set1
    result_text.insert(END, f"🔍 仅数据列2有 ({len(diff2)}个):\n{', '.join(diff2) or '无'}")

def validate_input():
    # 获取entry1中的输入并去除首尾空格
    f1 = entry1.get().strip()
    f2 = entry2.get().strip()
    
    result_text.delete(1.0, END)
    
    if not f1 and not f2:
        result_text.insert(END, "⚠️ 错误：两列数据均为空！")
        return False
    if not f1:
        result_text.insert(END, "⚠️ 错误：数据列1为空！")
        return False
    if not f2:
        result_text.insert(END, "⚠️ 错误：数据列2为空！")
        return False

    if "," not in f1 or "," not in f2:
        result_text.insert(END, "⚠️ 错误：数据少于2，且请用英标的逗号\",\"分隔数据（例：C1, C2, C3）")
        return False
    return True

def execute_compare():
    if validate_input():
        compare_data(entry1.get(), entry2.get())

def clear_output():
    result_text.delete(1.0, END)
    result_text.insert(END, "输出内容已清空\n")
    entry1.focus()

def reset_all():
    entry1.delete(0, END)
    entry2.delete(0, END)
    result_text.delete(1.0, END)
    result_text.insert(END, "系统已重置\n")
    entry1.focus()

def GUI_main():
    window = Tk()
    window.title("数据对比分析工具 v2.1")
    window.geometry("600x400")

    # 设置窗口始终在最前
    window.attributes("-topmost", True)
    
    # === 主布局配置 ===
    window.columnconfigure(0, weight=1)
    window.rowconfigure(2, weight=1)  # 网页5网格权重配置
    
    # === 输入区域 ===
    input_frame = ttk.Frame(window, padding=(20, 10))
    input_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)
    
    # 输入框1（自适应实现）
    ttk.Label(input_frame, text="数据列1（逗号分隔）:", font=('微软雅黑', 11)).grid(row=0, column=0, sticky="w")
    global entry1
    entry1 = ttk.Entry(input_frame, font=('微软雅黑', 11))
    entry1.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
    
    # 输入框2（相同配置）
    ttk.Label(input_frame, text="数据列2（逗号分隔）:", font=('微软雅黑', 11)).grid(row=1, column=0, sticky="w")
    global entry2
    entry2 = ttk.Entry(input_frame, font=('微软雅黑', 11))
    entry2.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
    
    # 输入区域网格配置
    input_frame.columnconfigure(1, weight=1)  # 网页8列权重设置
    
    # === 按钮区域 ===
    btn_frame = ttk.Frame(window)
    btn_frame.grid(row=1, column=0, pady=15, sticky="ew")
    
    ttk.Button(btn_frame, text="执行对比", command=execute_compare, width=15).pack(side=LEFT, padx=10)
    ttk.Button(btn_frame, text="清空输出", command=clear_output, width=15).pack(side=LEFT, padx=10)
    ttk.Button(btn_frame, text="重置系统", command=reset_all, width=15).pack(side=LEFT, padx=10)
    
    # === 输出区域 ===
    output_frame = ttk.Frame(window)
    output_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
    
    # 带滚动条的文本框
    global result_text
    scroll_y = ttk.Scrollbar(output_frame)
    scroll_x = ttk.Scrollbar(output_frame, orient=HORIZONTAL)
    
    result_text = Text(output_frame, 
                      wrap=NONE,  # 允许水平滚动
                      font=('等线', 11),
                      yscrollcommand=scroll_y.set,
                      xscrollcommand=scroll_x.set,
                      padx=15, 
                      pady=15,
                      bg="#f8f9fa")
    
    scroll_y.config(command=result_text.yview)
    scroll_x.config(command=result_text.xview)
    
    # 布局配置（网页5网格布局优化）
    result_text.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")
    
    # 输出区域自适应配置
    output_frame.columnconfigure(0, weight=1)
    output_frame.rowconfigure(0, weight=1)
    
    # === 窗口缩放处理 ===
    window.bind("<Configure>", lambda e: window.update_idletasks())  # 网页1自适应刷新
    
    # 初始焦点设置
    entry1.focus()
    
    window.mainloop()

if __name__ == "__main__":
    GUI_main()