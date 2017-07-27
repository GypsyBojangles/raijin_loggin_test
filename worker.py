import datetime
import logging
import logging.handlers
import os
import socket
import sys
import time
import json
from random import randint

listener_hostname = sys.argv[1]
gridx = randint(0, 100)
gridy = randint(0, 100)
application = 'logging_test'
hostname = socket.gethostname()
job_id = os.getenv('PBS_JOBID', 'n/a')
job_name = os.getenv('PBS_JOBNAME', 'n/a')
submitted_queue = os.getenv('PBS_O_QUEUE', 'n/a')
run_queue = os.getenv('PBS_QUEUE', 'n/a')

rootLogger = logging.getLogger('')
rootLogger.setLevel(logging.INFO)
socketHandler = logging.handlers.SocketHandler(listener_hostname,
                                               logging.handlers.DEFAULT_TCP_LOGGING_PORT)
rootLogger.addHandler(socketHandler)


def log_dataset_event(dataset_event, dataset_location):
    ts = time.time()
    event_dict = {
        'dataset_event': dataset_event,
        'application': application,
        'worker': hostname,
        'job_id': job_id,
        'job_name': job_name,
        'submitted_queue': submitted_queue,
        'run_queue': run_queue,
        'head': listener_hostname,
        'properties': {
            'gridx': gridx,
            'gridy': gridy
        },
        'dataset_location': dataset_location if dataset_location else 'n/a',
        'reported_time': datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    }

    logging.info(json.dumps(event_dict))


def worker_app():
    log_dataset_event('dataset processing started', None)

    # generate some lag to make the events more interesting
    randomwait = randint(5, 30)
    time.sleep(randomwait)

    randomevent = randint(0, 30)

    dataset_location = '/some/random/path/' + application + str(gridx) + str(gridy)

    if randomevent == 0:
        log_dataset_event('could not connect to database', None)

    elif randomevent == 1:
        log_dataset_event('error reading data', None)

    elif randomevent == 2:
        log_dataset_event('error with application', None)

    elif randomevent == 3:
        log_dataset_event('error writing to file', dataset_location)

    elif randomevent == 4:
        log_dataset_event('dataset validation failed', dataset_location)

    elif randomevent == 5:
        log_dataset_event('dataset cleanup failed', dataset_location)

    elif randomevent == 6:
        log_dataset_event('dataset indexing failed', dataset_location)

    else:
        log_dataset_event('dataset indexed', dataset_location)


if __name__ == "__main__":
    worker_app()
