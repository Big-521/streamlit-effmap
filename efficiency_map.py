import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import griddata
from matplotlib.colors import ListedColormap
from matplotlib.ticker import FuncFormatter
import os
import matplotlib.font_manager as fm

def process_efficiency_map(file_path, chart_title, plot_curve=True, contour_interval=2):
    # ==== 字体配置区块 ====
    font_path = "/usr/share/fonts/wqy-microhei/wqy-microhei.ttc"
    if os.path.exists(font_path):
        my_font = fm.FontProperties(fname=font_path)
        font_name = my_font.get_name()
        plt.rcParams.update({
            'font.family': font_name,
            'font.size': 12,
            'axes.unicode_minus': False,
            'axes.titlesize': 16,
            'axes.labelsize': 14,
            'xtick.labelsize': 12,
            'ytick.labelsize': 12,
            'figure.titlesize': 16,
            'legend.fontsize': 12
        })
        print("✅ 字体设置成功:", font_name)
    else:
        print("⚠️ 未找到中文字体，图表可能乱码")
        my_font = None

    # ==== 数据读取 ====
    data = pd.read_excel(file_path, engine='openpyxl')
    X = data['输入转速<r/min>'].values
    Y = data['输入转矩<N.m>'].values
    Z = data['系统效率'].values

    # ==== 色图设置 ====
    jet = plt.get_cmap('jet', 256)
    newcolors = jet(np.linspace(0, 1, 256))
    newcolors[0] = [1, 1, 1, 1]  # 白色表示无数据
    newcmp = ListedColormap(newcolors)

    # ==== 网格插值 ====
    xi = np.linspace(0, X.max(), 250)
    yi = np.linspace(0, Y.max(), 250)
    Xi, Yi = np.meshgrid(xi, yi)
    Zi = griddata((X, Y), Z, (Xi, Yi), method='linear')

    # ==== 外特性曲线计算 ====
    different = np.unique(X)
    num_different = len(different)
    E = np.zeros((2, num_different))
    R = np.zeros((2, num_different))

    for idx, val in enumerate(different):
        E[0, idx] = val
        R[0, idx] = val
        y_vals = Y[X == val]
        if len(y_vals) > 0:
            E[1, idx] = y_vals.max()
            R[1, idx] = y_vals.min()
        else:
            E[1, idx] = np.nan
            R[1, idx] = np.nan

    rpmmin = E[0, :]
    torquemin = E[1, :]
    rpmmax = R[0, :]
    torquemax = R[1, :]

    # ==== 蒙版处理 ====
    red_line_interp = np.interp(xi, rpmmin, torquemin)
    mask = Yi <= red_line_interp[np.newaxis, :]
    Zi_masked = np.where(mask, Zi, np.nan)

    # ==== 图像绘制 ====
    fig, ax = plt.subplots(figsize=(10, 8))
    cf = ax.contourf(Xi, Yi, Zi_masked, 43, cmap=newcmp)

    # ==== 等高线 ====
    levels = np.arange(85, 100, contour_interval)
    contour = ax.contour(Xi, Yi, Zi_masked, levels=levels, colors='black', linewidths=1)
    ax.clabel(contour, contour.levels, inline=True, fontsize=10, fmt="%.0f")

    # ==== 散点图（隐藏） ====
    sc = ax.scatter(X, Y, c=Z, cmap=newcmp, s=50, edgecolors='k')
    cb = fig.colorbar(sc, ax=ax, label='效率%')
    cb.set_label('效率%', fontsize=14, fontproperties=my_font)  # 设置标签字体
    cb.ax.tick_params(labelsize=12)
    sc.set_visible(False)

    # ==== 外特性边界线 ====
    if plot_curve:
        ax.plot(rpmmin, torquemin, 'k-', linewidth=3, label="最小边界")
        ax.plot(rpmmax, torquemax, 'g-', label="最大边界")

    # ==== 坐标轴设置 ====
    ax.set_xlabel('转速 r/min', fontsize=14, fontproperties=my_font)
    ax.set_ylabel('扭矩 N·m', fontsize=14, fontproperties=my_font)
    ax.set_title(chart_title, fontsize=16, fontproperties=my_font)
    ax.grid(False)
    ax.tick_params(axis='both')
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x)}'))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{int(y)}'))
    ax.set_ylim(bottom=Y.min())
    ax.set_xlim(left=X.min())

    # ==== 保存 ====
    os.makedirs("output", exist_ok=True)
    output_path = os.path.join("output", "efficiency_map.png")
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    return output_path
