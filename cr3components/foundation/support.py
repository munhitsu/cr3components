from django.core.mail import mail_admins
from django.conf import settings
import traceback

def send_error(exec_info):
    subject = 'Error on %s site.' % (settings.PROJECT,)
    (type, error_message, stacktrace,) = exec_info
    m = traceback.format_exception(type, error_message, stacktrace)
    message = ''
    for l in m:
        message += l
    print 'message',message
    mail_admins(subject, message, True)
    
def send_message(message):
    subject = 'Message from %s site.' % (settings.PROJECT,)
    mail_admins(subject, message, True)
