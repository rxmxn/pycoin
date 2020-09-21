# first stage
FROM python:3.8.5 AS builder

COPY requirementsDocker.txt .

# install dependencies to the local user directory (eg. /root/.local)
RUN pip install --user -r requirementsDocker.txt

# second unnamed stage
FROM python:3.8.5-slim
WORKDIR /app

ARG ALPHAVANTAGE_KEY

# copy only the dependencies installation from the 1st stage image
COPY --from=builder /root/.local /root/.local
COPY ./coin /app/coin
COPY ./cli.py /app

# update PATH environment variable
ENV PATH=/root/.local:$PATH

# Examples of how to run:
# docker run -e ALPHAVANTAGE_KEY=$ALPHAVANTAGE_KEY -it ramoncd89/pycoin bash
# Server mode:
# docker run -e ALPHAVANTAGE_KEY=$ALPHAVANTAGE_KEY --rm -it -p 8080:8080 ramoncd89/pycoin

EXPOSE 5000
CMD [ "python", "cli.py", "start-server" ]
