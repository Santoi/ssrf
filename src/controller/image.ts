import axios from "axios";
import express from "express";

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
      if (response.headers['content-type'])
        res.setHeader('Content-Type', response.headers['content-type']);
      res.setHeader('Access-Control-Allow-Origin', '*');
      res.end(response.data);
    } catch (err) {
      res.status(500).send(`${err}`);
    }
}

function req_comes_from_out_of_LAN(req: express.Request){
  return !req.headers['x-forwarded-host'] || req.headers['x-forwarded-host'] === undefined
}

export async function getSecret(
  req: express.Request,
  res: express.Response
) {

  if (req_comes_from_out_of_LAN(req)){
    console.log("hacked");
    res.statusCode = 200;
    res.setHeader('Content-Type', 'text/plain');
    res.end('Dang it, you hacked me!!');
  }else{
    console.log("firewalled");
    res.status(403).send("Access to this method is forbidden");
  }
  
}