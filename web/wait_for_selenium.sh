#!/bin/sh

# Wait for Selenium to be ready
while true; do
    response=$(curl -s http://selenium:4444/wd/hub/status)
    success=$(echo "$response" | jq -r '.value.ready')

    if [ "$success" = "true" ]; then
        echo "Selenium is ready"
        break
    else
        echo "Waiting for Selenium to be ready..."
        sleep 10
    fi
done

# Continue with your script
