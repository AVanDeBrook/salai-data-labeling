FROM ubuntu:23.10
SHELL [ "/bin/bash", "-c" ]
EXPOSE 8080

# image config
RUN apt-get -yq update && apt-get -yq upgrade
RUN apt-get -yq install python3 python3-pip pipx
RUN pipx install label-studio
RUN pipx runpip label-studio install -U --upgrade-strategy=eager django==3.2.20 redis numpy setuptools

# label-studio config for serving local files through the web server
ENV LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true
ENV LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=/label-studio/data

ADD labeling_interfaces/asr_labeling_interface.xml /label-studio/data/label_config/asr_labeling_interface.xml

# funnily, the web docs for the CLI reference are wrong. pattern is: label-studio init [OPTIONS] [PROJECT_NAME]
RUN pipx run label-studio init \
    --username default_user@localhost --password salaiFOIAdata2023 \
    --label-config /label-studio/data/label_config/asr_labeling_interface.xml \
    FOIA-Data

# same here: label-studio start [OPTIONS] [PROJECT_NAME]
ENTRYPOINT [ "pipx", "run", "label-studio", "start", "FOIA-Data" ]
