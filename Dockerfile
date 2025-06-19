###########
# BUILDER #
###########

# pull official base image
FROM python:3.8-slim-buster AS builder

ENV TZ=America/Sao_Paulo

# set work directory 
WORKDIR /usr/app


# set environment variables 
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PIPENV_VENV_IN_PROJECT=1

# install dependencies
RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  git \
  libpq-dev \
  libffi-dev \
  cargo \
  openssl \ 
  netcat-openbsd \
  libxss1 \
  gcc \
  locales && \
  apt-get autoremove -y && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*


# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv lock && pipenv install --deploy --ignore-pipfile


#########
# FINAL #
#########

# pull official base image
FROM python:3.8-slim-buster

ENV TZ=America/Sao_Paulo

RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  git \
  libpq-dev \
  xvfb \
  gnupg2 \
  ffmpeg \
  wget \
  libxrender1 \
  libfontconfig \
  libxtst6 \
  xz-utils \
  chromium libxcursor1 libxss1 libpangocairo-1.0-0 libgtk-3-0 \
  locales && \
  apt-get autoremove -y && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*
# install dependencies
COPY --from=builder /usr/app/.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# set work directory
WORKDIR /usr/app

COPY ./entrypoint.sh .

COPY ./ .

# run entrypoint.sh
RUN chmod +x /usr/app/entrypoint.sh
RUN pip install pyppeteer
RUN pyppeteer-install

EXPOSE 5000

ENTRYPOINT ["/usr/app/entrypoint.sh"]
CMD ["python3", "-m", "uvicorn", "src.seaapi.adapters.entrypoints.application:app", "--reload", "--host", "0.0.0.0", "--port", "5000"]