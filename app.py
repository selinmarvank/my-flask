import os
from flask import Flask

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

    # Replace with your table
    query = """
        SELECT AgeGroup, TotalCustomers, TotalRevenue,Gender
        FROM `acoustic-apex-469415-m0.DAG.age_summary_gender`
        LIMIT 10
    """
    query_job = client.query(query)
    results = query_job.result()

    # Convert to list of dicts
    rows = [dict(row) for row in results]

    # Simple HTML template
    template = """
    <h1>BigQuery Results</h1>
    <table border="1" cellpadding="5">
        <tr>
            {% for col in rows[0].keys() %}
                <th>{{ col }}</th>
            {% endfor %}
        </tr>
        {% for row in rows %}
            <tr>
                {% for val in row.values() %}
                    <td>{{ val }}</td>
                {% endfor %}
            </tr>
        {% endfor %}
    </table>
    """
    return render_template_string(template, rows=rows)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
