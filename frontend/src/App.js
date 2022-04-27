import './App.css';
import React, { useEffect, useState } from 'react';
import { Typography, Paper, Container, TextField, Button, Divider } from "@mui/material";
import SearchIcon from '@mui/icons-material/Search';
import { DataGrid } from "@mui/x-data-grid";
import Backdrop from '@mui/material/Backdrop';
import Box from '@mui/material/Box';
import Modal from '@mui/material/Modal';
import Fade from '@mui/material/Fade';

const API_URL = "http://localhost:8000/query"
const UPDATE_API_URL = "http://localhost:8000/updated_query"

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: "60%",
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
};


const MapAPI_Data = ([rank, link, tweet]) => {
  // Used for mapping what we get from the API to how we display it
  return {
    "rank": rank,
    "link": link,
    "href": "https://twitter.com" + link,
    "tweet": tweet
  }
}

const DisplayResults = (props) => {
  const tweets = props.tweets
  // Make array of rough tokens to highlight on
  const queryList = props.original_query.split(" ").map(element => element.toLowerCase())
  const [selectionModel, setSelectionModel] = useState([]);

  const [open, setOpen] = useState(false);
  const handleClose = () => setOpen(false);

  const [title, setTitle] = useState();
  const [modalText, setModalText] = useState();
  const [selectedState, setSelectedState] = useState({
    selectedTweets: [],
    unSelectedTweets: []
  })

  const CallAPI = async (queryText, relevant_docs, irrelevant_docs) => {
    let out = { query: queryText, relevant_tweets: relevant_docs, irrelevant_tweets: irrelevant_docs }

    return fetch(UPDATE_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      cors: "no-cors",
      body: JSON.stringify(out)
    }).then(res => res.json())
  }

  const updateQuery = async () => {
    const res = await CallAPI(props.original_query, selectedState.selectedTweets.map((obj) => obj.link), selectedState.unSelectedTweets.map((obj) => obj.link))
    if (res) {
      props.modifyResults(res["ranked_results"].map(MapAPI_Data));
    }
    // Clear old selections
    setSelectionModel([])
    // TODO: Fix forward ref update here
  }

  // Grid column definition
  const columns = [
    {
      field: "rank",
      headerName: "Rank",
      width: 75
    },
    {
      field: "href",
      headerName: "Link", minWidth: 400, flex: 1,
      renderCell: (params) => {
        return <a target="_blank" href={params.value} rel="noreferrer">{params.value}</a>
      }
    },
    {
      field: "tweet",
      headerName: "Tweet", minWidth: 500, flex: 2,
      renderCell: (params) => {
        // Same rough tokenization
        let tweetText = params.value.split(" ")
        return (<p>{
          // Match case and punctation free
              tweetText.map((token) => queryList.includes(token.replace(/[^a-zA-Z0-9 ]/g, "").toLowerCase()) ? <b> {token}</b> : ` ${token}`)
            }</p>)
      }
    } 
  ];

  return (
    <>
      <Modal
        aria-labelledby="transition-modal-title"
        aria-describedby="transition-modal-description"
        open={open}
        onClose={handleClose}
        closeAfterTransition
        BackdropComponent={Backdrop}
        BackdropProps={{
          timeout: 500,
        }}
      >
        <Fade in={open}>
          <Box sx={style}>
            <Typography id="transition-modal-title" variant="h6" component="h2">
              {title}
            </Typography>
            <Typography id="transition-modal-description" sx={{ mt: 2 }}>
              {modalText}
            </Typography>
          </Box>
        </Fade>
      </Modal>
      <div style={{ display: "flex", flexDirection: "row" }}>
        <Button style={{ width: "20%", margin: "0.5% 0% 0.5% 10%", border: "0.5px solid #088cb1" }} id="re-query"
          onClick={(e) => {
            // Clear results by setting to undefined
            // Clear old query? 
            // TODO: Determine if we actually want to clear query
            props.modifyQuery(undefined)
            props.modifyResults(undefined)
          }}
        >
          Home
        </Button>
        <Button style={{ width: "20%", margin: "0.5% 0 0.5% 40%", border: "0.5px solid #088cb1" }} id="re-query" onClick={updateQuery}>
          Update Query
        </Button>
      </div>
      <DataGrid
        columns={columns}
        loading={tweets.length === 0}
        rows={tweets}
        selectionModel={selectionModel}
        checkboxSelection
        getRowId={row => {
          return row.rank;
        }}
        onCellDoubleClick={(params) => {
          if (params.field === "rank" || params.field === "__check__") {
            return
          }
          if (params.field === "tweet") {
            setTitle("Tweet Text")
          }
          if (params.field === "href") {
            setTitle("Tweet Link")
          }
          setModalText(params.value);
          setOpen(true);
        }}
        onSelectionModelChange={(ids) => {
          const selectedIDs = new Set(ids);
          const localState = {}
          localState.selectedTweets = tweets.filter((row) => selectedIDs.has(row.rank));
          localState.unSelectedTweets = tweets.filter((row) => !selectedIDs.has(row.rank))
          setSelectedState(localState)
          setSelectionModel(ids);
        }}
      />
    </>
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
      setResults(res["ranked_results"].map(MapAPI_Data));
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
        setResults(res["ranked_results"].map(MapAPI_Data));
      }
    })
  }, [queryParam])

  const CallAPI = async (queryText) => {
    let out = { query: queryText }

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
            <Typography style={{ margin: "0 10% 0 0" }} variant='h5'>Search for Tweets: </Typography>
            <SearchIcon />
            <TextField
              id="search-query-field"
              label="Query"
              value={query}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  executeSearch();
                  e.preventDefault();
                }
              }}
              onChange={(e) => setQuery(e.target.value)} />
            <Button id="submit-query" variant="text" onClick={executeSearch}>Search</Button>
          </Container>
        )
        : <DisplayResults
          modifyResults={(up) => setResults(up)}
          modifyQuery={(up) => setQuery(up)}
          original_query={query}
          tweets={results} />
      }
    </Paper>
  );
}
