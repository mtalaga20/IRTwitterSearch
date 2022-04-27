# PROJECT
## Front end
* ~~matched token highlighting in front end~~
* show percent match (maybe we already have this?)
* porter-stemmer front end for highlighting

## Crawling
* ~~fix twitter specific parsing error in crawler (!!!)~~
* add URL repository to disk (url, time crawled)

## Indexing
* modify position information to work w/ stop list
* evaluate the indexing structure to decrease size on disk? (if we have time)

## Search Engine
* check code and make sure we are NOT looping through all dimensions for cosine similarity (but doc vals are still normalized)
* semantic scoring with FastText embeddings? (if we have time)

## Analysis
* evaluation as per project requirements (should show that adding RF and term proximity increase performance)

## Infrastructure
* connect front end to backend/ check search engine interface

## Deployment
* nginx w/ reverse proxy, nginx static w\ gunicorn for api
* docker?

## Documentation
* update README
* update requirements.txt

## ACTIONS
* run the crawler to get more tweets (few thousand)

# PRESENTATION
* design outline
* make figures
* decide who presents which slides
* references?

# REPORT
* make and share latex doc
* make outline
* find references
