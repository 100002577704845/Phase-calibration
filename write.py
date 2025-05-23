import numpy as np
import pandas as pd
import os
import re

bfic_offset = [(0, 0), (2, 0), (2, 2), (0, 2)]
channel_offset = [(0, 0), (1, 0), (1, 1), (0, 1)]

def write(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if not filename.endswith(".csv"):
            continue

        match = re.match(r"T_(TX|RX)_step_(\d+)\.csv", filename)
        if not match:
            continue

        tx_rx = 0 if match.group(1) == "TX" else 1
        step = int(match.group(2))
        ideal_phase = (step / 255.0) * 2 * np.pi

        input_path = os.path.join(input_folder, filename)
        try:
            df = pd.read_csv(input_path, header=None)
        except Exception as e:
            print(f"無法讀取 {input_path}: {e}")
            continue

        for group_id in range(16):
            for bfic_id in range(4):
                for ch_id in range(4):
                    group_row = group_id // 4
                    group_col = group_id % 4
                    bfic_dy, bfic_dx = bfic_offset[bfic_id]
                    ch_dy, ch_dx = channel_offset[ch_id]
                    y = group_row * 4 + bfic_dy + ch_dy
                    x = group_col * 4 + bfic_dx + ch_dx

                    try:
                        val = str(df.iat[y, x]).replace(" ", "").replace("i", "j")  # 從value讀取第0筆複數，轉為python能處理的複數
                        c = complex(val)
                        measured_phase = np.angle(c)
                        phase_correction = (ideal_phase - measured_phase) % (2 * np.pi)                 # 確保 phase 在 0~2pi
                        phase_correction = int(np.round(255 * phase_correction / (2 * np.pi))) % 256    # 確保轉成 bits 沒有小數
                    except Exception as e:
                        print(f"相位錯誤 {filename} @ ({y},{x}): {e}")
                        continue

                    # 儲存為獨立 csv
                    out_data = pd.DataFrame([{
                        "TX_RX": tx_rx,
                        "step": step,
                        "group": group_id,
                        "BFIC": bfic_id,
                        "channel": ch_id,
                        "phase": phase_correction
                    }])
                    out_filename = f"TX_RX_{tx_rx}_step_{step}_G_{group_id}_BFIC_{bfic_id}_CH_{ch_id}.csv"
                    out_path = os.path.join(output_folder, out_filename)
                    out_data.to_csv(out_path, index=False)
                    print(f"儲存: {out_filename}")
