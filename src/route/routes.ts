import { Router } from "express";
import { getData, getSecret } from "../controller/image";
import multer from "multer";

export const imageRouter = Router();

imageRouter.get("/secret", getSecret);
imageRouter.post("/image", getData);