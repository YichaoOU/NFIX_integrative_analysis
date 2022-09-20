#!/bin/bash
for xx in {1..100}
do
	#bedtools shuffle -i NFIX_all_PU1.bed -g ~/Data/Mouse/mm9/annotations/mm9_main.chrom.sizes -excl excl.bed -noOverlapping > random1.bed
	#bedtools shuffle -i NFIX_all_PU1.bed -g ~/Data/Mouse/mm9/annotations/mm9_main.chrom.sizes -excl excl.bed -noOverlapping > random2.bed
	#cat random1.bed random2.bed > random.bed
	shuf total_random.bed | head -n 743 > random.bed
	module load bedtools;bedtools getfasta -fi /home/yli11/Data/Mouse/mm9/index/STAR/Mus_musculus.NCBIM37.67.add_chr.dna.toplevel.fa -bed random.bed -fo random.fa
	rm *.fimo
	fimo --motif NFIX --norc --parse-genomic-coord --text --thresh 0.0001 selected.homer.meme random.fa > NFIX.fimo
	fimo --motif PU1 --parse-genomic-coord --text --thresh 0.0001 selected.homer.meme random.fa > PU1.fimo
	for i in *.fimo;do fimo_to_bed.py $i;done
	sort -k1,1 -k2,2n NFIX.fimo.pvalue.bed > NFIX.fimo.pvalue.st.bed
	sort -k1,1 -k2,2n PU1.fimo.pvalue.bed > PU1.fimo.pvalue.st.bed
	bedtools closest -a NFIX.fimo.pvalue.st.bed -b PU1.fimo.pvalue.st.bed -k 1 -d > NFIX_PU1_motif.distance.random.$xx
done

