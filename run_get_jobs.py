# /usr/bin/env python
import json, requests, time, sys, argparse
from config import Config
import logging



def run_job(spider, item):
    params = {
        'project': Config.PROJECT,
        'spider': Config.spiders[spider][item]
    }
    logging.info('Run job ' + Config.spiders[spider][item])
    requests.post(Config.URL_RUN_JOB, data=params, auth=(Config.API, ''))



def get_job_id(spider, item):
    params = {
        'project': Config.PROJECT,
        'spider': Config.spiders[spider][item],
        'state': 'finished'
    }
    jobs = []
    #run_job(spider, item)
    #time.sleep(3600)
    response = requests.get(Config.URL_LIST_JOBS, params=params, auth=(Config.API, ''))
    jobs_data = json.loads(response.text)['jobs']
    for item_data in jobs_data:
        if item_data['close_reason'] == 'finished':
            jobs.append(item_data)

    project_id = jobs[0]['id']
    logging.info('Project ID ' + project_id)
    return project_id

def get_elems(spider,item):
    params = {
        'format': 'json'
    }
    jobid = get_job_id(spider, item)
    response = requests.get(Config.URL_GET_ELEM + jobid, params=params, auth=(Config.API, ''))
    elems = json.loads(response.text)
    # logging.info('In job id ' + jobid + 'containt a ' + len(elems) + 'elements')
    logging.info('In job id %s containt a %s elements' % (jobid, len(elems)))
    return elems
def collect_jsons(spider):
    results = []
    for item in Config.spiders[spider]:

        results.extend(get_elems(spider, item))
    logging.info('collect json done, result containt a %s elements' % (len(results)))
    return results