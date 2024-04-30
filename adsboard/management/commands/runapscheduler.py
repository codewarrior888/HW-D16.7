import logging
import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings

from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from django.contrib.auth.models import User
from adsboard.models import Post

logger = logging.getLogger(__name__)


def my_job():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(post_time__gte=last_week)
    
    readable_posts = "\n".join(["{} - {}".format(p.post_time, p.title) for p in posts])
    readable_posts_html = "<br>".join(["{}-{}-{} {}:{} - {}".format(i.post_time.day, i.post_time.month, i.post_time.year, i.post_time.hour, i.post_time.minute, i.title) for i in posts])


    users_email_list = set(User.objects.all().values_list('email', flat=True))
    subject = f'Weekly new posts!'

    text_content = (
        f'New posts: {readable_posts}...\n\n'
        f'Read: {settings.SITE_URL}/posts/'
    )
    html_content = (
        f'<h3>Weekly new posts!</h3><br>'
        f'<i>{readable_posts_html}</i><br><br>'
        f'Visit <a href="{settings.SITE_URL}/posts/">Classified Ads Portal</a> for more posts!')

    msg = EmailMultiAlternatives(subject, text_content, None, users_email_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="mon", hour="08", minute="00"),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")