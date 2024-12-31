# Benchmarking of Time Series Databases for IoT Energy Data in Smart Buildings
The code aims to explore the performance of InfluxDB, TimescaleDB, MongoDB and PostgreSQL by accessing their capabilities in data ingestion, query execution, storage efficiency, and scalability. 



Databases Used
InfluxDB

Used for time-series data storage, leveraging buckets for optimized ingestion and querying.
Scripts include data ingestion, query performance, aggregation latency, and compression metrics.
Results generated using Python scripts with the InfluxDB client library.
PostgreSQL

Traditional relational database used to benchmark time-series performance in table-based structures.
Queries and ingestion operations executed using SQL scripts.
TimescaleDB

An extension of PostgreSQL designed for time-series data.
Utilized hypertables for partitioning and optimizing storage/querying.
Scripts include ingestion, compression, and aggregation metrics.
MongoDB

NoSQL database storing data in collections.
Queries written using JavaScript and executed in the Mongo shell.
Logs capture performance metrics like query latency and storage efficiency.
Key Scripts and Metrics
1. InfluxDB
Data Ingestion:
Simulates data ingestion into a bucket, measuring time, rate, and latency.
Query Performance:
Evaluates query latency and aggregation (e.g., average, min, max).
Compression and Storage:
Calculates raw size, compressed size, compression efficiency, and disk usage.
2. PostgreSQL
Table Ingestion:
SQL scripts create tables, load data, and measure ingestion rates/latency.
Query and Aggregation:
Executes queries to compute metrics and evaluate latency.
Indexing and Storage:
Index creation latency and overhead measured.
3. TimescaleDB
Hypertable Conversion:
Converts standard tables to hypertables for time-series optimization.
Compression:
Evaluates compression ratio and efficiency using chunk-level compression.
Performance Metrics:
Measures ingestion, query, and aggregation latencies.
4. MongoDB
Data Ingestion:
Uses mongoimport to ingest Steel.csv into a collection.
Query and Aggregation:
Measures query latency and aggregation metrics like average, min, and max.
Storage Metrics:
Logs disk usage, indexing overhead, and compression efficiency.



