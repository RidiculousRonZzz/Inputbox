@echo off
powershell -Command "Start-Process cmd -ArgumentList '/s,/c,python lastWeek.py > lastWeek.txt 2>&1' -Verb RunAs"
