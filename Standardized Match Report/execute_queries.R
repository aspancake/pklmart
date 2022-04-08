# dedicated to creating relevant tables that can be used to produce the report

# libraries ----
library(data.table)
library(RPostgres)
library(DBI)
library(getPass)
library(dplyr)
library(readr)

# configurables ----
host = 'localhost'
port='5432'
dbname='pklm'
user='postgres'

query_wd = 'C:/Users/ASpan/OneDrive/Documents/Pickle/Standardized Match Report/Queries'

# functions ----
# connect to db 
connect_to_db <- function(host, port, dbname, user){
  pw = getPass()
  
  con = dbConnect(RPostgres::Postgres()
                  , host=host
                  , port=port
                  , dbname=dbname
                  , user=user
                  , password=pw)
  
  rm(pw)
  return(con)
}

# function to retrieve data
execute_query <- function(con, query){
  dt = data.table(dbFetch(dbSendQuery(con, query)))
  return(dt)
}

# execute ----
# connect to db
con = connect_to_db(host, port, dbname, user)

# set local directory
setwd(query_wd)

# high level drop shot summary
ts_summ_query = read_file('third_shot_summary_by_team.sql')
ts_summ_dt = execute_query(con, ts_summ_query)

# third shot breakdown by team
ts_breakdown_by_team_query = read_file("third_shot_breakdown_by_team.sql")
ts_by_team_breakdown_dt = execute_query(con, ts_breakdown_by_team_query)