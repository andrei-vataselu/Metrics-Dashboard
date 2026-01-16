# QuickSight Dashboard Guide

This directory contains examples and documentation for creating Amazon QuickSight dashboards from the metrics data collected by Roxxane. The data stored in S3 provides rich system metrics that can be visualized and analyzed to gain insights into system performance, resource utilization, and operational patterns.

## Data Schema

The metrics data includes the following fields:

**Core Metrics:**
- `cpu_pct` - CPU usage percentage
- `ram_pct` - RAM usage percentage
- `interval_s` - Collection interval in seconds

**Network Metrics:**
- `net_bytes_sent_per_s` - Network bytes sent per second
- `net_bytes_recv_per_s` - Network bytes received per second
- `net_packets_sent_per_s` - Network packets sent per second
- `net_packets_recv_per_s` - Network packets received per second
- `net_err_in_per_s` - Network input errors per second
- `net_err_out_per_s` - Network output errors per second
- `net_drop_in_per_s` - Network input drops per second
- `net_drop_out_per_s` - Network output drops per second

**Disk Metrics:**
- `disk_read_bytes_per_s` - Disk read bytes per second
- `disk_write_bytes_per_s` - Disk write bytes per second
- `disk_read_ops_per_s` - Disk read operations per second
- `disk_write_ops_per_s` - Disk write operations per second

**System Information:**
- `hostname` - Hostname of the system
- `os` - Operating system name
- `os_v` - Operating system version
- `arch` - System architecture
- `node_role` - Node role identifier
- `env` - Environment identifier
- `session_id` - Session identifier

**Time Fields:**
- `ts` - Unix timestamp
- `timestamp` - Formatted timestamp string
- `date` - Date string (YYYY-MM-DD)
- `hour` - Hour (00-23)
- `minute` - Minute (00-59)
- `day_of_week` - Day of week name
- `year`, `month`, `day` - Partition keys

## Dashboard Types

### Performance Monitoring Dashboard

Monitor system resource utilization over time with key performance indicators.

**Visualizations:**
- Line chart: CPU usage percentage over time (grouped by hostname)
- Line chart: RAM usage percentage over time (grouped by hostname)
- Gauge chart: Current CPU and RAM usage averages
- Heat map: CPU usage by hour of day and day of week
- Table: Top 10 hosts by average CPU usage

**Use Cases:**
- Identify resource-intensive periods
- Detect capacity planning needs
- Monitor resource trends over time
- Compare performance across different hosts

### Network Analysis Dashboard

Analyze network throughput, errors, and packet statistics to identify network issues and bottlenecks.

**Visualizations:**
- Line chart: Network bytes sent/received per second over time
- Bar chart: Network errors and drops by hostname
- Scatter plot: Network throughput vs errors (identify problematic hosts)
- Area chart: Network packet rates over time
- Table: Hosts with highest error rates

**Use Cases:**
- Identify network congestion periods
- Detect hosts with network issues
- Monitor network capacity utilization
- Analyze error patterns and trends

### Disk I/O Dashboard

Monitor disk read/write operations and throughput to understand storage performance.

**Visualizations:**
- Line chart: Disk read/write bytes per second over time
- Bar chart: Disk operations per second by hostname
- Scatter plot: Disk I/O vs CPU usage (identify I/O-bound systems)
- Heat map: Disk activity by hour of day
- Table: Hosts with highest disk I/O rates

**Use Cases:**
- Identify I/O-intensive workloads
- Detect storage bottlenecks
- Monitor disk performance trends
- Compare I/O patterns across hosts

### Host Comparison Dashboard

Compare metrics across different hosts to identify outliers and performance differences.

**Visualizations:**
- Box plot: CPU usage distribution by hostname
- Box plot: RAM usage distribution by hostname
- Bar chart: Average metrics by hostname (side-by-side comparison)
- Scatter plot: CPU vs RAM usage by hostname
- Table: Summary statistics by hostname

**Use Cases:**
- Identify underperforming or overperforming hosts
- Compare system configurations
- Detect hardware issues
- Plan resource allocation

### Time-Based Pattern Analysis

Identify patterns in system behavior based on time of day, day of week, or date.

**Visualizations:**
- Heat map: CPU usage by hour and day of week
- Line chart: Average metrics by hour of day
- Bar chart: Average metrics by day of week
- Line chart: Daily trends over time
- Table: Peak usage times by metric type

**Use Cases:**
- Understand usage patterns
- Plan maintenance windows
- Identify seasonal trends
- Optimize resource scheduling

### Environment Comparison Dashboard

Compare metrics across different environments (dev, staging, production) to understand environment-specific behavior.

**Visualizations:**
- Bar chart: Average CPU/RAM by environment
- Line chart: Metrics over time grouped by environment
- Scatter plot: Environment comparison (CPU vs RAM)
- Table: Summary statistics by environment

