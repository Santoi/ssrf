import axios from "axios";
import express, { NextFunction } from "express";

export async function getData(
    req: express.Request,
    res: express.Response
  ) {
    try {
      const urlToRedirect = req.body.urlToRedirect;
      if (!urlToRedirect){
        throw new Error("Url field is missing");
      }
      const response = await axios.get(urlToRedirect, { responseType: 'arraybuffer' });
      if (response.headers['content-type']) {
        res.setHeader('Content-Type', response.headers['content-type']);
      }
      res.setHeader('Access-Control-Allow-Origin', '*');
      res.end(response.data);
    } catch (err) {
      res.status(500).send(`${err}`);
    }
}

export async function getSecret(
  req: express.Request,
  res: express.Response
) {
  res.status(500).send("Method not implemented");
}