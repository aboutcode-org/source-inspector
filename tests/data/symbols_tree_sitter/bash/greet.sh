#!/bin/bash

# Define a global variable
GREETING="Hello"

# Define a function to greet the user
greet_user() {
  local username=$1
  echo "$GREETING, $username! Welcome to the Bash scripting tutorial."
}

# Call the function with an argument
greet_user "Alice"
