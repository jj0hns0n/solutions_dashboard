import os
from datetime import datetime, timedelta
from harvest import Harvest, HarvestError
from spreadsheets_util import *

h = Harvest( os.environ['HARVEST_URL'], os.environ['HARVEST_EMAIL'], os.environ['HARVEST_PASSWORD'] )

end = datetime.today()
start = end - timedelta(720) # 2 Years in the past

gd_client = gdata.spreadsheet.service.SpreadsheetsService()
gd_client.email = os.environ['GDOCS_EMAIL']
gd_client.password = os.environ['GDOCS_PASSWORD']
gd_client.source = 'opengeo-solutions_dashboard-1'
gd_client.ProgrammaticLogin()
#gd_client.debug = True

key = '0AgQ7XY0Atfx5dERpQ2VDcEtGUVpOQVRvVng4Tm1DMGc'
worksheet = 'od6'

def update_project(row, name, client, total, billable, non_billable):
    CellsUpdateAction(gd_client, key, worksheet, row, 1, name)
    CellsUpdateAction(gd_client, key, worksheet, row, 2, client)
    CellsUpdateAction(gd_client, key, worksheet, row, 3, str(total))
    CellsUpdateAction(gd_client, key, worksheet, row, 4, str(billable))
    CellsUpdateAction(gd_client, key, worksheet, row, 5, str(non_billable))

project_count = 1
for project in h.projects():
    total = 0
    tasks = {}
    billable = 0
    non_billable = 0
    for assignment in project.task_assignments:
        task_dict = {}
        name = assignment.task.name
        task_dict['name'] = name
        task_dict['billable'] = assignment.billable
        task_dict['hours'] = 0
        task_dict['budget'] = assignment.budget
        tasks[name] = task_dict
    for entry in project.entries(start, end):
        task = tasks[entry.task.name]
        total += entry.hours
        task['hours'] = task['hours'] + entry.hours
        if tasks[entry.task.name]['billable']:
            billable += entry.hours
        else:
            non_billable += entry.hours
    print "%s,%s,%02f, %02f, %02f" % (project.name, str(project.client.name), total, billable, non_billable)
    for k,v in tasks.iteritems():
        print k, v['hours'], v['budget']
    
    update_project(project_count+1, project.name, str(project.client.name), total, billable, non_billable)
    project_count += 1
