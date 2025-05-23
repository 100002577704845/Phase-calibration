import numpy as np
import os
import pandas as pd

# === 初始化 ===
N = 16                  # Ny=Nx=16
TX_RX_list = [0, 1]
stepsize_list = [0, 85, 170, 255]
# 產生 2*8=8 個 N*N 的複數矩陣
T_dict = {(tx, step): np.zeros((N, N), dtype=complex) for tx in TX_RX_list for step in stepsize_list}

# 相對座標
bfic_offset = [(0, 0), (2, 0), (2, 2), (0, 2)]
channel_offset = [(0, 0), (1, 0), (1, 1), (0, 1)]

def read(tx_rx, step, group_id, bfic_id, ch_id, base_dir="received_complex_files"):
    # 找出每個元素定義的座標位置
    group_row = group_id // 4
    group_col = group_id % 4
    y0 = group_row * 4 + bfic_offset[bfic_id][0] + channel_offset[ch_id][0]
    x0 = group_col * 4 + bfic_offset[bfic_id][1] + channel_offset[ch_id][1]

    filename = f"TX_RX_{tx_rx}_step_{step}_G_{group_id}_BFIC_{bfic_id}_CH_{ch_id}.csv"   # G:group, CH:channel
    filepath = os.path.join(base_dir, filename)
    try:
        df = pd.read_csv(filepath)
        value = complex(str(df["value"].iloc[0]).replace(" ", "").replace("i", "j"))    # 從value讀取第0筆複數，轉為python能處理的複數
        T_dict[(tx_rx, step)][y0, x0] = value                                           # 把值寫入對應的矩陣
        return True
    except Exception as e:
        print(f"[錯誤] {filepath}: {e}")
        return False
# read 全部的 complex response
def read_all(base_dir="received_complex_response"):
    for tx in TX_RX_list:
        for step in stepsize_list:
            for g in range(16):         # group
                for b in range(4):      # BFIC
                    for c in range(4):  # channel
                        read(tx, step, g, b, c, base_dir=base_dir)
# 儲存 2*4=8 個 complex response table 為 csv 檔
def save_all_tables(output_dir="complex_response_table"):
    os.makedirs(output_dir, exist_ok=True)
    for (tx_rx, step), mat in T_dict.items():
        mode = "TX" if tx_rx == 0 else "RX"
        fname = f"T_{mode}_step_{step}.csv"
        pd.DataFrame(mat).to_csv(os.path.join(output_dir, fname), index=False, header=False)
    print(f"已儲存所有 table 至 {output_dir}/")
