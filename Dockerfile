FROM python:3.10

WORKDIR /home/elvenpass

RUN mkdir -p /home/elevenpass

COPY ./requirements.txt /home/elevenpass/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /home/elevenpass/requirements.txt

COPY . /home/elevenpass

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

