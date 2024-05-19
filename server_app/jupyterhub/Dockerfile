FROM jupyterhub/jupyterhub:latest
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN mkdir -p /srv/jupyterhub /home/admin/project_1 && cd /srv/jupyterhub
RUN chmod 777 /home/admin
RUN jupyterhub --generate-config
COPY jupyterhub_config.py /srv/jupyterhub
EXPOSE 8000
CMD ["jupyterhub", "--port", "8000"]