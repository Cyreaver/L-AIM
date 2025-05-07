# -*- coding: utf-8 -*-
"""
Created on Fri May  2 10:31:20 2025

@author: robbi
"""
#!/bin/bash

# Default configuration
GHIDRA_INSTALL_DIR=""
SCRIPT_PATH=""
IMPORT_DIR=""
PROJECT_DIR="/tmp/ghidra_batch_proj"
RECURSIVE=0

# Function to display usage
usage() {
    echo "Usage: $0 -g <ghidra_dir> -s <script_path> -i <input_dir> [-p <project_dir>] [-r]"
    echo ""
    echo "Options:"
    echo "  -g <ghidra_dir>     Path to Ghidra installation directory"
    echo "  -s <script_path>    Path to your DecompileAllToFile.py script"
    echo "  -i <input_dir>      Directory containing binaries to decompile"
    echo "  -p <project_dir>    (Optional) Temp directory for Ghidra projects [default: /tmp/ghidra_batch_proj]"
    echo "  -r                  (Optional) Recursively search directories for binaries"
    echo "  -h                  Show this help message"
    exit 1
}

# Parse command-line arguments
while getopts "g:s:i:p:rh" opt; do
  case $opt in
    g) GHIDRA_INSTALL_DIR="$OPTARG" ;;
    s) SCRIPT_PATH="$OPTARG" ;;
    i) IMPORT_DIR="$OPTARG" ;;
    p) PROJECT_DIR="$OPTARG" ;;
    r) RECURSIVE=1 ;;
    h) usage ;;
    *) usage ;;
  esac
done

# Check for required parameters
if [[ -z "$GHIDRA_INSTALL_DIR" || -z "$SCRIPT_PATH" || -z "$IMPORT_DIR" ]]; then
    echo "Error: Missing required arguments."
    usage
fi

# Validate paths
if [[ ! -d "$GHIDRA_INSTALL_DIR" ]]; then
    echo "Error: Ghidra directory '$GHIDRA_INSTALL_DIR' does not exist."
    exit 1
fi

if [[ ! -f "$SCRIPT_PATH" ]]; then
    echo "Error: Script '$SCRIPT_PATH' does not exist."
    exit 1
fi

if [[ ! -d "$IMPORT_DIR" ]]; then
    echo "Error: Input directory '$IMPORT_DIR' does not exist."
    exit 1
fi

mkdir -p "$PROJECT_DIR"

# File search options
if [[ $RECURSIVE -eq 1 ]]; then
    FILES=$(find "$IMPORT_DIR" -type f)
else
    FILES=$(find "$IMPORT_DIR" -maxdepth 1 -type f)
fi

# Process each file
for BINARY in $FILES; do
    if [[ -f "$BINARY" ]];
