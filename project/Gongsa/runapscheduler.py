import logging
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Post
from aici.models import VOC
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from apscheduler.triggers.cron import CronTrigger

logger = logging.getLogger(__name__)

def delete_completed_constructions():
    thirty_days_after_end = datetime.now().date() - timedelta(days=30)
    constructions_to_delete = Post.objects.filter(end_at__lte=thirty_days_after_end)
    constructions_to_delete.delete()

def delete_confirmed_voc():
    one_day_ago = timezone.now() - timedelta(days=1)
    confirmed_voc = VOC.objects.filter(voc_status='확인완료', updated_at__lte=one_day_ago)
    confirmed_voc.delete()

def start():
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)

    scheduler.add_job(
        delete_completed_constructions,
        trigger=CronTrigger(second="*/30"),
        id="my_job",
        max_instances=1,
        replace_existing=True,
    )
    logger.info("Added job 'delete_completed_constructions'.")

    scheduler.add_job(
        delete_confirmed_voc,
        trigger=CronTrigger(second="*/30"),
        id="my_job_b",
        max_instances=1,
        replace_existing=True,
    )
    logger.info("Added job 'delete_confirmed_voc'.")

    try:
        logger.info("Starting scheduler...")
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Stopping scheduler...")
        scheduler.shutdown()
        logger.info("Scheduler shut down successfully!")
