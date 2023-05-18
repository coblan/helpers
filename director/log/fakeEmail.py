from django.core.mail.backends.base import BaseEmailBackend
from  django.utils.log import AdminEmailHandler
from concurrent_log_handler import ConcurrentRotatingFileHandler
from django.views.debug import ExceptionReporter


try:
    from html import unescape  # python 3.4+
except ImportError:
    try:
        from html.parser import HTMLParser  # python 3.x (<3.4)
    except ImportError:
        from HTMLParser import HTMLParser  # python 2.x
    unescape = HTMLParser().unescape
    

class MyEmailBackend(BaseEmailBackend):
    def send_messages(email_messages):
        print(email_messages)


class MyAdminEmailHandler(AdminEmailHandler):
    def send_mail(self, subject, message, *args, **kwargs):
        print(message)
    

def format_frames(frames):
    ls =[]
    
    for row in  reversed( frames ):
        vars_list  = row.get('vars')
        vars_str =''
        if row.get('type') =='django':
            continue
        for v in vars_list:
            value = unescape(v[1])
            vars_str += f'\t{v[0]}={value}\n'
        ls.append(str({
            'filename':row.get('filename'),
            'type':row.get('type'),
            'function':row.get('function'),
            'lineno':row.get('lineno'),
        }))
        ls.append(vars_str)
    return '\n'.join(ls)

class MyConcurrentLogHandler(ConcurrentRotatingFileHandler):
    def emit(self, record):
        """
        Emit a record.

        Override from parent class to handle file locking for the duration of rollover and write.
        This also does the formatting *before* locks are obtained, in case the format itself does
        logging calls from within. Rollover also occurs while the lock is held.
        """
        # noinspection PyBroadException
        try:
            msg = self.format(record)
            if record.levelname in ['ERROR','WARNING']:
                if record.exc_info:
                    exc_info = record.exc_info
                else:
                    exc_info = (None, record.getMessage(), None)   
                reporter = ExceptionReporter(None, is_email=False, *exc_info)
                frames =reporter.get_traceback_data().get('frames')     
                
                
                if frames:
                    
                    #ls  =[str(x) for x in frames]
                    frame_str = format_frames(frames)  #'\n'.join(ls)
                else:
                    frame_str = 'no frames'
                msg += '\n ======vars=======\n' + frame_str
            try:
                self._do_lock()

                try:
                    if self.shouldRollover(record):
                        self.doRollover()
                except Exception as e:
                    self._console_log("Unable to do rollover: %s" % (e,), stack=True)
                    # Continue on anyway

                self.do_write(msg)

            finally:
                self._do_unlock()
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)