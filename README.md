FILES

- 1shot.py : working 1 shot version

- 0shot.py: working 0 shot version

- 2shot.py: working 2 shot verions

previous files save for all policies the output in a text file, 
correctly mentioning which categories are mentioned in the data

Categories: folder with ground truth 

Output: folder with both text and json files

OPP-115: folder with annotations and policies

MAPP_Corpus: alternative policies dataset, still to be tested

In the following files, manually change 0/1/2 basing which few-shot is being performed.

- txt_cleaner.py: deletes entry "Data: Answer" if present to avoid mismatching

- textToJsonResults.py: transforms text files into json files, to match the format of the ground truth extracted

- jaccardIndexCalc.py : (to be renamed) calculated metrics for individual files 

- performances.py: aggregates and averages performances 

txt files show examples of prompts