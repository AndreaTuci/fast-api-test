#!/bin/sh

while true; do
    echo "Starting FastAPI app..."
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    if [ $? -ne 0 ]; then
        echo "The FastAPI app exited with an error. Restarting in 5 seconds..."
        sleep 5
    else
        echo "Unexpected exit. Restarting..."
        sleep 1
    fi
done
