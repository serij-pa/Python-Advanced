from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

@app.route('/division/<int:num_2>')
@metrics.counter(name="division_metriks", description='TEST_METRICS',
                 labels={'status': lambda r: r.status_code})
def test_endpoint(num_2):
    if num_2 == 0:
        raise ZeroDivisionError('Деление на ноль недопустимо!')
    result = 100 / num_2
    return b'Result ' + str(result).encode(), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)