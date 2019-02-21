import pandas as pd

def format_df(df_in, dtype_map):
    df = df_in.copy()
    for col, col_type in dtype_map.items():
        if col_type == 'datetime':
            df[col] = pd.to_datetime(df[col])
        else:
            df[col] = df[col].astype(col_type)
    return df