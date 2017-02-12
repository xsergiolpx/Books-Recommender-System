# Libraries
library(arules)
library(arulesViz)
library(plyr)

scrap_trans = function(entry, map_from, map_to){
  paste(mapvalues(as.array(strsplit(substr(entry, 2, nchar(entry)-1),",")[[1]]),
                  from = map_from,
                  to = map_to,
                  warn_missing = FALSE),
        collapse = ",")
}

lappend <- function ( lst, ...){
  lst <- c(lst, list(...))
  return(lst)
}

eappend <- function(elem, ...){
  elem <- c(elem, ...)
  return(elem)
}

create_transactions = function(trans){
  transactions = list()
  for(i in 1:nrow(trans)){
    single = character()
    for(page in strsplit(x = trans$items[i], split = ",")[[1]]){
      single = eappend(single, page)
    }
    transactions = lappend(transactions, single)
  }
  return(transactions)
}

read_transactions = function(name, separator){
  books = read.csv(name, sep=separator)
  names(books) = c("user", "items")
  books$user = as.character(books$user)
  books$items = as.character(books$items)

  return(create_transactions(books))
}

write_rules = function(rules, name, separator){
  write(rules, file=name, sep=separator)
}

create_rules = function(transactions, support, confidence, target){
  return(apriori(transactions, parameter = list(supp = support, conf = confidence, target = "rules")))
}

