import os
from flask import Flask,render_template_string
from google.cloud import bigquery
import json

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, Cloud Run!"


@app.route('/api/test')
def test():
    return {"name":"selin"}

@app.route("/api/analysis")
def index():
    client = bigquery.Client()

    query = """
        SELECT AgeGroup, TotalCustomers, TotalRevenue, Gender
        FROM `acoustic-apex-469415-m0.DAG.age_summary_gender`
        LIMIT 10
    """
    query_job = client.query(query)
    results = query_job.result()

    rows = [dict(row) for row in results]

    # Prepare JSON data for JS
    chart_data = {
        "labels": [row["AgeGroup"] for row in rows],
        "customers": [row["TotalCustomers"] for row in rows],
        "revenue": [row["TotalRevenue"] for row in rows],
        "gender": [row["Gender"] for row in rows],
    }

    template = """
    <html>
    <head>
        <title>BigQuery Chart</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body>
        <h1>BigQuery Analysis</h1>
        <canvas id="myChart" width="600" height="400"></canvas>

        <script>
            const data = {{ chart_data | safe }};

            const ctx = document.getElementById('myChart').getContext('2d');
            const myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [
                        {
                            label: 'Total Customers',
                            data: data.customers,
                            backgroundColor: 'rgba(54, 162, 235, 0.6)',
                        },
                        {
                            label: 'Total Revenue',
                            data: data.revenue,
                            backgroundColor: 'rgba(255, 99, 132, 0.6)',
                        }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: {
                        tooltip: {
                            callbacks: {
                                afterBody: (tooltipItems) => {
                                    const idx = tooltipItems[0].dataIndex;
                                    return "Gender: " + data.gender[idx];
                                }
                            }
                        }
                    },
                    scales: {
                        x: { title: { display: true, text: 'Age Group' } },
                        y: { title: { display: true, text: 'Values' } }
                    }
                }
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(template, chart_data=json.dumps(chart_data))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
