const express = require("express");
var cors = require("cors");
const app = express();
const process = require("child_process");

app.use(cors());
app.get("/", async function (req, res) {
    const result = await process.spawn("python3", ["../join/test.py"]);
    result.stdout.on("data", function (data) {
        console.log(data.toString());
    });

    res.send("12341234");
});
app.listen(3001, () => console.log("3001 포트 대기"));
