@echo off
echo Starting Redis and PostgreSQL...
cd /d %~dp0
docker-compose up -d
start stock-trading.exe
exit