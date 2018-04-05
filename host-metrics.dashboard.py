from grafanalib.core import *

dashboard = Dashboard(
  title = 'Host metrics',
  templating = Templating(
    list = [
      Template(
        default = 'None',
        name = 'node',
        regex = '/instance=\\\"(.*?)\\\"/',
        dataSource = 'Prometheus',
        query = 'node_boot_time',
        label = 'Host',
        includeAll = True,
        multi = True,
      ),
    ],
  ),
  rows = [
    Row(
      panels = [
        Graph(
          title = 'CPU',
          dataSource = 'Prometheus',
          span = 6,
          targets = [
            Target(
              expr = 'avg without (cpu)(irate(node_cpu{instance=~"$node",mode!="idle"}[5m]))',
              legendFormat = '{{instance}} {{mode}}',
              intervalFactor = 5,
              refId = 'A',
            ),
          ],
          legend = Legend(
            show = True,
            rightSide = True,
            alignAsTable = True,
          ),
          yAxes = [
            YAxis(format=PERCENT_UNIT_FORMAT),
            YAxis(format=OPS_FORMAT),
          ],
        ),
        Graph(
          title = 'Load average',
          dataSource = 'Prometheus',
          span = 6,
          targets = [
            Target(
              expr = 'node_load1{instance=~"$node"}',
              legendFormat = '{{instance}} 1min',
              intervalFactor = 10,
              refId = 'A',
            ),
            Target(
              expr = 'node_load5{instance=~"$node"}',
              legendFormat = '{{instance}} 5min',
              intervalFactor = 10,
              refId = 'B',
            ),
            Target(
              expr = 'node_load15{instance=~"$node"}',
              legendFormat = '{{instance}} 15min',
              intervalFactor = 10,
              refId = 'C',
            ),
          ],
        ),
      ],
    ),
    Row(
      panels = [
        Graph(
          title = 'Memory',
          dataSource = 'Prometheus',
          targets = [
            Target(
              expr = 'node_memory_MemTotal{instance=~"$node"} - node_memory_MemFree{instance=~"$node"} - node_memory_Buffers{instance=~"$node"} - node_memory_Cached{instance=~"$node"}',
              legendFormat = '{{instance}} Used',
              intervalFactor = 10,
              refId = 'A',
            ),
            Target(
              expr = 'node_memory_Buffers{instance=~"$node"}',
              legendFormat = '{{instance}} Buffers',
              intervalFactor = 10,
              refId = 'B',
            ),
            Target(
              expr = 'node_memory_Cached{instance=~"$node"}',
              legendFormat = '{{instance}} Cached',
              intervalFactor = 10,
              refId = 'C',
            ),
            Target(
              expr = 'node_memory_FreeMem{instance=~"$node"}',
              legendFormat = '{{instance}} Free',
              intervalFactor = 10,
              refId = 'D',
            ),
          ],
          yAxes = [
            YAxis(format=BYTES_FORMAT),
            YAxis(format=OPS_FORMAT),
          ],
        ),
      ],
    ),
    Row(
      panels = [
        Graph(
          title = 'Disk Space Available',
          dataSource = 'Prometheus',
          span = 6,
          targets = [
            Target(
              expr = 'node_filesystem_avail{device="/dev/sda1",mountpoint="/.r"}',
              legendFormat = '{{instance}}',
              refId = 'A',
            ),
          ],
          yAxes = [
            YAxis(format=BYTES_FORMAT),
            YAxis(format=OPS_FORMAT),
          ],
        ),
        Graph(
          title = 'Disk I/O',
          dataSource = 'Prometheus',
          span = 6,
          targets = [
            Target(
              expr = 'irate(node_disk_io_time_ms{instance=~"$node",device!~"^(sr\\\d+$)"}[5m]) / 1000',
              legendFormat = '{{instance}}',
              intervalFactor = 5,
              refId = 'A',
            ),
          ],
          yAxes = [
            YAxis(format=PERCENT_UNIT_FORMAT),
            YAxis(format=OPS_FORMAT),
          ],
        ),
      ],
    ),
    Row(
      panels = [
        SingleStat(
          title = 'Total Memory',
          dataSource = 'Prometheus',
          format = "bytes",
          span = 4,
          targets = [
            Target(
              expr = 'sum(node_memory_MemTotal{instance=~"$node"})',
              refId = 'A',
              format = '',
            ),
          ],
          sparkline = SparkLine(
            show = True,
          ),
        ),
        SingleStat(
          title = 'Total Memory Free',
          dataSource = 'Prometheus',
          format = "bytes",
          span = 4,
          targets = [
            Target(
              expr = 'sum(node_memory_MemFree{instance=~"$node"})',
              refId = 'A',
              format = '',
            ),
          ],
          sparkline = SparkLine(
            show = True,
          ),
        ),
        SingleStat(
          title = 'Total Memory Available',
          dataSource = 'Prometheus',
          format = "bytes",
          span = 4,
          targets = [
            Target(
              expr = 'sum(node_memory_MemAvailable{instance=~"$node"})',
              refId = 'A',
              format = '',
            ),
          ],
          sparkline = SparkLine(
            show = True,
          ),
        ),
      ],
    ),
  ],
).auto_panel_ids()
