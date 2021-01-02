#!/bin/bash
sudo docker stop compare_api
sudo docker rm compare_api
sudo docker image build -t throwtrash/compare ../
sudo docker run -p 80:80 --restart=always --name compare_api -d throwtrash/compare gunicorn -b 0.0.0.0:80 --timeout=120 app.app