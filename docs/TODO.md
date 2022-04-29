# PROJECT
## Front end

## Crawling
* Load/Save URL Frontier for Crawler

## Indexing
* evaluate the indexing structure to decrease size on disk? (if we have time)

## Search Engine
* semantic scoring with FastText embeddings? (if we have time)
* Identify candidate documents that contain at least one query term.

## Analysis
* evaluation as per project requirements (should show that adding RF and term proximity increase performance)
    - Needs further investigation
    - Create framework for evaluating engine
    - Keep old versions of search engine
    - Prec/Rec Curves?

## Deployment
* nginx w/ reverse proxy, nginx static w\ gunicorn for api
* docker?

## Documentation
* update README
* update requirements.txt

## ACTIONS
* run the crawler to get more tweets (few thousand)
    - Grant: "soccer"
    - Michael: "rock"

## Optimizations
* [hint: there is no need to construct the complete document vector, or loop through all dimensions in the vector space]
* Grant Fill In (sliders on frontend)
* Percent match

# PRESENTATION
* design outline
* make figures
* decide who presents which slides
* references?

# REPORT
* make and share latex doc
* make outline
* find references
