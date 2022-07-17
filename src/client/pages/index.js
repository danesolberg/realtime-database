import { useEffect, useState, useRef } from 'react';
import Head from 'next/head'
import styles from '../styles/Home.module.css'
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import Box from '@mui/material/Box';


export default function Home() {
  const [websocket, setWebsocket] = useState(null);
  const [query, setQuery] = useState("SELECT * FROM users WHERE name='Alice' or name='Bob' and age>10 or name='Carol' and age=50");
  // const [query, setQuery] = useState("session.query(User).where(or_(User.name=='Alice', and_(User.name=='Bob', User.age>10), and_(User.name=='Carol', User.age==50)))");
  
  const [table, setTable] = useState("users");
  const [targetTable, setTargetTable] = useState(null);
  const [schema, setSchema] = useState(null);
  const [subscriptions, setSubscriptions] = useState([]);
  const [selectedSub, setSelectedSub] = useState("");
  const [data, setData] = useState({});
  const [newRow, setNewRow] = useState({name: 'Carol', age: 10});

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8001/");

    ws.onopen = () => {
      console.log('ws opened');
      setWebsocket(ws)
    };
    ws.onclose = (event) => {
      console.log('ws closed');
    }

    return () => {
      // console.log('closing ws');
      // ws.close();
    }
  }, [])

  useEffect(() => {
    if (!websocket) return;

    websocket.onmessage = e => {
      const message = JSON.parse(e.data);
      console.log('e', message);
      handle(message);
      return false;
    };
  }, [websocket, data]);

  const handle = (event) => {
    if (event.type == "mutation") {
      if (!(event.data.table in data)) {
        console.log(event.data.table)
        console.log(data);
        console.log("1")
        setData(prevData => ({
          ...prevData,
          [event.data.table]: [event.data.value]
        }));
      } else {
        console.log("2")
        console.log(data);
        const table = event.data.table;
        let documents = [...data[table]];
        const changed_document = event.data.value;
        const id = changed_document.id;
        const idx = documents.findIndex(e => e.id === id);
        if (idx === -1) {
          documents.push(changed_document);
        } else {
          documents[idx] = changed_document
        }
        setData(prevData => ({
          ...prevData,
          [table]: documents
        }));
      }
    } else if (event.type == "subscribed") {
      if (!subscriptions.includes(event.data.query)) {
        setSubscriptions(prevSubscriptions => ([...prevSubscriptions, event.data.query]));
      }
    } else if (event.type == "schema") {
      setTargetTable(event.data.table);
      setSchema(event.data.schema);
    }
  }

  const subscribe = () => {
    console.log(query);
    if (query != null) {
      websocket.send(JSON.stringify({
        type: "subscribe",
        data: {
          query
        }
      }));
    }
  }

  const saveRow = () => {
    console.log(newRow);
    if (newRow != null) {
      websocket.send(JSON.stringify({
        type: "mutate",
        data: {
          action: "insert",
          table: targetTable,
          value: newRow
        }
      }));
    }
  }

  const getSchema = () => {
    if (table != null) {
      websocket.send(JSON.stringify({
        type: "get_schema",
        data: {
          table: table
        }
      }));
    }
  }

  const renderList = () => {
    // console.log(data);
    if (targetTable in data) {
      return (
        <List>
          {data[targetTable].map((doc, i) => (
            <ListItem key={i} disablePadding>
              <ListItemText primary={JSON.stringify(doc)} />
            </ListItem>
          ))}
        </List>
      );
    } else {
      return "no data";
    }
  }

  const renderInsertForm = () => {
    if (schema != null) {
      const inputs = Object.entries(schema).map(([k, v], i) => (
        <div key={i}>
          <TextField
            label={k}
            value={newRow[k]}
            onChange={e => {
              setNewRow(prevData => ({
                ...prevData,
                [k]: e.target.value
              }));
            }}
          />
        </div>
      ))

      return (
        <Box
          component="form"
          sx={{
            '& .MuiTextField-root': { m: 1, width: '25ch' },
          }}
          noValidate
          autoComplete="off"
        >
          {inputs}
        </Box>
      )
    } else {
      return null
    }
  }


  return (
    <div className={styles.container}>
      <Head>
        <title>Realtime Database</title>
        <meta name="description" content="Testing realtime database features with websockets" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>
          Realtime Database Tests
        </h1>

        <div style={{ width: "1000px", margin: "25px" }}>
          <Button variant="contained" onClick={subscribe}>Subscribe</Button>
          <TextField fullWidth id="outlined-basic" label="Subscribe to query" variant="outlined" value={query} onChange={e => setQuery(e.target.value)}/>
          <FormControl fullWidth>
            <InputLabel>Select query subscription</InputLabel>
            <Select
              value={selectedSub}
              label="Subscribed table"
              onChange={(e) => setSelectedSub(e.target.value)}
            >
              {subscriptions.map((sub, i) => {
                return <MenuItem key={i} value={sub}>{sub}</MenuItem>
              })}
            </Select>
          </FormControl>
        </div>

        

        <div style={{ width: "1000px", margin: "25px" }}>
          <Button variant="contained" onClick={getSchema}>Enter</Button>
          <TextField fullWidth id="outlined-basic" label="Select target table for inserts" variant="outlined" value={table} onChange={e => setTable(e.target.value)}/>
          
          
          {/* <TextField fullWidth id="outlined-basic" label="Save new row" variant="outlined" value={newRow} onChange={e => setNewRow(e.target.value)}/> */}
        </div>

        <div >

        </div>
        {renderInsertForm()}
        <Button variant="contained" onClick={saveRow}>Insert</Button>
        {renderList()}

      </main>

     
    </div>
  )
}
