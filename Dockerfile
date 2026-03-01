FROM python:3.12.3-slim

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system --deploy

COPY . .

ENV PYTHONPATH=/app

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]