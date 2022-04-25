# EvilCommas

This repository came to existance because of the way that Google forms saves data from mult-choice quiestions from surveys. 
What it does is it sends data from a single response and saved a response in a row in google spreadsheet. 
Answer to each question in a seperate cell. Answers to questions that allow multiple choice is saved in a single cell with a comma that seperates choices.
The problem is that the questions also are allowed to have commas which leads to chaos in any trial to analyse this data.
So to fix this problem and automate this process as much as I could, this repo was created. For those who had similar problem, enjoy!

## Setup
- go to the root directory and run 
```bash
pip install numpy pandas
```

## Run
- execute script with command 
```bash
python extract.py <filename>
```
Where `filename` is name of file in data folder without the .csv extension for example
```bash
python extracy.py data
```


