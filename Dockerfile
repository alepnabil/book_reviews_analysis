#pull ubuntu image

FROM python:3.7-slim
FROM apache/airflow:2.2.0


USER root
COPY requirements.txt /requirements.txt


RUN apt-get -y update
RUN apt-get install --assume-yes git





#add chromedriver to PATH
ENV PATH "$PATH:/usr/local/bin/"



USER ${AIRFLOW_UID}
RUN pip install --user --upgrade pip
RUN git clone https://github.com/allenai/longformer.git
RUN pip install --no-cache-dir --user -r /requirements.txt



#make folder to store temp data
RUN bash -c 'mkdir -p raw_data/{english,malay}'
RUN bash -c 'mkdir -p clean_data/{english,malay}'


ENV AIRFLOW__CORE__DAGBAG_IMPORT_TIMEOUT=300



