#!/bin/bash

# Log file
log_file="transfer_log.txt"

# Clear log file
> "$log_file"

# Define source files and target directory on Server B
source_file_list="source_file_list.txt"
target_dir="/path/to/target/directory"

# Define SSH connection details for Server B
userB="userB"
serverB="serverB.example.com"

# Function to perform SFTP transfer and log information
perform_sftp_transfer() {
    local source_file="$1"
    local target_dir="$2"
    local userB="$3"
    local serverB="$4"

    # Log start time
    start_time=$(date +"%Y-%m-%d %H:%M:%S")
    echo "Start time: $start_time" >> "$log_file"

    # SFTP transfer from Server A to Server B
    echo "Transferring file $source_file to $serverB..."
    sftp -o "BatchMode yes" -b - "$userB@$serverB" <<EOF >> "$log_file"
put "$source_file" "$target_dir"
exit
EOF

    # Log end time
    end_time=$(date +"%Y-%m-%d %H:%M:%S")
    echo "End time: $end_time" >> "$log_file"

    # Log file size
    file_size=$(du -sh "$source_file" | cut -f1)
    echo "File size: $file_size" >> "$log_file"

    # Calculate and log transfer time
    start_timestamp=$(date -d "$start_time" +"%s")
    end_timestamp=$(date -d "$end_time" +"%s")
    transfer_time=$((end_timestamp - start_timestamp))
    echo "Transfer time: $transfer_time seconds" >> "$log_file"

    echo "File transfer of $source_file complete."
}

# Loop through each source file from the list and initiate SFTP transfer in parallel
while IFS= read -r source_file; do
    perform_sftp_transfer "$source_file" "$target_dir" "$userB" "$serverB" &
done < "$source_file_list"

# Wait for all background processes to finish
wait

echo "All file transfers complete. Log saved to $log_file."
