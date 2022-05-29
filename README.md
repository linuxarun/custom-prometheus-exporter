# custom-prometheus-exporter
1. Run both the files prometheus_server.py and prometheus.py as service.
2. Provide logs in the log_file specified in prometheus.py in format -> metric=my_custom_metric;label_1=mylabel_1;label_2=my_label_2;
3. Additionally, time taken by any metric can be provided in the log above -> metric=my_custom_metric;label_1=mylabel_1;label_2=my_label_2;time_taken=2;
4. You can check the metrics on the port and path specified in app.py
