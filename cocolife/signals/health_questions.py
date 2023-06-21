from django.db.models.signals import pre_save

from cocolife.models.CLHealthQuestionsAnswers import CLHealthQuestionsAnswers

from api.tasks.email import (
    notify_agent_of_failed_health_declaration,
    notify_insuree_of_failed_health_declaration
)


def pre_save_health_question_answer_handler(sender, instance, **kwargs):
    try:
        previous_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    has_failed = previous_instance.answer_status != 'fail' and instance.answer_status == 'fail'
    if has_failed:
        insuree = instance.ProdInsuree
        user = insuree.billed_to
        product = insuree.product
        application_datetime_str = product.created_at.strftime('%B %d, %Y at %I:%M:%S %p')

        agent_task_kwargs = {
            'reference_id': 'NQ{}'.format(user.pk),
            'product_name': product.name,
            'application_datetime_str': application_datetime_str,
            'application_number': product.application_number,
            'full_name': '{} {} {}'.format(user.first_name, user.middle_name, user.last_name),
            'mobile': user.mobie_number,
            'email': user.email,
        }
        notify_agent_of_failed_health_declaration.apply_async(kwargs=agent_task_kwargs)


def register_handlers():
    pre_save.connect(
        pre_save_health_question_answer_handler,
        sender=CLHealthQuestionsAnswers,
        dispatch_uid='pre_save_health_question_answer_handler'
    )
