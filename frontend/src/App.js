import './App.css';
import React, { useEffect, useState } from 'react';
import { Typography, Paper, Container, TextField, Button, Divider } from "@mui/material";
import SearchIcon from '@mui/icons-material/Search';
import { DataGrid } from "@mui/x-data-grid";

const API_URL = "http://localhost:8000/query"

const DisplayResults = (props) => {
  const tweets = props.tweets

  console.log(tweets)
  // Grid column definition
  const columns = [
    {
      field: "rank",
      headerName: "Rank",
      width: 75
    },
    { field: "link", headerName: "Reference", width: 400 },
    {
      field: "href",
      headerName: "Link", width: 500, 
      renderCell: (params) => {
        return <a target="_blank" href={params.value} rel="noreferrer">{params.value}</a>
      }}
  ];

  return (
    <DataGrid
      columns={columns}
      loading={tweets.length === 0}
      rows={tweets}
      getRowId={row => {
        return row.rank;
      }}
    />
  )
}

export const App = () => {
  const [results, setResults] = useState(undefined);
  const [query, setQuery] = useState("");

  const searchParams = new URLSearchParams(window.location.search)

  const queryParam = searchParams.has("q") ? searchParams.get("q") : null

  const executeSearch = async () => {
    const res = await CallAPI(query)
    if (res) {
      setResults(res["ranked_results"].map(([rank, link]) => {
        return {
          "rank": rank,
          "link": link,
          "href": "https://twitter.com" + link
        }
      }));
    }
    // TODO: Fix forward ref update here
  }

  useEffect(() => {
    if (queryParam == null) {
      return;
    }
    // Update the query automatically
    CallAPI(queryParam).then((res) => {
      if (res) {
        setResults(res["ranked_results"].map(([rank, link]) => {
          return {
            "rank": rank,
            "link": link,
            "href": "https://twitter.com" + link
          }
        }));
      }
    })
  }, [queryParam])

  const CallAPI = async (queryText) => {
    let out = { query: queryText }
    console.log(out)

    return fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      cors: "no-cors",
      body: JSON.stringify(out)
    }).then(res => res.json())
  }

  return (
    <Paper style={{ minHeight: "100%", height: "auto", display: "flex", flexDirection: "column" }} elevation={3}>
      <Typography style={{ margin: "2.5% auto", textAlign: "center" }} variant="h2" gutterBottom>
        Twitter Search Tool
      </Typography>
      <Divider />
      {!results ? // TODO make more nuanced check condition
        (
          <Container maxWidth="lg" style={{ marginTop: "2.5%", display: "flex", flexDirection: "row", justifyContent: "center", alignItems: "center" }}>
            <Typography variant='h5'>Search for Tweets: </Typography>
            <SearchIcon />
            <TextField id="search-query-field" label="Query" value={query} onChange={(e) => setQuery(e.target.value)} />
            <Button id="submit-query" variant="text" onClick={executeSearch}>Search</Button>
          </Container>
        )
        : <DisplayResults tweets={results} />
      }
    </Paper>
  );
}
