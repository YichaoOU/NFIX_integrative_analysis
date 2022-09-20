# Summary

This repository provides analysis and processed data for our paper: `An NFIX mediated regulatory network governs the balance of hematopoietic stem and progenitor cells during hematopoiesis`


# Get Started

## scRNA-seq data analysis, Figure 1 and Figure 2

Seurat obj is `manual_label.RData`, can be found in the NCBI GEO database: `GSE166922`.

Figure 1 shows results for cell clustering and cell type annotation. Protein surface markers and known marker gene expression (panel C, D) were used to define cell types in panel B. Code see `scRNA_seq/cite_seq_analysis.ipynb` and `scRNA_seq/3_7_marker_genes.ipynb`

Figure 2 shows differential abundance analysis. Code for panel A, B: `scRNA_seq/Figure2.ipynb`. Code for panel C `scRNA_seq/GSEApy.ipynb`. GSEA results are `scRNA_seq/GSEA*csv`

During revision, we also calculated the following (see Code `scRNA_seq/differential_abundance.ipynb`):

1. KDE for different bandwidth

2. DAseq analysis for different resolutions


## Functional genomics data analysis, Figure 3 and Figure 4

Initial Data Quality are provided in `HPC5_data_analysis/**/*html` and `HPC7_data_analysis/**/*html`

NFIX IDR peaks: `HPC5_data_analysis/ChIP_seq/NFIX_IDR.noko.st.bed`

PU.1 IDR peaks: `HPC5_data_analysis/ChIP_seq/PU1_IDR.st.bed`

ChIP-seq signal plots (e.g., Fig3.A) were generated using fold enrichment signal from `MACS2` and NFIX IDR peaks. (Data can be found in the GEO database)

Pie chart showing peak distribution (e.g., Fig3.B) was generated using `homer annotatePeaks`

Motif enrichment (e.g., Fig3.C) was generated using `homer findMotifsGenome.pl`

Fig3.D and Fig3.E data (except NFIX) were from HPC7, see `HPC7_data_analysis/ChIP_seq/`. SRA ID is provided in `HPC7_data_analysis/ChIP_seq/sra*list`. We reprocessed these ChIP-seq data using our pipeline, if you need these bw files, just let us know.

HPC5 footprint signal (e.g., Fig4.B) was generated using `HINT ATAC`.

HPC5 super-enhancer in silico prediction code is here: `HPC5_data_analysis/super_enhancer/SE.lsf`, the resulting bed file is `HPC5_data_analysis/super_enhancer/merged_SE.bed`

NFIX-PU1 footprint and motif distance analysis: `HPC5_data_analysis/NFIX_PU1_motif_footprint_analysis/ecdf-with-random.ipynb`

## Integrative analysis, Figure 5

Pipeline shown in Fig5 contains the following steps (in folder `integrative_analysis`).

1. Gathering ATAC-seq data from different blood lineages: `step1_S3norm_ATAC`

2. Together with NFIX and PU.1 motif, to predict new NFIX-PU.1 co-binding sites in other blood lineages: `step2_Catchitt_peak_prediction`

3. Direct target gene finding based on scRNA-seq gene expression (Fig5.B): `step3_direct_targets`

- captureC data: `target.5kb.bed` (extended +/- 5kb) is from Table S5 in https://www.sciencedirect.com/science/article/pii/S2211124719315566?via%3Dihub

- TAD data: `GSE119347_BMHSC_TADs.bed.gz`

- scRNA-seq DEG: `*DEG.orig.ident.logFC02.FDR001.tsv`

4. GO enrichment for direct target genes (Fig5.C): `step4_GO_enrichment`








