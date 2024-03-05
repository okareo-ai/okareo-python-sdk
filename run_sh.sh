#!/bin/bash
while true
do
  bash -c "BASE_URL='http://34.133.182.104:8000' poetry run pytest"
  sleep 10
done
