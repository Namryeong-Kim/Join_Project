const express = require("express");
var cors = require("cors");
const app = express();
const process = require("child_process");

app.use(cors());
app.get("/", async function (req, res) {
  const result = await process.spawn("python3", [
    "../join/run_detectors/detectors.py",
  ]);
  result.stdout.on("data", function (data) {
    const sendResult = data.toString();
    res.send(sendResult);
  });
});
app.listen(3001, () => console.log("3001 포트 대기"));
