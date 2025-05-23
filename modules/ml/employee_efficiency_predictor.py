import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from pos_sistem.modules.ml.data_loader import load_data

def get_employee_efficiency(top_n=5):
    query = """
        SELECT 
            e.name AS employee_name,
            COUNT(s.id) AS total_sales,
            SUM(s.total) AS total_amount,
            MIN(s.created_at) AS first_sale,
            MAX(s.created_at) AS last_sale
        FROM employees e
        JOIN sales s ON e.id = s.employee_id
        GROUP BY e.id
    """
    df = load_data(query)

    df['first_sale'] = pd.to_datetime(df['first_sale'])
    df['last_sale'] = pd.to_datetime(df['last_sale'])
    df['days_active'] = (df['last_sale'] - df['first_sale']).dt.days + 1

    df['sales_per_day'] = df['total_sales'] / df['days_active']
    df['amount_per_day'] = df['total_amount'] / df['days_active']

    scaler = MinMaxScaler()
    df[['total_sales', 'total_amount', 'sales_per_day', 'amount_per_day']] = scaler.fit_transform(
        df[['total_sales', 'total_amount', 'sales_per_day', 'amount_per_day']]
    )

    df['efficiency_score'] = df[['total_sales', 'total_amount', 'sales_per_day', 'amount_per_day']].mean(axis=1)

    return df.sort_values(by='efficiency_score', ascending=False).head(top_n)
