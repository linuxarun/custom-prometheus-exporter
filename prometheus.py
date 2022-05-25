import os,stat
from time import sleep

service = service = os.uname()[1]

def main():
    gather_metrics()

metrics_data_map = {}

metrics_file = "/root/prometheus/data/metrics_data"
log_file = "/var/log/application_metrics.log"

def prometheus():
    f = open(metrics_file,"r")
    data = f.read()
    return data

def areEqual(arr1, arr2, n, m):
    if (n != m):
        return False

    arr1.sort()
    arr2.sort()
    for i in range(0, n):
        if (arr1[i] != arr2[i]):
            return False
    return True


def create_metrics_data(metric, keys, time_taken):   
    if metric not in  metrics_data_map:
        metrics_data_map[metric] = []
        metrics_data_map[metric].append([keys, 1.0, time_taken])
        return

    found = False
    for item in metrics_data_map[metric]:
        if areEqual(item[0], keys, len(item[0]), len(keys)) == True:
            item[1] += 1
            if time_taken is not None:
                if item[2] is None:
                    item[2] = 0.0
                item[2] += time_taken
            found = True
            break
    if found == False:
        metrics_data_map[metric].append([keys, 1.0, time_taken])


def write_metrics():
    metric_str = ""
    for metric,data in metrics_data_map.items():
        if data is None or len(data) == 0:
            continue
        for data_value in data:
            if data_value is None or len(data_value[0]) == 0:
                continue
            metric_str += metric + "_count" + "{" + "app_service=" + "\"" + service + "\"" + ","
            for item in data_value[0]:
                metric_str += item.split('=')[0] + "=" + "\"" + item.split('=')[1] + "\"" + ","
            metric_str += "} " + str(data_value[1]) + "\n"

            if data_value[2] is not None:
                metric_str += metric + "_sum" + "{" + "app_service=" + "\"" + service + "\"" + ","
                for item in data_value[0]:
                    metric_str += item.split('=')[0] + "=" + "\"" + item.split('=')[1] + "\"" + ","
                metric_str += "} " + str(data_value[2]) + "\n"
    f = open(metrics_file,"w")
    f.write(metric_str)
    f.close()

def gather_metrics():
    for line in tail_log_file():
        try:
            data = line.split(';')
            metrics_map = {}
            for data_item in data:
                if data_item is None or data_item == "":
                    continue
                pair = data_item.split('=')
                if len(pair) != 2:
                    continue
                metrics_map[pair[0]] = pair[1]
            try:
                metric = metrics_map.pop('metric')
            except Exception as e:
                metric = "custom_metric"
    
            try:
                time_taken = float(metrics_map.pop('time_taken'))
            except Exception as e:
                time_taken = None

            labels_data = []
            for key,value in metrics_map.items():
                if key is None or key == "":
                    continue
                if value is None or value == "":
                    value = "None"
                labels_data.append(key + "=" + value)

            create_metrics_data(metric, labels_data, time_taken)
            write_metrics()

        except Exception as e:
            print(line + ". Exception: " + str(e))


def tail_log_file():
    if not os.path.exists(log_file):
        open(log_file, 'w').close()
        os.chmod(log_file, 0o777)
    current = open(log_file, "r")
    curino = os.fstat(current.fileno()).st_ino
    current.seek(0, os.SEEK_END)
    while True:
        line = current.readline()
        if not line:
            sleep(0.1)
            try:
                if oct(os.stat(log_file).st_mode)[-3:] != '777':
                    os.chmod(log_file, 0o777)
                if os.stat(log_file).st_ino != curino:
                    new = open(log_file, "r")
                    current.close()
                    current = new
                    curino = os.fstat(current.fileno()).st_ino
                    continue
            except IOError:
                if not os.path.exists(log_file):
                    open(log_file, 'w').close()
                    os.chmod(log_file, 0o777)
                    current = open(log_file, "r")
                    curino = os.fstat(current.fileno()).st_ino
                pass
        else:
            line.replace('\n','')
            line.replace('\r\n','')
            yield line

if __name__ == "__main__":
    main()