**Use Cases:**
- Compare environment performance
- Validate environment parity
- Identify environment-specific issues
- Plan capacity across environments

### Anomaly Detection Dashboard

Identify unusual patterns, spikes, or outliers in system metrics.

**Visualizations:**
- Line chart: Metrics with anomaly detection overlay
- Scatter plot: Outlier detection (CPU vs RAM)
- Table: Anomalous events with timestamps
- Bar chart: Anomaly frequency by hostname
- Heat map: Anomaly patterns by time

**Use Cases:**
- Detect system issues early
- Identify security incidents
- Monitor for unusual activity
- Track system health

## Data Relationships

### Resource Correlation

**CPU vs RAM Usage**
Analyze the relationship between CPU and memory utilization. Systems with high CPU but low RAM may be CPU-bound, while high RAM with low CPU may indicate memory-intensive workloads.

**Network Throughput vs Errors**
Correlate network throughput with error rates. High throughput with high errors may indicate network congestion or hardware issues.

**Disk I/O vs System Load**
Compare disk I/O rates with CPU usage to identify I/O-bound systems. High disk activity with low CPU suggests storage bottlenecks.

### Time-Based Relationships

**Hourly Patterns**
Identify peak usage hours and correlate with business operations. Understanding hourly patterns helps with capacity planning and resource scheduling.

**Day of Week Patterns**
Analyze weekly patterns to identify recurring high-load days. This helps plan maintenance windows and resource allocation.

**Seasonal Trends**
Track long-term trends to identify growth patterns, seasonal variations, and capacity planning needs.

### Host Relationships

**Host Performance Comparison**
Compare similar hosts to identify configuration differences, hardware issues, or workload distribution problems.

**Host Clustering**
Group hosts by similar performance characteristics to identify patterns and optimize resource allocation.

### Environment Relationships

**Environment Parity**
Compare metrics across environments to ensure dev/staging accurately reflects production behavior.

**Environment-Specific Patterns**
Identify environment-specific usage patterns that may indicate configuration differences or workload variations.

## QuickSight Setup

1. **Create Data Source**
   - Connect to your S3 bucket using AWS Glue as the data catalog
   - Select the Glue database and table created by the crawler
   - Use SPICE for better performance with large datasets

2. **Import Data**
   - Choose the partitioned table from Glue
   - QuickSight will automatically recognize the partition structure
   - Set up incremental refresh if needed

3. **Create Calculated Fields**
   - Network total throughput: `net_bytes_sent_per_s + net_bytes_recv_per_s`
   - Disk total I/O: `disk_read_bytes_per_s + disk_write_bytes_per_s`
   - CPU load category: `IF(cpu_pct > 80, "High", IF(cpu_pct > 50, "Medium", "Low"))`
   - RAM load category: Similar calculation for RAM

4. **Build Visualizations**
   - Start with the Performance Monitoring dashboard as a foundation
   - Add filters for hostname, environment, and time ranges
   - Use parameters for dynamic filtering

5. **Set Up Alerts**
   - Configure alerts for CPU > 90%
   - Configure alerts for RAM > 95%
   - Configure alerts for network errors > threshold

## Best Practices

- Use SPICE for frequently accessed data to improve performance
- Set up scheduled refreshes to keep data current
- Use parameters for flexible filtering across visualizations
- Create calculated fields for common metrics combinations
- Use consistent color schemes across related dashboards
- Add tooltips with additional context for metrics
- Include data quality indicators (record counts, last update time)
- Use appropriate chart types for different metric types (line for time series, bar for comparisons)

## Example Queries

**Peak CPU Usage by Hour:**
```
SELECT hour, AVG(cpu_pct) as avg_cpu
FROM metrics_table
GROUP BY hour
ORDER BY avg_cpu DESC
```

**Hosts with Network Errors:**
```
SELECT hostname, SUM(net_err_in_per_s + net_err_out_per_s) as total_errors
FROM metrics_table
WHERE net_err_in_per_s > 0 OR net_err_out_per_s > 0
GROUP BY hostname
ORDER BY total_errors DESC
```

**CPU vs RAM Correlation:**
```
SELECT hostname, AVG(cpu_pct) as avg_cpu, AVG(ram_pct) as avg_ram
FROM metrics_table
GROUP BY hostname
```

## Files in This Directory

- `README.md` - This documentation file
- `General_Reports_2026-01-16T14_46_11.pdf` - Example QuickSight dashboard export
- `image.png` - Dashboard screenshot example
- `image2.png` - Additional dashboard visualization example

Use these examples as reference when building your own dashboards. The PDF contains a complete dashboard export that can be imported into QuickSight, while the images show example visualizations you can recreate.
