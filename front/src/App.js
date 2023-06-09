import logo from "./logo.svg";
import "./App.css";
import * as React from "react";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import axios from "axios";
function App() {
    return (
        <div className="App">
            <BasicButtons />
        </div>
    );
}

function BasicButtons() {
    const onClick = async () => {
        const data = await axios.get("http://localhost:3001/");
        console.log(data);
    };

    return (
        <Stack spacing={2} direction="row">
            <Button variant="text" onClick={onClick}>
                Execute
            </Button>
        </Stack>
    );
}
export default App;
