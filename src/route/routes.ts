import { Router } from "express";
import { getData, getSecret, respondOptions } from "../controller/image";
import multer from "multer";

export const imageRouter = Router();

imageRouter.get("/secret", getSecret);
imageRouter.post("/image", getData);
imageRouter.options("/image", respondOptions);
