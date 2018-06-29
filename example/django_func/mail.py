from django.core.mail import send_mail #导入django发送邮件模块
send_mail('subject', 'message', '******@163.com', ['******@qq.com'],fail_silently=False)