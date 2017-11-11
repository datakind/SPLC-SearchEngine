# Google_Search_Masterlist_Identifier

This code aims to get for each query in string format the top results in Google Search, check if the results are in the Master List provided by Southern Poverty Law Center, and return the number of times they appear for each search.
*Inputs*:
- Master List -> HateDomainMasterList_Clean.csv
- List of Queries -> ['are immigrants more likely to be on welfare', 'are immigrants allowed to vote', ...] (example)

*Output*:
- Table with all the results from queries, the rank they appear in the search and if it is in masterlist. (exported in .csv)
