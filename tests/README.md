
In this folder there are several tests for the script, one correct test with strand = '+', one correct test with strand = '-', and 18 tests created for showing all the errors that the script can produce (Some errore are groupped in the same ```test.gtf```, so the script checks more than 18 errors)

**Row's error:**

- test_1.gtf : start needs to be an integer greater than 0, end needs to be an integer greater than start

- test_2.gtf : feature must be equal to one of : ['CDS', 'start_codon', 'stop_codon', '5UTR', '3UTR', 'inter', 'inter_CNS', 'intron_CNS', 'exon']

- test_3.gtf : strand must be equal to + or -.

- test_4.gtf : frame must be equal to: 0 or 1 or 2 if the relative feature is equal to CDS or start_codon, stop_codon, '.' otherwise.

- test_5.gtf : attributes need to respect the correct syntax (name "value";).

- test_6.gtf : attributes gene_id and transcript_id must be present in the file.

- test_7.gtf : If feature is equal to inter or inter_CNS then the value of gene_id and transcript_id must be empty.
- test_19.gtf : ```score``` must be a numeric value.

**Gene's error**:

- test_8.gtf : All strand values must be equal.

**Transcript's error**:

- test_9.gtf : If there is a start_codon or a stop_codon there must be a CDS and viceversa.

- test_10.gtf : start_codon must be made from 3 bases

- test_11.gtf : stop_codon must be made by 3 bases.

- test_12.gtf : CDS's length must be a mutiple of 3

- test_13.gtf : Ranges of rows with feature equal to start_codon, stop_codon, CDS, 5UTR or 3UTR mustn't overlap

- test_14.gtf : start_codon needs to be placed correctly at the start of the CDS.

- test_15.gtf : stop_codon needs to be placed correctly ather the end or the CDS.

- test_16.gtf : 5UTR codons need to be placed correctly before the start_codon.

- test_17.gtf : 3UTR codons need to be placed correctly after the stop_codon

- test_18.gtf : frame of the rows with feature equal to start_codon, stop_codon, CDS must be calculeted correctly