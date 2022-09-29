FROM python:3.6
RUN apt-get update && apt-get install -y libgettextpo-dev cmake
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN touch /code/creams_project.log
RUN chown -R :www-data /code
RUN groupadd varwwwusers
RUN adduser www-data varwwwusers
RUN chgrp -R varwwwusers /code/creams_project.log
RUN chmod 775 /code/creams_project.log
RUN apt-get install -y libpq-dev
RUN pip install --upgrade pip
RUN pip install --trusted-host pypy.org --trusted-host files.pythonhosted.org -r requirements.txt
