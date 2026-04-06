from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)
CSV_FILE = "stock_history.csv"

# Create a dummy CSV if it doesn't exist
if not os.path.exists(CSV_FILE):
    print(f"{CSV_FILE} not found. Creating a dummy CSV...")
    dummy_data = {
        "Open": list(range(100, 131)),
        "Close": list(range(101, 132)),
        "High": list(range(102, 133)),
        "Low": list(range(99, 130))
    }
    pd.DataFrame(dummy_data).to_csv(CSV_FILE, index=False)
    print(f"{CSV_FILE} created successfully.")

@app.route('/')
def index():
    history = pd.read_csv(CSV_FILE)

    # Take last 30 rows
    history = history.tail(30)

    # Ensure 'Date' column exists
    if 'Date' not in history.columns:
        history['Date'] = pd.date_range(end=pd.Timestamp.today(), periods=len(history)).strftime('%Y-%m-%d')

    dates = history['Date'].tolist()

    # Collect datasets dynamically (all except Date)
    datasets = []
    for col in history.columns:
        if col != 'Date':
            datasets.append({
                "label": col,
                "data": history[col].tolist()
            })

    return render_template(
        "index.html",
        dates=dates,
        datasets=datasets
    )

if __name__ == "__main__":
    app.run(debug=True)