import csv
import subprocess

def get_hdfs_file_count(cluster_url, hdfs_location):
    try:
        command = f"hdfs dfs -count {cluster_url}/{hdfs_location}"
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            raise Exception(f"Error while running the command: {error.decode()}")
        return int(output.decode().strip().split()[1])
    except Exception as e:
        print(f"Error: {e}")
        return None

def compare_file_counts(cluster1_url, cluster2_url, hdfs_locations):
    print("Comparing HDFS file counts for the given locations in two clusters:")
    print(f"Cluster 1: {cluster1_url}")
    print(f"Cluster 2: {cluster2_url}\n")

    # Create a list to store the comparison results
    comparison_results = []

    for location in hdfs_locations:
        cluster1_count = get_hdfs_file_count(cluster1_url, location)
        cluster2_count = get_hdfs_file_count(cluster2_url, location)

        if cluster1_count is not None and cluster2_count is not None:
            print(f"Location: {location}")
            print(f"Cluster 1 File Count: {cluster1_count}")
            print(f"Cluster 2 File Count: {cluster2_count}")

            if cluster1_count == cluster2_count:
                print("File counts match in both clusters.\n")
            else:
                print("File counts differ between the two clusters.\n")

            comparison_result = {
                "Location": location,
                "Cluster 1 File Count": cluster1_count,
                "Cluster 2 File Count": cluster2_count,
                "Match": cluster1_count == cluster2_count
            }
            comparison_results.append(comparison_result)
        else:
            print(f"Error retrieving file count for location: {location}\n")

    # Save the comparison_results list to a CSV file
    csv_file = "hdfs_file_counts_comparison.csv"
    with open(csv_file, mode='w', newline='') as file:
        fieldnames = ["Location", "Cluster 1 File Count", "Cluster 2 File Count", "Match"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        for result in comparison_results:
            writer.writerow(result)

    print(f"Comparison results have been saved to '{csv_file}'.")

if __name__ == "__main__":
    # Replace 'cluster1_url' and 'cluster2_url' with the HDFS URLs of the two clusters.
    cluster1_url = "hdfs://cluster1_hostname:8020"
    cluster2_url = "hdfs://cluster2_hostname:8020"

    # Read HDFS locations from the txt file (one location per line)
    locations_file = "hdfs_locations.txt"
    with open(locations_file, "r") as file:
        hdfs_locations = [line.strip() for line in file if line.strip()]

    if not hdfs_locations:
        print("No HDFS locations found in the file.")
    else:
        compare_file_counts(cluster1_url, cluster2_url, hdfs_locations)
