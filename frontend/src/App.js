import './App.css';
import React, { useState } from 'react';
import { Typography, Paper, Container, TextField, Button, Divider } from "@mui/material";
import SearchIcon from '@mui/icons-material/Search';

const DisplayResults = (props) => {
  const tweets = props.tweets

  return (
    <div>
      TODO: Display Results
      {
        tweets.map((val) => <p>{val}</p>)

      }
    </div>
  )
}

export const App = () => {
  const [results, setResults] = useState(undefined);

  const executeSearch = () => {
    let queryNode = document.getElementById("search-query-field");
    // TODO: Make this actually call api
    setResults([queryNode.innerText])
    // TODO: Fix forward ref update here
  }

  return (
    <Paper style={{ minHeight: "100%", height: "auto", display: "flex", flexDirection: "column" }} elevation={3}>
      <Typography style={{ margin: "2.5% auto", textAlign: "center" }} variant="h2" gutterBottom>
        Twitter Search Tool
      </Typography>
      <Divider />
      { !results ? // TODO make more nuanced check condition
        (
          <Container maxWidth="lg" style={{ marginTop: "2.5%", display: "flex", flexDirection: "row", justifyContent: "center", alignItems: "center" }}>
            <Typography variant='h5'>Search for Tweets: </Typography>
            <SearchIcon />
            <TextField id="search-query-field" label="Query" />
            <Button id="submit-query" variant="text" onClick={executeSearch}>Search</Button>
          </Container>
        )
        : <DisplayResults tweets={results}/>
      }
    </Paper>
  );
}
