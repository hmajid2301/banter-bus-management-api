FROM python:3.9.8-slim

COPY dist ./dist/
RUN pip install dist/*
