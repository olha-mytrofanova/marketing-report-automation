import pandas as pd
from jinja2 import Template
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

# Load data
df = pd.read_csv("data.csv")
df["date"] = pd.to_datetime(df["date"])

# Aggregate by channel
by_channel = df.groupby("channel").agg(
    impressions=("impressions", "sum"),
    clicks=("clicks", "sum"),
    spend=("spend", "sum"),
    revenue=("revenue", "sum")
).reset_index()

# Calculate KPIs
by_channel["ctr"] = (by_channel["clicks"] / by_channel["impressions"] * 100).round(2)
by_channel["roas"] = (by_channel["revenue"] / by_channel["spend"]).round(2)

total_spend = df["spend"].sum()
total_revenue = df["revenue"].sum()
total_roas = round(total_revenue / total_spend, 2)

# Generate ROAS bar chart
fig, ax = plt.subplots(figsize=(8, 4))
colors = ['#3498db', '#e74c3c', '#2ecc71']
bars = ax.bar(by_channel["channel"], by_channel["roas"], color=colors)
ax.set_title("ROAS by Channel", fontsize=14, fontweight='bold')
ax.set_ylabel("ROAS (x)")
ax.set_xlabel("Channel")

for bar, val in zip(bars, by_channel["roas"]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
            f'{val}x', ha='center', fontweight='bold')

buf = io.BytesIO()
plt.savefig(buf, format='png', bbox_inches='tight', dpi=150)
buf.seek(0)
chart_b64 = base64.b64encode(buf.read()).decode('utf-8')
plt.close()

# Build HTML report
template_str = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Marketing Report</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 40px; background: #f5f5f5; }
        h1 { color: #2c3e50; }
        .summary { display: flex; gap: 20px; margin-bottom: 30px; }
        .card { background: white; padding: 20px; border-radius: 8px; flex: 1; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .card h3 { margin: 0 0 8px 0; color: #7f8c8d; font-size: 14px; }
        .card p { margin: 0; font-size: 28px; font-weight: bold; color: #2c3e50; }
        table { width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        th { background: #2c3e50; color: white; padding: 12px; text-align: left; }
        td { padding: 12px; border-bottom: 1px solid #ecf0f1; }
        tr:hover { background: #f8f9fa; }
    </style>
</head>
<body>
    <h1>Marketing Performance Report</h1>
    <p>Generated: {{ date }}</p>

    <div class="summary">
        <div class="card">
            <h3>Total Spend</h3>
            <p>${{ total_spend }}</p>
        </div>
        <div class="card">
            <h3>Total Revenue</h3>
            <p>${{ total_revenue }}</p>
        </div>
        <div class="card">
            <h3>Overall ROAS</h3>
            <p>{{ total_roas }}x</p>
        </div>
    </div>

    <h2>ROAS by Channel</h2>
    <img src="data:image/png;base64,{{ chart_b64 }}" style="width:100%; max-width:700px; margin-bottom:30px;">

    <h2>Performance by Channel</h2>
    <table>
        <tr>
            <th>Channel</th>
            <th>Impressions</th>
            <th>Clicks</th>
            <th>CTR %</th>
            <th>Spend $</th>
            <th>Revenue $</th>
            <th>ROAS</th>
        </tr>
        {% for row in rows %}
        <tr>
            <td>{{ row.channel }}</td>
            <td>{{ row.impressions }}</td>
            <td>{{ row.clicks }}</td>
            <td>{{ row.ctr }}%</td>
            <td>${{ row.spend }}</td>
            <td>${{ row.revenue }}</td>
            <td>{{ row.roas }}x</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

template = Template(template_str)
html = template.render(
    date=datetime.now().strftime("%Y-%m-%d"),
    total_spend=total_spend,
    total_revenue=total_revenue,
    total_roas=total_roas,
    chart_b64=chart_b64,
    rows=by_channel.to_dict("records")
)

with open("report.html", "w") as f:
    f.write(html)

print("Done. Open report.html to view the report.")