import axios from "axios";
import express from "express";
import fs from "fs";
import dns from "node:dns";

const data = fs.readFileSync("./blacklist.json", "utf8");
const blacklist = new Set(JSON.parse(data));

async function hasToFirewall(hostname: string): Promise<boolean> {
  console.log("hostname is:", hostname);
  const resolved: string = await resolve(hostname);
  console.log("resolved domain:", resolved);
  if (blacklist.has(resolved)) {
    return true;
  }
  return false;
}

function resolvek(hostname: string): Promise<string[]> {
  return new Promise<string[]>((resolve, reject) => {
    dns.resolve(hostname, (err, addresses) => {
      if (err) {
        reject(err);
      } else {
        resolve(addresses);
      }
    });
  });
}

function resolve(hostname: string): Promise<string> {
  return new Promise<string>((resolve) => {
    dns.lookup(hostname, (_err, address, _family) => {
      resolve(address);
    });
  });
}

function sendFirewallMessage(res: express.Response) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.status(403).send(`Access to this method is forbidden`);
}

export function respondOptions(req: express.Request, res: express.Response) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.header(
    "Access-Control-Allow-Headers",
    "Origin, X-Requested-With, Content-Type, Accept, Authorization"
  );
  res.header("Access-Control-Allow-Methods", "PUT, POST, PATCH, DELETE, GET");
  return res.status(200).json({});
}

export async function getData(req: express.Request, res: express.Response) {
  try {
    console.log(req.body.urlToRedirect);
    const urlToRedirect = new URL(req.body.urlToRedirect);
    if (!urlToRedirect) {
      console.log("No url to redirect found");
      throw new Error("Url field is missing");
    }

    // Firewall
    if (await hasToFirewall(urlToRedirect.hostname)) {
      sendFirewallMessage(res);
      return;
    }

    console.log("passed firewall check");
    const response = await axios.get(urlToRedirect.href, {
      responseType: "arraybuffer",
    });
    if (response.headers["content-type"])
      res.setHeader("Content-Type", response.headers["content-type"]);
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.end(response.data);
  } catch (err) {
    console.log("there was an error", (err as Error).message);
    res
      .status(500)
      .send(`There was an error fetching: ${(err as Error).message}`);
  }
}

function req_comes_from_out_of_LAN(req: express.Request) {
  return (
    !req.headers["x-forwarded-host"] ||
    req.headers["x-forwarded-host"] === undefined
  );
}

export async function getSecret(req: express.Request, res: express.Response) {
  if (req_comes_from_out_of_LAN(req)) {
    console.log("hacked");
    res.statusCode = 200;
    res.setHeader("Content-Type", "text/plain");
    res.end("Dang it, you hacked me!!");
  } else {
    console.log("firewalled");
    sendFirewallMessage(res);
  }
}
