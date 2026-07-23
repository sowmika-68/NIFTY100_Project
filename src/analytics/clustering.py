import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Database path
DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"


def get_connection():
    """
    Create and return a SQLite database connection.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def load_clustering_data():
    """
    Load the latest financial ratios required for clustering.
    """
    conn = get_connection()

    query = """
        SELECT
            c.id AS company_id,
            c.company_name,
            s.broad_sector,
            fr.return_on_equity_pct,
            fr.debt_to_equity,
            fr.operating_profit_margin_pct,
            fr.free_cash_flow_cr
        FROM companies c
        LEFT JOIN sectors s
            ON c.id = s.company_id
        LEFT JOIN financial_ratios fr
            ON c.id = fr.company_id
        WHERE fr.id = (
            SELECT MAX(f2.id)
            FROM financial_ratios f2
            WHERE f2.company_id = c.id
        )
        ORDER BY c.company_name;
        """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df

    df["company_name"] = (
        df["company_name"]
        .fillna("")
        .str.replace(r"[\r\n]+", " ", regex=True)
        .str.strip()
    )

    df["broad_sector"] = (
        df["broad_sector"]
        .fillna("Unknown")
        .str.strip()
    )
def impute_sector_median(df):
    """Replace missing numeric values with the median within each broad sector."""

    numeric_columns = [
        "return_on_equity_pct",
        "debt_to_equity",
        "operating_profit_margin_pct",
        "free_cash_flow_cr",
    ]

    for column in numeric_columns:
        df[column] = (
            df.groupby("broad_sector")[column]
            .transform(lambda x: x.fillna(x.median()))
        )

    print("\nMissing Values After Imputation:")
    
    print(df.isnull().sum())

    return df
    
    

def scale_features(df):
    """
    Standardize clustering features.
    """

    features = [
        "return_on_equity_pct",
        "debt_to_equity",
        "operating_profit_margin_pct",
        "free_cash_flow_cr"
    ]

    scaler = StandardScaler()

    scaled = scaler.fit_transform(df[features])

    print("\nScaled Data Statistics:")
    print(pd.DataFrame(scaled, columns=features).describe())

    return scaled



def generate_elbow_plot(data):
    """
    Generate and save the KMeans elbow plot.
    """

    inertia = []

    for k in range(2, 11):
        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10
        )

        model.fit(data)

        inertia.append(model.inertia_)

    plt.figure(figsize=(8, 5))

    plt.plot(range(2, 11), inertia, marker="o")

    plt.title("KMeans Elbow Method")
    plt.xlabel("Number of Clusters")
    plt.ylabel("Inertia")
    plt.grid(True)

    output_path = PROJECT_ROOT / "reports" / "elbow_plot.png"

    plt.savefig(output_path)

    plt.close()

    print(f"Elbow plot saved to: {output_path}")

def run_kmeans(df, scaled_data):
    """
    Run KMeans clustering and return the DataFrame with cluster assignments.
    """
    model = KMeans(
        n_clusters=5,
        random_state=42,
        n_init=10
    )

    cluster_ids = model.fit_predict(scaled_data)

    df["cluster_id"] = cluster_ids

    # Distance from assigned centroid
    distances = model.transform(scaled_data)

    df["distance_from_centroid"] = [
        round(distances[i][cluster_ids[i]], 4)
        for i in range(len(df))
    ]

    cluster_names = {
        0: "Cluster 0",
        1: "Cluster 1",
        2: "Cluster 2",
        3: "Cluster 3",
        4: "Cluster 4"
    }

    df["cluster_name"] = df["cluster_id"].map(cluster_names)

    return df

def save_cluster_labels(df):
    """
    Save cluster assignments to CSV.
    """
    output_path = PROJECT_ROOT / "output" / "cluster_labels.csv"

    columns = [
        "company_id",
        "company_name",
        "cluster_id",
        "cluster_name",
        "distance_from_centroid"
    ]

    df[columns].to_csv(output_path, index=False)

    print(f"\nCluster labels saved to: {output_path}")


def main():
    print("Database connected successfully!")
    print(f"Database Path: {DB_PATH}")

    # Load data
    df = load_clustering_data()
    # Clean text columns
    df["company_name"] = (
        df["company_name"]
        .astype(str)
        .str.replace(r"[\r\n]+", " ", regex=True)
        .str.strip()
    )

    df["broad_sector"] = (
        df["broad_sector"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )
    print(df["company_name"].head())

    print("\nFirst 5 Rows:")
    print(df.head())

    print(f"\nRows Loaded: {len(df)}")

    # Fill missing values
    df = impute_sector_median(df)

    print("\nMissing Values After Imputation:")
    print(df.isnull().sum())

    # Scale features
    scaled_data = scale_features(df)

    df = run_kmeans(df, scaled_data)
    print("\nCluster Counts:")
    print(df["cluster_id"].value_counts().sort_index())
    save_cluster_labels(df)

    print("\nScaled Data Shape:")
    print(scaled_data.shape)

    # Generate elbow plot
    generate_elbow_plot(scaled_data)

    print("\nDay 36 Steps Completed Successfully!")



if __name__ == "__main__":
    main()