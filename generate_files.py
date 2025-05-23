import numpy as np
import os
import pandas as pd

TX_RX_list = [0, 1]                 # 0 for TX,1 for RX
stepsize_list = [0, 85, 170, 255]   # 4 type of stepsize
group_list = range(16)              # group : 0~15
bfic_list = range(4)                # BFIC : 0~3
channel_list = range(4)             # channel : 0~3

output_dir = "received_complex_response"
os.makedirs(output_dir, exist_ok=True)

file_count = 0
for tx_rx in TX_RX_list:
    for step in stepsize_list:
        for group in group_list:
            for bfic in bfic_list:
                for ch in channel_list:
                    # 產生隨機複數：real 和 imag 都在 [0, 1) 區間
                    real_part = np.random.uniform(0, 1)
                    imag_part = np.random.uniform(0, 1)
                    sample_value = f"{real_part}+{imag_part}j"

                    # 建立 DataFrame
                    df = pd.DataFrame([{
                        "TX_RX": tx_rx,
                        "step": step,
                        "group": group,
                        "BFIC": bfic,
                        "channel": ch,
                        "value": sample_value
                    }])

                    filename = f"TX_RX_{tx_rx}_step_{step}_G_{group}_BFIC_{bfic}_CH_{ch}.csv"
                    filepath = os.path.join(output_dir, filename)
                    df.to_csv(filepath, index=False)

                    file_count += 1

print(f"產生 {file_count} 個含 metadata 的複數 CSV 檔案在資料夾 {output_dir}")
