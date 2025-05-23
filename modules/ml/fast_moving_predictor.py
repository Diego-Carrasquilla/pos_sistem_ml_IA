
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from pos_sistem.modules.ml.data_loader import load_data

def load_training_data():
    query = """
        SELECT 
            p.id, p.name, p.stock,
            IFNULL(SUM(sd.quantity), 0) AS total_sold,
            DATEDIFF(MAX(s.created_at), MIN(s.created_at)) AS active_days,
            MAX(s.created_at) AS last_sale_date
        FROM products p
        LEFT JOIN sale_details sd ON p.id = sd.product_id
        LEFT JOIN sales s ON sd.sale_id = s.id
        GROUP BY p.id, p.name
    """
    df = load_data(query)
    df["active_days"] = df["active_days"].replace(0, 1)
    df["sales_per_day"] = df["total_sold"] / df["active_days"]
    df["days_since_last_sale"] = (pd.Timestamp.today() - pd.to_datetime(df["last_sale_date"])).dt.days
    df["will_run_out_soon"] = (df["stock"] < 5).astype(int)
    return df, df["will_run_out_soon"]

def train_model():
    df, y = load_training_data()
    X = df.drop(columns=["id", "name", "last_sale_date", "will_run_out_soon"])
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

def predict_fast_products(model):
    df, _ = load_training_data()
    X = df.drop(columns=["id", "name", "last_sale_date", "will_run_out_soon"])
    predictions = model.predict(X)
    df["prediction"] = predictions
    return df[df["prediction"] == 1] 

