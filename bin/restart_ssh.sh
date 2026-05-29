#!/bin/bash

# Check if environment variable is already set and valid
if [ -n "$SSH_AGENT_PID" ]; then
    echo "ssh-agent is already running (PID: $SSH_AGENT_PID)."
else
    # Fallback: look for any running ssh-agent.exe process
    AGENT_PID=$(ps -ef | grep "ssh-agent" | awk '{print $2}' | head -n 1)

    if [ -n "$AGENT_PID" ]; then
        echo "Found an existing ssh-agent (PID: $AGENT_PID). Killing it first"
        kill -9 $AGENT_PID
    fi    

    echo "Retarting ssh-agent and adding ssh key"
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/id_ed25519
fi
