from influxdb_client import InfluxDBClient, QueryApi
import time
import os
import pandas as pd
import psutil  # To measure memory usage

# InfluxDB Setup
url = "http://localhost:8086"
token = "4tSl--LAXNsKMDo6mQOjjHnE1RBHGe0Px-oWA8FdGtF72xEdTyapqSokQYFouwWr64YE9DQ9u7KvtuLjX1nqRA=="
org = "sunway uni"
bucket = "Timeseries Performance"

# Initialize client
client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api()
query_api = client.query_api()

# Metrics storage
metrics = {
    "Ingestion Time (sec)": {},
    "Ingestion Rate (points/sec)": {},
    "Ingestion Latency (sec)": {},
    "Query Latency (sec)": {},
    "Aggregation Latency (sec)": {},
    "Memory Usage (MB)": {},
    "Compression Efficiency (%)": {},
    "Compression Ratio": {},
    "Raw Size (MB)": {},
    "Compressed Size (MB)": {},
    "Disk Usage (bytes)": {},
    "Indexing Overhead (bytes)": {},
    "Indexing Creation Latency (sec)": {},
}

# 1. Data Ingestion Performance (Simulation for Testing)
data = []
num_data_points = 35041  # Total number of points from the CSV file
average_point_size = 150  # Estimate of bytes per data point

# Simulate data ingestion
start_time = time.time()
for i in range(num_data_points):
    point = f"measurement,tag=example value={i} {int(time.time_ns())}"
    data.append(point)
time.sleep(1)  # Simulate network delay
end_time = time.time()

ingestion_time = end_time - start_time
ingestion_latency = ingestion_time / num_data_points

metrics["Ingestion Time (sec)"]["InfluxDB"] = ingestion_time
metrics["Ingestion Rate (points/sec)"]["InfluxDB"] = num_data_points / ingestion_time
metrics["Ingestion Latency (sec)"]["InfluxDB"] = ingestion_latency

# Simulate indexing creation latency
indexing_creation_latency = ingestion_time * 0.2  # Assume 20% of ingestion time
metrics["Indexing Creation Latency (sec)"]["InfluxDB"] = indexing_creation_latency

# Simulate indexing overhead
indexing_overhead = num_data_points * 10  # Assume 10 bytes per index entry
metrics["Indexing Overhead (bytes)"]["InfluxDB"] = indexing_overhead

# 2. Query Performance (Simulation for Testing)
start_time = time.time()
time.sleep(0.1)  # Simulated query execution time
end_time = time.time()
metrics["Query Latency (sec)"]["InfluxDB"] = end_time - start_time




# Simulate aggregation latency
start_time = time.time()

# Query to calculate the average of Usage_kWh
query_avg = '''
from(bucket: "Timeseries Performance")
  |> range(start: 0)
  |> filter(fn: (r) => r["_measurement"] == "timeseries")
  |> filter(fn: (r) => r["_field"] == "Usage_kWh")
  |> aggregateWindow(every: inf, fn: mean, createEmpty: false)
'''

# Query to calculate the minimum of Usage_kWh
query_min = '''
from(bucket: "Timeseries Performance")
  |> range(start: 0)
  |> filter(fn: (r) => r["_measurement"] == "timeseries")
  |> filter(fn: (r) => r["_field"] == "Usage_kWh")
  |> aggregateWindow(every: inf, fn: min, createEmpty: false)
'''

# Query to calculate the maximum of Usage_kWh
query_max = '''
from(bucket: "Timeseries Performance")
  |> range(start: 0)
  |> filter(fn: (r) => r["_measurement"] == "timeseries")
  |> filter(fn: (r) => r["_field"] == "Usage_kWh")
  |> aggregateWindow(every: inf, fn: max, createEmpty: false)
'''

# Execute the queries
result_avg = query_api.query(org=org, query=query_avg)
result_min = query_api.query(org=org, query=query_min)
result_max = query_api.query(org=org, query=query_max)

end_time = time.time()
metrics["Aggregation Latency (sec)"]["InfluxDB"] = end_time - start_time

# Initialize variables
avg_usage = None
min_usage = None
max_usage = None

# Extract and display average
if result_avg and len(result_avg) > 0:
    for table in result_avg:
        for record in table.records:
            avg_usage = record.get_value()

# Extract and display minimum
if result_min and len(result_min) > 0:
    for table in result_min:
        for record in table.records:
            min_usage = record.get_value()

# Extract and display maximum
if result_max and len(result_max) > 0:
    for table in result_max:
        for record in table.records:
            max_usage = record.get_value()

# Display results
if avg_usage is None or min_usage is None or max_usage is None:
    print("No data found for Usage_kWh")
else:
    print(f"InfluxDB Aggregation Latency: {metrics['Aggregation Latency (sec)']['InfluxDB']:.6f} seconds")
    print(f"Average Usage (kWh): {avg_usage}")
    print(f"Minimum Usage (kWh): {min_usage}")
    print(f"Maximum Usage (kWh): {max_usage}")





# 3. Calculate Raw Size from CSV (in MB)
data_file_path = "Steel_industry_data.csv"  # Path to the CSV file
try:
    raw_size_bytes = os.path.getsize(data_file_path)
    raw_size_mb = raw_size_bytes / (1024 * 1024)  # Convert to MB
    metrics["Raw Size (MB)"]["InfluxDB"] = raw_size_mb
    print(f"Raw Size (from CSV): {raw_size_mb:.2f} MB")
except Exception as e:
    print(f"Error reading file size: {e}")
    raw_size_bytes = 0

# 4. Simulated Compressed Size (for Testing) in MB
compressed_size_bytes = int(raw_size_bytes * 0.5)  # Assume 50% compression
compressed_size_mb = compressed_size_bytes / (1024 * 1024)  # Convert to MB
metrics["Compressed Size (MB)"]["InfluxDB"] = compressed_size_mb

# 5. Compression Metrics
if raw_size_mb > 0 and compressed_size_mb > 0:
    compression_efficiency = max((raw_size_mb - compressed_size_mb) / raw_size_mb * 100, 0)
    compression_ratio = raw_size_mb / compressed_size_mb
else:
    compression_efficiency = None
    compression_ratio = None

metrics["Compression Efficiency (%)"]["InfluxDB"] = compression_efficiency
metrics["Compression Ratio"]["InfluxDB"] = compression_ratio

print(f"Compression Efficiency: {compression_efficiency}%")
print(f"Compression Ratio: {compression_ratio}")

# 6. Disk Usage (Simulated in Bytes)
# Simulate disk usage based on compressed size for testing purposes
disk_usage_bytes = compressed_size_bytes * 1.2  # Assume 20% additional overhead for metadata
metrics["Disk Usage (bytes)"]["InfluxDB"] = disk_usage_bytes

print(f"Disk Usage: {disk_usage_bytes:.2f} bytes")

# 7. Memory Usage
try:
    memory_usage = psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)
    metrics["Memory Usage (MB)"]["InfluxDB"] = memory_usage
    print(f"Memory usage: {memory_usage:.2f} MB")
except Exception as e:
    print(f"Error calculating memory usage: {e}")

# Convert metrics to DataFrame
results = pd.DataFrame(metrics)

# Print results
print(results)

# Export results to CSV
results.to_csv("database_performance_metrics.csv", index=True)
print("Results saved to 'database_performance_metrics.csv'.")
