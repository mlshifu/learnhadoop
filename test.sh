#!/bin/bash

log_file="/path/to/script_log.txt"

log() {
    echo "$(date "+%Y-%m-%d %H:%M:%S") $1" >> "$log_file"
}

# Function to delete files in batches
delete_files_in_batches() {
    local hdfs_files=("$@")
    local start_time=$(date "+%Y-%m-%d %H:%M:%S")

    hadoop fs -rm -r -skipTrash "${hdfs_files[@]}"
    local exit_code=$?

    local end_time=$(date "+%Y-%m-%d %H:%M:%S")

    if [ $exit_code -eq 0 ]; then
        printf "%s\n" "${hdfs_files[@]}" >> success_files.txt
        log "Deleted batch of files (Start Time: $start_time, End Time: $end_time)"
    else
        # Some or all files in the batch failed to delete
        printf "%s\n" "${hdfs_files[@]}" >> failed_files.txt
        log "Failed to delete files. See failed_files.txt for details. (Start Time: $start_time, End Time: $end_time)"
    fi
}

# Function to process files for a given Hive table
process_hive_table() {
    local table_name="$1"
    local output_file="/path/to/${table_name}_files_to_purge.txt"

    # Hive Query to get the list of files to be purged
    hive -e "SELECT file_path FROM $table_name WHERE date_column < date_sub(current_date, 180)" > "$output_file"

    # Read file paths from the output file and split into chunks
    local chunk_size=40000
    local batch_size=100  # Adjust the batch size as needed

    # Process files in batches
    for chunk_file in $(split -l "$chunk_size" "$output_file" "${output_file}.chunk."); do
        local start_time_chunk=$(date "+%Y-%m-%d %H:%M:%S")

        # Read file paths from the chunk file using xargs
        local file_paths=($(xargs -a "$chunk_file"))

        # Delete files in batches
        for ((i = 0; i < ${#file_paths[@]}; i += batch_size)); do
            local batch=("${file_paths[@]:i:batch_size}")
            delete_files_in_batches "${batch[@]}"
        done

        local end_time_chunk=$(date "+%Y-%m-%d %H:%M:%S")
        log "Processing for chunk file $chunk_file completed (Start Time: $start_time_chunk, End Time: $end_time_chunk)"
    done

    # Remove temporary chunk files
    rm "${output_file}.chunk."*

    log "Processing for table $table_name completed"
}

# List of Hive tables to process
hive_tables=("table1" "table2" "table3" "table4" "table5")

# Process each Hive table
for table in "${hive_tables[@]}"; do
    process_hive_table "$table"
done

log "Script completed successfully"
