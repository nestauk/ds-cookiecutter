FROM conda/miniconda3

WORKDIR /home/root/cookiecutter/tests

RUN apt update && apt install -y git make

COPY . /home/root/cookiecutter
RUN pip install -r /home/root/cookiecutter/requirements.txt
RUN git config --global user.email test@example.com
RUN git config --global user.name "Test"

CMD ["python", "-m", "pytest"]
