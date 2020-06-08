#!/bin/bash

for f in `ls useful_data`
do 
    > $f
done

for f in `ls useful_data`; 
do
    > useful_data/$f
done

for j in `seq 1 2 3`;
do
    class_dir=weka_data/clase_$j
    output_dir_sco=useful_data/logUPSM_clase$j
    output_dir_inc=useful_data/incorrect_clase$j
for i in `seq 10`;
do
    score=`grep "LogScore Bayes" $class_dir/modelo_$i/output`
    echo "Modelo $i: $score" >> $output_dir_sco

    incorrect=`grep "Incorrectly" $class_dir/modelo_$i/output`
    echo "Modelo $i: $incorrect" >> $output_dir_inc
done
done


class_dir=weka_data/clase_2
output_dir_sco=useful_data/logUPSM_clase2
output_dir_inc=useful_data/incorrect_clase2

score=`grep "LogScore Bayes" $class_dir/output`
echo "Modelo 1: $score" >> $output_dir_sco

incorrect=`grep "Incorrectly" $class_dir/output`
echo "Modelo 1: $incorrect" >> $output_dir_inc




