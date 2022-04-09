import time
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task
def long_task():
    logger.info('this is a long task')
    time.sleep(3600)
    logger.info('this is a long task')
