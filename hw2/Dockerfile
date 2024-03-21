FROM continuumio/miniconda3

RUN apt-get update && apt-get install -y \
    texlive \
    texlive-latex-extra \
    texlive-fonts-recommended

COPY . /hw2/

COPY environment.yml .
RUN conda env create -f environment.yml

SHELL ["conda", "run", "-n", "env", "/bin/bash", "-c"]

WORKDIR /hw2/task1&2
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "env", "python", "main.py"]