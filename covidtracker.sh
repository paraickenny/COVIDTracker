#!/bin/bash



/home/ec2-user/miniconda3/bin/python  /home/ec2-user/covidtracker/pygeo_heatmap/covidtracker_py3.py
/home/ec2-user/miniconda3/bin/python /home/ec2-user/covidtracker/pygeo_heatmap/test_py3.py

cat /home/ec2-user/covidtracker/pygeo_heatmap/statcounter.txt >> /home/ec2-user/covidtracker/pygeo_heatmap/index.html

cp /home/ec2-user/covidtracker/pygeo_heatmap/results/heatmap.html /home/ec2-user/www
cp /home/ec2-user/covidtracker/pygeo_heatmap/index.html /home/ec2-user/www

cp  /home/ec2-user/covidtracker/pygeo_heatmap/results/heatmap.html /home/ec2-user/covidtracker/pygeo_heatmap/results/"heatmap_history_"`date +"%Y-%m-%d"`".html"
mv  /home/ec2-user/covidtracker/pygeo_heatmap/results/heatmap_history*  /home/ec2-user/www/history/
