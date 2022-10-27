FROM quay.io/centos/centos:stream8

RUN dnf -y module install python39 && dnf -y install python39 python39-pip 
RUN curl -s https://packagecloud.io/install/repositories/akopytov/sysbench/script.rpm.sh | bash
RUN dnf -y install sysbench-1.0.20
RUN mkdir /sysbench
RUN chmod 777 /sysbench
ADD https://raw.githubusercontent.com/arcalot/arcaflow-plugins/main/LICENSE /sysbench/
ADD README.md /sysbench/
ADD poetry.lock /sysbench/
ADD pyproject.toml /sysbench/
ADD sysbench_plugin.py /sysbench/
ADD test_sysbench_plugin.py /sysbench/
ADD tests /sysbench/tests/
ADD configs /sysbench/configs/
WORKDIR /sysbench

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --without dev
RUN python3.9 test_sysbench_plugin.py

ENTRYPOINT ["python3.9", "/sysbench/sysbench_plugin.py"]
CMD []

LABEL org.opencontainers.image.title="Sysbench Arcalot Plugin"
LABEL org.opencontainers.image.source="https://github.com/arcalot/arcaflow-plugin-sysbench"
LABEL org.opencontainers.image.licenses="Apache-2.0+GPL-2.0-only"
LABEL org.opencontainers.image.vendor="Arcalot project"
LABEL org.opencontainers.image.authors="Arcalot contributors"
LABEL io.github.arcalot.arcaflow.plugin.version="1" 