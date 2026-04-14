import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ================== 配置区域 ==================
DATA_FILE = "sphere_data.csv"          # 你的数据文件名
PLOT_TRAJECTORY = True                 # 是否绘制轨迹图
PLOT_PHASE_PORTRAIT = True             # 是否绘制相图
PLOT_ERROR_TIME = True                 # 是否绘制误差随时间变化
SAVE_FIGURES = True                    # 是否保存图片（否则仅显示）
OUTPUT_PREFIX = "sphere_analysis"      # 输出图片前缀
# =============================================

def load_data(filename):
    """读取CSV数据，自动跳过以#开头的注释行"""
    # 先读取文件内容，跳过注释行
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if not line.startswith('#') and line.strip() != '']
    if not lines:
        raise ValueError("文件中没有有效数据")
    
    # 将数据转换为DataFrame
    from io import StringIO
    data_str = '\n'.join(lines)
    df = pd.read_csv(StringIO(data_str), header=None)
    
    # 列名顺序：time, px, py, vx, vy, ex, ey, tx, ty
    df.columns = ['time', 'px', 'py', 'vx', 'vy', 'ex', 'ey', 'tx', 'ty']
    return df

def plot_trajectory(df):
    """绘制球体在水平面（X-Y）上的运动轨迹以及目标点位置"""
    plt.figure(figsize=(8, 6))
    plt.plot(df['px'], df['py'], 'b-', linewidth=1.5, alpha=0.8, label='Sphere path')
    # 标记起点
    plt.plot(df['px'].iloc[0], df['py'].iloc[0], 'go', markersize=8, label='Start')
    # 标记终点
    plt.plot(df['px'].iloc[-1], df['py'].iloc[-1], 'ro', markersize=8, label='End')
    # 绘制目标点（假设目标点不变，取第一帧的目标坐标；若目标在动，可以绘制轨迹）
    target_x = df['tx'].iloc[0]
    target_y = df['ty'].iloc[0]
    plt.plot(target_x, target_y, 'm*', markersize=12, label='Target')
    
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.title('Horizontal Trajectory')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    if SAVE_FIGURES:
        plt.savefig(f"{OUTPUT_PREFIX}_trajectory.png", dpi=200)
    plt.show()

def plot_phase_portrait(df):
    """绘制X和Y方向的相图（位置误差 vs 速度）"""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # X方向相图
    ax = axes[0]
    ax.plot(df['ex'], df['vx'], 'b-', alpha=0.6, linewidth=0.8)
    ax.plot(df['ex'].iloc[0], df['vx'].iloc[0], 'go', markersize=6, label='Start')
    ax.plot(df['ex'].iloc[-1], df['vx'].iloc[-1], 'ro', markersize=6, label='End')
    ax.set_xlabel('Error X')
    ax.set_ylabel('Velocity X')
    ax.set_title('Phase Portrait (X-axis)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='k', linestyle='--', linewidth=0.8)
    ax.axvline(x=0, color='k', linestyle='--', linewidth=0.8)
    
    # Y方向相图
    ax = axes[1]
    ax.plot(df['ey'], df['vy'], 'r-', alpha=0.6, linewidth=0.8)
    ax.plot(df['ey'].iloc[0], df['vy'].iloc[0], 'go', markersize=6, label='Start')
    ax.plot(df['ey'].iloc[-1], df['vy'].iloc[-1], 'ro', markersize=6, label='End')
    ax.set_xlabel('Error Y')
    ax.set_ylabel('Velocity Y')
    ax.set_title('Phase Portrait (Y-axis)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='k', linestyle='--', linewidth=0.8)
    ax.axvline(x=0, color='k', linestyle='--', linewidth=0.8)
    
    plt.tight_layout()
    if SAVE_FIGURES:
        plt.savefig(f"{OUTPUT_PREFIX}_phase.png", dpi=200)
    plt.show()

def plot_error_time(df):
    """绘制误差和速度随时间变化的曲线"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    # 误差随时间变化
    ax = axes[0, 0]
    ax.plot(df['time'], df['ex'], 'b-', label='Error X')
    ax.plot(df['time'], df['ey'], 'r-', label='Error Y')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Position Error')
    ax.set_title('Position Error vs Time')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 速度随时间变化
    ax = axes[0, 1]
    ax.plot(df['time'], df['vx'], 'b-', label='Velocity X')
    ax.plot(df['time'], df['vy'], 'r-', label='Velocity Y')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Velocity')
    ax.set_title('Velocity vs Time')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 位置随时间变化（与目标对比）
    ax = axes[1, 0]
    ax.plot(df['time'], df['px'], 'b-', label='Pos X')
    ax.plot(df['time'], df['py'], 'r-', label='Pos Y')
    # 目标水平线（假设目标不变）
    ax.axhline(y=df['tx'].iloc[0], color='b', linestyle='--', alpha=0.5, label='Target X')
    ax.axhline(y=df['ty'].iloc[0], color='r', linestyle='--', alpha=0.5, label='Target Y')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Position')
    ax.set_title('Position vs Time')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 2D 误差范数（标量距离）随时间变化
    ax = axes[1, 1]
    distance = np.sqrt(df['ex']**2 + df['ey']**2)
    ax.plot(df['time'], distance, 'g-', label='Distance to target')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Distance')
    ax.set_title('Distance to Target vs Time')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    if SAVE_FIGURES:
        plt.savefig(f"{OUTPUT_PREFIX}_timeseries.png", dpi=200)
    plt.show()

def main():
    try:
        df = load_data(DATA_FILE)
        print(f"成功加载 {len(df)} 行数据，时间跨度 {df['time'].max() - df['time'].min():.2f} 秒")
        
        if PLOT_TRAJECTORY:
            plot_trajectory(df)
        if PLOT_PHASE_PORTRAIT:
            plot_phase_portrait(df)
        if PLOT_ERROR_TIME:
            plot_error_time(df)
            
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    main()