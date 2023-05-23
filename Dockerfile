FROM python:3.10

COPY main.py .

# install dependencies
RUN pip install schedule requests

# Start python the foreground. -u forces the stdout and stderr streams to be unbuffered
# which fixed a problem with logs not displaying
CMD ["python","-u","main.py"] 