import logo from "./logo.svg";
import "./App.css";
import * as React from "react";
import { useState } from "react";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import axios from "axios";
import Alert from "@mui/material/Alert";

function App() {
  const [data, setData] = useState();
  const onClick = async () => {
    const data = await axios.get("http://localhost:3001/");
    setData(data);
  };
  return (
    <div className="App">
      <BasicButtons onClick={onClick} />
      <p
        style={{
          color: "red",
        }}
      >
        {data && data.data}
      </p>
      <Alert severity="error">This is an error alert — check it out!</Alert>
    </div>
  );
}

function BasicButtons({ onClick }) {
  return (
    <Stack spacing={2} direction="row">
      <Button variant="text" onClick={onClick}>
        Execute
      </Button>
    </Stack>
  );
}
export default App;
