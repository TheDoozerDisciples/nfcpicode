#!/bin/bash



# Navigate to the testsite directory

cd /path/to/testsite || { echo "Failed to locate testsite directory"; exit 1; }



# Run "npm run dev" in the background

npm run dev &

echo "npm run dev started in the background"


# Wait for 10 seconds

echo "Waiting for 10 seconds..."

sleep 10


# Navigate to the nfcpicode directory

cd /path/to/nfcpicode || { echo "Failed to locate nfcpicode directory"; exit 1; }



# Run script.py

python3 script.py || { echo "Failed to execute script.py"; exit 1; }



echo "Script executed successfully"