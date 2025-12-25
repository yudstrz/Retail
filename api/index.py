from flask import Flask, jsonify, request
import pandas as pd
import os

app = Flask(__name__)

# Global cache for data to avoid reloading on every request (warm start)
df = None

def load_data():
    global df
    if df is None:
        # Path to data.parquet relative to api/index.py
        # Vercel bundles files in the same directory
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(base_dir, 'data.parquet')
        
        if os.path.exists(data_path):
            try:
                df = pd.read_parquet(data_path)
                # Ensure datetime and necessary columns
                if 'InvoiceDate' in df.columns:
                    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
                    df['Year'] = df['InvoiceDate'].dt.year
                    df['Month'] = df['InvoiceDate'].dt.month
                    df['YearMonth'] = df['InvoiceDate'].dt.to_period("M").astype(str)
                
                # Calculate Revenue if not present
                if 'Revenue' not in df.columns and 'Quantity' in df.columns and 'UnitPrice' in df.columns:
                    df['Revenue'] = df['Quantity'] * df['UnitPrice']
            except Exception as e:
                print(f"Error loading data: {e}")
                df = pd.DataFrame()
        else:
            print(f"Data file not found at {data_path}")
            df = pd.DataFrame()
            
    return df

@app.route('/api/filters')
def get_filters():
    data = load_data()
    if data.empty: return jsonify({"years": [], "months": []})
    
    years = sorted(data["Year"].unique().tolist())
    months = sorted(data["Month"].unique().tolist())
    return jsonify({"years": years, "months": months})

@app.route('/api/stats')
def get_stats():
    data = load_data()
    if data.empty: return jsonify({"error": "No data"}), 500

    year = request.args.get('year')
    month = request.args.get('month')
    
    filtered = data.copy()
    if year and year != 'All': filtered = filtered[filtered['Year'] == int(year)]
    if month and month != 'All': filtered = filtered[filtered['Month'] == int(month)]
    
    total_revenue = filtered['Revenue'].sum()
    total_orders = filtered['InvoiceNo'].nunique()
    total_customers = filtered['CustomerID'].nunique()
    
    top_product = "N/A"
    if not filtered.empty:
        top_product = filtered.groupby("Description")["Quantity"].sum().idxmax()
        
    aov = total_revenue / total_orders if total_orders > 0 else 0
    purchase_freq = total_orders / total_customers if total_customers > 0 else 0
    clv = aov * purchase_freq
    
    return jsonify({
        "revenue": total_revenue,
        "orders": total_orders,
        "customers": total_customers,
        "top_product": str(top_product),
        "aov": aov,
        "clv": clv
    })

@app.route('/api/revenue')
def get_revenue():
    data = load_data()
    if data.empty: return jsonify([])

    year = request.args.get('year')
    month = request.args.get('month')
    
    filtered = data.copy()
    if year and year != 'All': filtered = filtered[filtered['Year'] == int(year)]
    if month and month != 'All': filtered = filtered[filtered['Month'] == int(month)]

    trend = filtered.groupby("YearMonth")["Revenue"].sum().reset_index()
    return jsonify(trend.to_dict(orient='records'))

@app.route('/api/retention')
def get_retention():
    data = load_data()
    if data.empty: return jsonify([])
    
    # Retention is typically calculated over the whole dataset or sliding window
    # We will use the original logic (whole dataset)
    customer_month = data.groupby(["CustomerID", "YearMonth"]).size().reset_index(name="purchases")
    months = sorted(customer_month["YearMonth"].unique())
    
    retention_data = []
    for i in range(1, len(months)):
        prev = customer_month[customer_month["YearMonth"] == months[i-1]]["CustomerID"].unique()
        curr = customer_month[customer_month["YearMonth"] == months[i]]["CustomerID"].unique()
        retained = len(set(prev) & set(curr))
        rate = retained / len(prev) if len(prev) > 0 else 0
        retention_data.append({
            "Month": str(months[i]),
            "RetentionRate": rate,
            "ChurnRate": 1 - rate
        })
        
    return jsonify(retention_data)
    
if __name__ == '__main__':
    app.run(debug=True)
