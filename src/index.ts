import express from "express";
import "dotenv/config";
import { imageRouter } from "./route/routes";

import cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json());
app.use("", imageRouter);

app.listen(8080, () => {
  console.log(
    `[server]: Server is running at port 8080`,
  );
});
