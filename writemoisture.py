from influxdb import InfluxDBClient
from datetime import datetime
import time
import argparse

DBNAME = 'plant'


def get_moisture():
    return 1


def add_job_influx_db_metrics(client, tags_dict={}, values_dict={}, measurement='test'):
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    json_body = [
        {
            "measurement": measurement,
            "tags": tags_dict,
            "time": current_time,
            "fields": values_dict
        }
    ]

    client.write_points(points=json_body)


def main(host='localhost', port=8086):

    client = InfluxDBClient(host=host, port=port)
    client.switch_database(DBNAME)

    while True:
        # This line simply tells our script to wait 30 seconds, this is so the script doesnt hog all of the CPU
        add_job_influx_db_metrics(client, {}, {"moisture": get_moisture()}, 'moisture')
        time.sleep(30)


def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(
        description='Measures plant data and stores in InfluxDB')
    parser.add_argument('--host', type=str, required=False,
                        default='localhost',
                        help='hostname influxdb http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port influxdb http API')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(host=args.host, port=args.port)
