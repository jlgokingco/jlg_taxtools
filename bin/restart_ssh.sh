#!/bin/bash

# Check if environment variable is already set and valid
if [ -n "$SSH_AGENT_PID" ] && tasklist | grep -q "ssh-agent.exe.*$SSH_AGENT_PID"; then
    echo "ssh-agent is already running (PID: $SSH_AGENT_PID)."
else
    # Fallback: look for any running ssh-agent.exe process
    AGENT_PID=$(tasklist | grep "ssh-agent.exe" | awk '{print $2}' | head -n 1)

    if [ -n "$AGENT_PID" ]; then
        echo "Found existing ssh-agent (PID: $AGENT_PID). Connecting..."
        
        # MinGW usually creates sockets in /tmp/ or your user profile
        SOCKET_PATH=$(find /tmp/ -type s -name "agent.*" 2>/dev/null | head -n 1)
        
        if [ -n "$SOCKET_PATH" ]; then
            export SSH_AUTH_SOCK=$SOCKET_PATH
            export SSH_AGENT_PID=$AGENT_PID
        else
            echo "Found process but could not locate socket. Starting fresh..."
            eval "$(ssh-agent -s)"
        fi
    else
        echo "ssh-agent not found. Starting a new one..."
        eval "$(ssh-agent -s)"
    fi
fi
