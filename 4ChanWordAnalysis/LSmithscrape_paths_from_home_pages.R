# A. Information needed for getting started
     # 1. load needed libraries & functions
     rm(list = ls())
     library(dplyr)
     library(stringr)
     library(readr)
     library(XML)
     library(urltools)

     # 2. Functions that I created to scrape & parse data
          # i. gather: collects the links found on the landing page of each site
          gather = function(domain){
                         doc = try(htmlTreeParse(domain, useInternal = TRUE))
                         links = try(getHTMLLinks(doc))
                         #new_sites = try(links[str_detect(string = links, pattern = "htt")])
                    return(links)
                    }
          # ii. function used to clean the links found on homepages so that only the link's domain is returned
          clean_domains = function(link_list){
                              parsed = url_parse(link_list)$domain %>% na.omit() %>% unique()
                              # remove any string that doesnt have a period "." because this suggests that the domain is actually a path
                         return(parsed)
                         }
          
     # 3. load dataset, which is the original dataset containing the names & website links for hate groups
     df = read_csv("~/Documents/SPLC_Hate/Project/Data/HateDomainMasterList_Clean.csv")

# B. Steps to get the paths found on each sites landing page & find domains common on multiple sites
     # 1. For each domain, scrape the paths found on the home page
     df$links = lapply(X = domains, FUN = gather)
     # 2. reduce dataset by removing hate sites with homepages that did not contain links (or scrapable links)
     df2 = dplyr::filter(df, !str_detect(links, pattern = "Error"))
     df2$link_length = as.numeric(lapply(X = df2$links, FUN = length))
     df2 = df2[df2$link_length >0,]
     # 3. Clean the links from each page so that only the domain remains
     df2$clean_links = lapply(X = df2$links, FUN = clean_domains)
     # 4. Count the links
     # For each link, find the number of homepages it was found on 
     link_count = sort(table(unlist(df2$clean_links)), decreasing = T)
          # view all of the links that appear on more than once
          View(sort(link_count[link_count>1], decreasing = T)) 
