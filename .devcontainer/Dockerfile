FROM python:3.11 as dev-base

ARG USERNAME=devuser
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG KCJARGON_ENV
ARG POETRY_VERSION=1.3.1
ARG PYTHON_VERSION=3.11

ENV KCJARGON_ENV=${KCJARGON_ENV} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=${POETRY_VERSION} \
    POETRY_HOME='/usr/local/pypoetry' \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH='/opt/pysetup' \
    VENV_PATH='/opt/pysetup/.venv'

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM dev-base as builder-base

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y \
        ca-certificates \
        libffi-dev \
        python-dev \
        vim \
        curl \
        git \
        iputils-ping \
        build-essential \
        apache2 apache2-utils ssl-cert \
        libapache2-mod-wsgi-py3 \
        # && a2enmod wsgi \
    && curl https://bootstrap.pypa.io/get-pip.py --output /tmp/get-pip.py \
    && python3 /tmp/get-pip.py \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt clean -y && rm -rf /var/lib/apt/lists/*

WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

RUN poetry install --only main


FROM dev-base as dev-container

COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

COPY ./docker/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -s /bin/bash -m $USERNAME  \
    && apt-get update && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# This allows for bash history to remain between rebuilding the devcontainer
RUN SNIPPET="export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.bash_history" \
    && mkdir -p /commandhistory \
    && touch /commandhistory/.bash_history \
    && chown -R $USERNAME /commandhistory \
    && echo "$SNIPPET" >> "/home/$USERNAME/.bashrc"

WORKDIR $PYSETUP_PATH
RUN poetry install

WORKDIR /workspace

USER $USERNAME

ENTRYPOINT ["/docker-entrypoint.sh"]