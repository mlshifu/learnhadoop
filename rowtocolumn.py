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

=========================================================================================================

---
- name: Example Playbook with Handlers
  hosts: your_target_hosts
  tasks:
    - name: Ensure Apache is installed
      ansible.builtin.package:
        name: apache2
        state: present
      register: apache_install_result

    - name: Copy Apache configuration file
      ansible.builtin.copy:
        src: /path/to/apache.conf
        dest: /etc/apache2/apache2.conf
      register: apache_config_copy_result

  handlers:
    - name: Restart Apache
      ansible.builtin.service:
        name: apache2
        state: restarted
      when: apache_install_result.changed or apache_config_copy_result.changed


---
- name: Example Playbook with Handlers
  hosts: your_target_hosts
  tasks:
    - name: Ensure Apache is installed
      ansible.builtin.package:
        name: apache2
        state: present
      notify: 
        - Restart Apache

    - name: Copy Apache configuration file
      ansible.builtin.copy:
        src: /path/to/apache.conf
        dest: /etc/apache2/apache2.conf
      notify: 
        - Restart Apache

  handlers:
    - name: Restart Apache
      ansible.builtin.service:
        name: apache2
        state: restarted
=================================================================================
---
- name: Example Playbook with Handlers
  hosts: your_target_hosts
  tasks:
    - name: Ensure Apache is installed and Copy Apache configuration file
      block:
        - name: Ensure Apache is installed
          ansible.builtin.package:
            name: apache2
            state: present
          register: apache_install_result

        - name: Copy Apache configuration file
          ansible.builtin.copy:
            src: /path/to/apache.conf
            dest: /etc/apache2/apache2.conf
          register: apache_config_copy_result
      changed_when: apache_install_result.changed or apache_config_copy_result.changed

  handlers:
    - name: Restart Apache
      ansible.builtin.service:
        name: apache2
        state: restarted

===============================================================================================================

---
directories:
  - path: "/path/to/your/directory1"
    symlink_path: "/path/to/your/symlink1"
    owner: "user1"
    group: "group1"
    mode: "0755"
  - path: "/path/to/your/directory2"
    symlink_path: "/path/to/your/symlink2"
    owner: "user2"
    group: "group2"
    mode: "0644"
  # Add more directories as needed



---
- name: Create and configure directories
  hosts: your_target_hosts
  tasks:
    - name: Create directories
      file:
        path: "{{ item.path }}"
        state: directory
      with_items: "{{ directories }}"
      register: directory_created

    - name: Change ownership and permissions
      become: true
      ansible.builtin.file:
        path: "{{ item.path }}"
        owner: "{{ item.owner }}"
        group: "{{ item.group }}"
        mode: "{{ item.mode }}"
      with_items: "{{ directories }}"
      when: directory_created.results | bool

    - name: Create symlinks
      file:
        path: "{{ item.symlink_path }}"
        src: "{{ item.path }}"
        state: link
      with_items: "{{ directories }}"
      register: symlink_created

    - name: Validate directories and symlinks
      assert:
        that:
          - directory_created.results | bool
          - symlink_created.results | bool

---
- name: Apply My Ansible Role
  hosts: your_target_hosts
  roles:
    - my_ansible_role

my_ansible_role/
|-- tasks/
|   |-- main.yml
|-- defaults/
|   |-- main.yml
|-- meta/
|   |-- main.yml



=====================================================================================

