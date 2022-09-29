from django.conf import settings
import inspect
import logging
import sys


class ClassFilter(logging.Filter):
    def _get_class_from_frame(self,fr):
        args, _, _, value_dict = inspect.getargvalues(fr)
        # we check the first parameter for the frame function is
        instance = None
        if len(args) and args[0] == 'self':
            # in that case, 'self' will be referenced in value_dict
            instance = value_dict.get('self', None)
        if instance:
            # return its class
            return getattr(instance, '__class__', None)

        return None

    def filter(self, record):
        stack = inspect.stack()
        # the classes that directly called filter are not needed!
        unwanted_classes = ['Logger','ClassFilter']
        for stack_frame in stack:
            class_obj = self._get_class_from_frame(stack_frame[0])

            if class_obj and class_obj.__name__ not in unwanted_classes:
                if class_obj:
                    classname = class_obj.__name__
                else:
                    classname = 'None'
                break

        record.classname = classname
        return True


logger = logging.getLogger("trustid_logger")
logger.setLevel(logging.DEBUG)
logger.addFilter(ClassFilter())

# create file handler which logs even debug messages
fh = logging.FileHandler(settings.LOGGER_PATH)
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
formatter = logging.Formatter('%(levelname)s - %(classname)s - %(funcName)s - %(asctime)s - %(message)s')
fh.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.DEBUG)
sh.setFormatter(formatter)
logger.addHandler(sh)
