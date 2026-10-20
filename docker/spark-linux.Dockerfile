# Môi trường Linux cho thí nghiệm xây chỉ mục bằng Spark (run_scale.py --part build2).
# Cùng phiên bản thư viện với .venv-spark trên Windows; khác biệt duy nhất có chủ đích là hệ điều hành
# (trên Linux, PySpark dùng daemon fork worker nên không phải khởi động tiến trình Python mới cho mỗi task).
#
#   docker build -t n3-spark-linux -f docker/spark-linux.Dockerfile docker
#   docker run --rm -v "<repo>:/repo" n3-spark-linux bash /repo/docker/run_build2_linux.sh --reps 3
FROM python:3.11-slim-bookworm

RUN apt-get update \
 && apt-get install -y --no-install-recommends openjdk-17-jre-headless procps \
 && rm -rf /var/lib/apt/lists/*
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

RUN pip install --no-cache-dir pyspark==4.0.1 numpy==2.4.6 pandas==3.0.6 pyarrow==26.0.0 psutil==7.2.2 PyYAML==6.0.3

WORKDIR /work
