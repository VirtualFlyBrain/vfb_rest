FROM python:3.5.2

ENV KBserver=http://192.168.0.1:7474
ENV KBuser=neo4j
ENV KBpassword=password
ENV DjangoUser=admin
ENV DjangoPassword=admin

RUN mkdir /code
ADD requirements.txt /code
RUN pip install -r /code/requirements.txt
ADD . /code
WORKDIR /code/vfb_rest

RUN echo -e "travis_fold:start:processLoad" && \
cd "/code" && \
echo '** Git checkout VFB_neo4j **' && \
git clone --quiet https://github.com/VirtualFlyBrain/VFB_neo4j.git

RUN cd "/code" && \
echo -e "travis_fold:end:processLoad"

RUN mkdir /code/vfb_rest/vfb_rest/vfb
RUN mv /code/VFB_neo4j/src/* /code/vfb_rest/vfb_rest/vfb

RUN ls -l /code/vfb_rest/vfb_rest/vfb
RUN pip install django-rest-swagger

ENTRYPOINT bash -c "python manage.py migrate --noinput && \
python manage.py runserver 0.0.0.0:8000"
#&& python manage.py loaddata users
