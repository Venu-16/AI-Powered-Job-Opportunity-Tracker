const express = require("express");
const app = express();

// middleware
app.use(express.json());

// test route
app.get("/", (req, res) => {
  res.send("Backend is running 🚀");
});

// start server
app.listen(5000, () => {
  console.log("Server started on port 5000");
});
