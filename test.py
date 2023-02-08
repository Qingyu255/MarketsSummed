# This File can be used to delete all plotly grids.
import json
from charts import Charts

charts = Charts()

charts.permanently_delete_files("qy25555", filetype_to_delete='plot')
charts.permanently_delete_files("qy25555", filetype_to_delete='grid')

