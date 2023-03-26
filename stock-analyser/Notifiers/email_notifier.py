from logger import logger
import smtplib
from Notifiers.utils import NotifyUtils
from tenacity import retry,  stop_after_attempt

class EmailNotifier(NotifyUtils):
    '''
    Notify by email
    '''
    def __init__(self,email_conf):
        self.conf= email_conf

    def notify(self,content):
        #convert content to message
        message=self.content_to_message(content)
        if len(message) > 0:
            for email in self.conf.values():
                if email['enable'] and len(email["destination_emails"])>0:
                    for d in email["destination_emails"]:
                        self._send_message(email['server'],email['username'],email['password'],d,message)

    @retry(stop=stop_after_attempt(3))
    def _send_message(self,smtp_server,username,password,dest_emails,message):
        try:
            header = 'From: %s\n' % username
            header += 'To: %s\n' % dest_emails
            header += 'Content-Type: text/plain\n'
            header += 'Subject: signal alert!\n\n'
            message = header + message

            smtp_handler = smtplib.SMTP(smtp_server)
            smtp_handler.starttls()
            smtp_handler.login(username, password)
            result = smtp_handler.sendmail(username, dest_emails, message)
            smtp_handler.quit()
            return result
            logger.outputlog("send message from %s to %s"%(smtp_server,dest_emails))
        except Exception as e:
            logger.outputlog(e)

