ARG BASE_IMAGE=quay.io/jupyter/tensorflow-notebook:cuda-latest

FROM $BASE_IMAGE

# Declare the build arg so it's available in this stage
ARG ENABLE_KAGGLE_DATASETS=false

USER root
WORKDIR /app

# Ensure conda-forge + update mamba solver
RUN conda config --set channel_priority strict

COPY --chown=${NB_UID}:${NB_GID} requirements.txt /app/

# Jupyter config + SSL certs
COPY --chown=${NB_UID}:${NB_GID} jupyter-config/jupyter_notebook_config.py /home/jovyan/.jupyter/
COPY --chown=${NB_UID}:${NB_GID} jupyter-config/certs/* /home/jovyan/.jupyter/

# Optional Kaggle credentials (only used if ENABLE_KAGGLE_DATASETS=true)
COPY --chown=${NB_UID}:${NB_GID} kaggle.json /tmp/kaggle.json

 
RUN mamba install -y pip && \
    pip install --no-cache-dir -r /app/requirements.txt && \
    if [ "$ENABLE_KAGGLE_DATASETS" = "true" ]; then \
        pip install --no-cache-dir kaggle && \
        mkdir -p /home/jovyan/.kaggle && \
        mv /tmp/kaggle.json /home/jovyan/.kaggle/kaggle.json && \
        chmod 600 /home/jovyan/.kaggle/kaggle.json && \
        chown ${NB_UID}:${NB_GID} /home/jovyan/.kaggle/kaggle.json ; \
    else \
        rm -f /tmp/kaggle.json ; \
    fi && \
    mamba clean --all -f -y && \
    find /opt/conda -follow -type f -name '*.a' -delete && \
    find /opt/conda -follow -type f -name '*.pyc' -delete && \
    find /opt/conda -follow -type f -name '*.js.map' -delete


RUN if [ -f /home/jovyan/.jupyter/jupyter_key.key ]; then \
        chmod 600 /home/jovyan/.jupyter/jupyter_key.key; \
    fi && \
    if [ -f /home/jovyan/.jupyter/jupyter_cert.pem ]; then \
        chmod 644 /home/jovyan/.jupyter/jupyter_cert.pem; \
    fi

USER jovyan

EXPOSE 8888
CMD ["jupyter", "notebook"]