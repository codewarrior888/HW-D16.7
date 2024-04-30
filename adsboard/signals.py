from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from classifiedads.settings import SERVER_EMAIL

from .models import Comment, Post


@receiver(post_save, sender=Comment)
def comment_notify(sender, instance, **kwargs):
    print('comment_notify', instance)
    author = instance.author.username
    content = instance.content
    post_pk = instance.post.pk
    post_author = instance.post.author

    if instance.status:
        mail = instance.post.author.email
        subject = f'Your comment has been approved by {post_author}'
        text_content2 = (
            f'Hello, {author}! \n\n'
            f'Your comment "{content}" is accepted by {post_author}. \n'
            f'Read: http://127.0.0.1:8000/post/{post_pk}'
        )

        send_mail(
            subject=subject,
            message=text_content2,
            from_email=f'{SERVER_EMAIL}',
            recipient_list=[mail],
            fail_silently=False
        )
    else:
        mail = instance.post.author.email
        subject = f'A comment from {author} is waiting for your approval!'
        text_content = (
            'A comment to your post!'
            'Accept or reject: http://127.0.0.1:8000/usercomments/'
        )

        mail2 = instance.author.email
        subject2 = f'Your comment "{content}" was sent for approval'
        text_content2 = (
            '''Your comment "{content}" hasn't been approved yet. '''
            'We will notify you once it is approved and published'
        )

        send_mail(
            subject=subject,
            message=text_content,
            from_email=f'{SERVER_EMAIL}',
            recipient_list=[mail],
            fail_silently=False
        )

        send_mail(
            subject=subject2,
            message=text_content2,
            from_email=f'{SERVER_EMAIL}',
            recipient_list=[mail2],
            fail_silently=False
        )


@receiver(post_save, sender=Post)
def post_notify(sender, instance, **kwargs):
    author = instance.author
    title = instance.title
    mail = instance.author.email
    post_pk = instance.pk
    subject = f'Hello {author}! Your post was successfully published'
    text_content = (
        f'Hi, {author}! \n'
        f'Your post "{title}" was successfully published or changed. \n'
        f'Read: http://127.0.0.1:8000/posts/{post_pk}'
    )

    send_mail(
        subject=subject,
        message=text_content,
        from_email=f'{SERVER_EMAIL}',
        recipient_list=[mail],
        fail_silently=False
    )
