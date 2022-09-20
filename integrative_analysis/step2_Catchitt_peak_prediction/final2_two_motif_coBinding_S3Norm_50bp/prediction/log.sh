for i in *;do echo $i;sort -k 4gr $i/0.7${i}.05.peaks.bed | head -n 1000 > $i.top1k.bed;done

