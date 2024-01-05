
current_time=$(date +%s)
one_month_ago=$(date -d '1 month ago' +%s)

hadoop fs -ls -R /path/to/parent/directory | awk '{print $3,$6,$7,$NF}' | grep -v '^-' | while read user date time dir; do
  dir_time=$(date -d "$date $time" +%s)
  if [ $dir_time -lt $one_month_ago ]; then
    hadoop fs -du -s $dir | awk -v user=$user '{sum += $1} END {print user, sum/2^30 "GB"}'
  fi
done
