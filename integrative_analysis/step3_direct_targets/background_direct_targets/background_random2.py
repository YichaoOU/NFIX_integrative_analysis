import os
import pandas as pd
import sys
from joblib import Parallel, delayed
import uuid

def get_N_target(peaks,tad,gtf,cap,deg):
	
	TAD_command="bed_TAD_gene.py %s %s %s"%(peaks,tad,gtf)

	

	captureC_command = "bed_Capture_gene.py %s %s"%(peaks,cap)

	os.system(TAD_command)
	os.system(captureC_command)
	
	# Parallel(n_jobs=3)(delayed(os.system)(i) for i in [TAD_command,nearest_gene_command,captureC_command])


	command = 'cut -f 5 %s > %s.list1'%(peaks,peaks)
	os.system(command)
	command = 'cat %s.TAD.gene.bed | cut -f 4 > %s.list2'%(peaks,peaks)
	os.system(command)
	command = 'cat %s.capC.gene.bed | cut -f 5 > %s.list3'%(peaks,peaks)
	os.system(command)

	command = "cat {0}.list1 {0}.list2 {0}.list3 > {0}.target.list".format(peaks)
	# command = "cat {0}.list1 {0}.list3 > {0}.target.list".format(peaks)
	os.system(command)
	# filter by DEG



	command = "cat {0}.list1 {0}.list2 {0}.list3 > {0}.target2.list".format(peaks)
	os.system(command)
	# filter by DEG

	# deg = sys.argv[5]
	# df = pd.read_csv(deg,sep="\t")
	total_list = pd.read_csv("%s.target2.list"%(peaks),header=None)
	dn = deg[deg.avg_log2FC<=0]
	up = deg[deg.avg_log2FC>0]
		
	# overlap = set(deg.index).intersection(total_list[0])
	overlap1 = set(dn.index).intersection(total_list[0])
	overlap2 = set(up.index).intersection(total_list[0])
	#df = deg.loc[overlap]
	df1 = deg.loc[overlap1]
	df2 = deg.loc[overlap2]
		
	# df.to_csv("%s.direct_targets.all.tsv"%(deg.split("/")[-1]),sep="\t")
	os.system("rm {0}.list1 {0}.list2 {0}.list3".format(peaks))
	return df1,df2


tad = "GSE119347_BMHSC_TADs.bed.gz"
gtf = "Mus_musculus.mm10_mm9.93.filtered.gtf"
cap = "target.5kb.bed"
chrom_size = "/home/yli11/Data/Mouse/mm9/annotations/mm9.chrom.sizes"

label = sys.argv[1]
deg = sys.argv[2]
deg = "/home/yli11/dirs/NFIX_megan/NFIX_integrative_analysis/NFIX_direct_targets/"+deg
degdf = pd.read_csv(deg,sep="\t")
out = sys.argv[3]
peak = f"{label}.top1k.bed"
addon_string = "random."+str(uuid.uuid4()).split("-")[-1]
# addon_string = "e8cbde61809f"
command = f"bedtools shuffle -i {peak} -g {chrom_size} > {addon_string}.bed"
def run(command,i):
	os.system(command + str(i))
Parallel(n_jobs=10,verbose=10)(delayed(run)(command,i) for i in range(1000))
os.system(f"cat {addon_string}.bed* > {addon_string}.all.bed;rm {addon_string}.bed*")
nearest_gene_command="module load homer/4.10;annotatePeaks.pl %s mm9 -gtf %s > %s.annot.txt"%(f"{addon_string}.all.bed",gtf,f"{addon_string}.all.bed")
os.system(nearest_gene_command)
command = 'sed "1d" %s.annot.txt | cut -f 2,3,4,5,16 > %s.bed'%(f"{addon_string}.all.bed",addon_string)
os.system(command)
import subprocess
def get_N(addon_string,i):
	command = f"cat {addon_string}.bed | shuf - | head -n 1000 | cut -f 1,2,3,4 > {addon_string}.bed{i}"
	# print (command)
	# os.system(command)
	subprocess.call(command,shell=True)
	
	df1,df2 = get_N_target(f"{addon_string}.bed{i}", tad, gtf, cap, degdf.copy())
	os.system(f"rm {addon_string}.bed{i}")
	print ("###",df1.shape[0])
	return [df1.shape[0],df2.shape[0]]

Numbers = Parallel(n_jobs=-1,verbose=10)(delayed(get_N)(addon_string,i) for i in range(100))
print (pd.DataFrame(Numbers))
pd.DataFrame(Numbers).to_csv(f"{out}.random.dn.up.list",sep="\t",header=False,index=False)
os.system(f"rm {addon_string}*")

