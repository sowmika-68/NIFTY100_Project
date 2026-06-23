def normalize_ticker(value):
    return str(value).strip().upper()

def normalize_year(value):
    return int(value)

def normalize_ticker(value):
    return str(value).strip().upper()

def normalize_year(value):
    return int(float(value))


def normalize_columns(df):
    df.columns = (
        df.columns
          .str.strip()
          .str.lower()
          .str.replace(" ", "_")
    )
    return df