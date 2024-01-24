#!/bin/bash

# Specify the HDFS directory where your files are located
HDFS_DIR="/your/hdfs/directory"

# Specify the path to the file containing the list of files to be deleted
FILE_LIST="file_list.txt"

# Specify the number of files to delete in each batch
BATCH_SIZE=1000

# Specify the number of parallel threads to run
NUM_THREADS=3

# Specify the checkpoint file
CHECKPOINT_FILE="delete_checkpoint.txt"

# Function to delete files in a batch
delete_files() {
  local start=$1
  local end=$2

  # Create an array to store file paths
  files=()

  # Read the file list and extract files for the current batch
  while IFS= read -r file; do
    files+=("${HDFS_DIR}/${file}")
  done < <(sed -n "${start},${end}p" "$FILE_LIST")

  # Delete files in the current batch
  hadoop fs -rm -skipTrash "${files[@]}"
}

# Check if the checkpoint file exists
if [ -f "$CHECKPOINT_FILE" ]; then
  # Read the last successfully processed batch from the checkpoint file
  last_batch=$(cat "$CHECKPOINT_FILE")
else
  # If the checkpoint file doesn't exist, start from the beginning
  last_batch=0
fi

# Check if the file list exists
if [ -f "$FILE_LIST" ]; then
  # Count the total number of files
  total_files=$(wc -l < "$FILE_LIST")

  # Calculate the number of batches
  num_batches=$((total_files / BATCH_SIZE))

  # Run parallel deletion threads
  for ((i = last_batch; i <= num_batches; i += NUM_THREADS)); do
    start=$((i * BATCH_SIZE + 1))
    end=$((start + BATCH_SIZE - 1))

    # Run the deletion in the background
    delete_files "$start" "$end" &
  done

  # Wait for all background processes to finish
  wait

  # Update the checkpoint file
  echo "$num_batches" > "$CHECKPOINT_FILE"

  echo "Deletion complete."
else
  echo "File list not found: $FILE_LIST"
fi

