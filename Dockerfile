FROM python:3.10
EXPOSE 5000
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
COPY . .
RUN pip install -r requirements.txt
CMD ["flask", "run", "--host", "0.0.0.0"]