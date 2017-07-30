# Python scripts

## scrape
Grabs the HTML from Parliment web site and converts it to an intermediate XML file.

Usage ```python scrape.py "DATE"```
e.g. ```python scrape.py 20170726```

## transform

Converts the intermediate XML file to Akoma Ntoso XML 

 usage: ```python transform.py "FILE"```
 e.g: ```python transform.py 20170726.xml```


## TODO

* parse question time
* parse voting 
