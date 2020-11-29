
# GTF-VALIDATOR
Python script for the validation of a GTF file.
GTF is a file-format for genomic sequences. More info about the format [here](https://mblab.wustl.edu/GTF22.html#intro).
### How it works:
 ```validator.py``` is a script that takes a path to a GTF file as input and creates ```validation.txt``` , a text file with the result of the validation process, in the directory of the script. ```validation.txt``` will contain a list of all the errors in the file and where they occured. The script contains useful comments for each function used. 

### Requirements 
For being able to run the script Python need to be present on the computer. It's also needed a file with extension ```.gtf``` and its path. The path needs to be expressed starting from the directory of the script.

### Documentation:
Each GTF file has to respect some specific rules, the validator will analyse the file at the submitted path and check if it respects all these properties, if one ore more properties aren't satisfied an associated error will be present in ``validation.txt``

List of properties checked by the script:

 For each row:
 - The number of elements in the row must be at lest 9.
 - ```start``` needs to be an integer greater than ```0```, ```end``` needs to be an integer greater than ```start```.
- ```feature``` must be equal to one of : ``` ['CDS', 'start_codon', 'stop_codon', '5UTR', '3UTR', 'inter', 'inter_CNS', 'intron_CNS', 'exon']```.
- ```strand``` must be equal to ```+``` or ```-```.
- ```frame``` must be equal to:
  - ```0``` or ```1``` or ```2``` if the relative ```feature``` is equal to ```CDS``` or ```start_codon```, ```stop_codon```.
  - ```.``` otherwise.
- ```attributes``` need to respect the correct syntax (```name "value";```).
- ```attributes``` ```gene_id``` and ```transcript_id``` must be present in the file.
- If ```feature``` is equal to ```inter``` or ```inter_CNS``` then the value of ```gene_id``` and ```transcript_id``` must be empty.
- ```score``` must be a numeric value.

For each gene:
- All ```strand``` values must be equal.

For each transcript of the same gene:
- If there is a ```start_codon``` or  a ```stop_codon``` there must be a ```CDS``` and viceversa.
- ```start_codon``` must be made from 3 bases
- ```stop_codon``` must be made by 3 bases.
- ```CDS```'s length must be a mutiple of 3
- Ranges of rows with feature equal to ```start_codon```, ```stop_codon```, ```CDS```, ```5UTR``` or ```3UTR``` mustn't overlap
- ```start_codon``` needs to be placed correctly at the start of the CDS.
- ```stop_codon``` needs to be placed correctly ather the end or the CDS.
- ```5UTR``` codons need to be placed correctly before the ```start_codon```.
- ```3UTR``` codons need to be placed correctly after the ```stop_codon```
- ```frame``` of the rows with feature equal to ```start_codon```, ```stop_codon```, ```CDS``` must be calculeted correctly using:  ```frame = (3 - ((length-frame) mod 3)) mod 3.```
- Note that the ```strand``` must be considered  when checking the properties for the transcripts of the same gene .
- **Note that rows with errors are not included in the validation of genes and transcripts** 