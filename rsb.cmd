@echo off
setlocal
set "ROSHAMBO_DSN_FILE=C:\_Local_DEV\CREDENTIALS\cockroachdb\roshambo.dsn"
set "ROSHAMBO_SWARM_ID=poc-starmap-2026-07-30"
set "ROSHAMBO_EMBEDDING_PROVIDER=placeholder"
set "PYTHONPATH=C:\_Local_DEV\repos\roshambo\src"
"C:\_Local_DEV\repos\roshambo\.venv\Scripts\python.exe" "C:\_Local_DEV\repos\roshambo\demo\multivendor\rsb.py" %*
