const express = require("express");
var mongoose = require("mongoose");
const app = express();
const port = 3000;

try {
  mongoose.connect(
    "mongodb://localhost:27017/imageLabeler",
    { useNewUrlParser: true }
  );

  app.get("/", (req, res) => res.send("Hello World!"));

  app.get("/api/images",(req,res)=>res.send("Alo"))

  app.listen(port, () => console.log(`Example app listening on port ${port}!`));
} catch (error) {
  console.log("AAAAAAAA", error);
  process.exit(1);
}
