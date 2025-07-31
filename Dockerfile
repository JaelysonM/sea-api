###########
# BUILDER #
###########

# pull official base image - Updated to Bullseye
FROM python:3.9-slim-bullseye AS builder

# set work directory 
WORKDIR /usr/app


# set environment variables 
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PIPENV_VENV_IN_PROJECT=1

# install dependencies
# Note: build-essential and other packages are available in Bullseye
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
RUN pip install pipenv
RUN pipenv lock && pipenv install --deploy --ignore-pipfile


#########
# FINAL #
#########

# pull official base image - Updated to Bullseye
FROM python:3.9-slim-bullseye

# Install runtime dependencies
# Note: chromium and other packages are available in Bullseye
RUN apt-get update && apt-get install -y --no-install-recommends \
  libpq-dev \
  xvfb \
  gnupg2 \
  wget \
  libxrender1 \
  libfontconfig1 \
  libxtst6 \
  xz-utils \
  chromium \
  libxcursor1 \
  libxss1 \
  libpangocairo-1.0-0 \
  libgtk-3-0 \
  locales && \
  apt-get autoremove -y && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# Copy the virtual environment from the builder stage
COPY --from=builder /usr/app/.venv /.venv

# Add the virtual environment to the PATH
ENV PATH="/.venv/bin:$PATH"

# set work directory
WORKDIR /usr/app

# Copy entrypoint and application code
COPY ./entrypoint.sh .
COPY ./ .

# Make entrypoint executable and install pyppeteer
RUN chmod +x /usr/app/entrypoint.sh
RUN pip install pyppeteer
RUN pyppeteer-install

# Expose the port the app runs on
EXPOSE 5000

# Define the entrypoint and default command
ENTRYPOINT ["/usr/app/entrypoint.sh"]
CMD ["python3", "-m", "uvicorn", "src.sicriaapi.adapters.entrypoints.application:app", "--reload", "--host", "0.0.0.0", "--port", "5000", "--workers", "6"]
