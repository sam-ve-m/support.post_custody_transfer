mv tests func/
mutatest -s ./func -y 'if' 'nc' 'ix' 'su' 'bs' 'bc' 'bn' -x 60 -n 1000 -t 'python3 -m pytest'
mv func/test .