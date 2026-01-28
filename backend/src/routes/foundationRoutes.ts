import { Router } from "express";
import { FoundationController } from "../controllers/FoundationController";

const router = Router();
const controller = new FoundationController();

router.get("/", controller.getInfo);
router.put("/", controller.updateInfo);

export default router;
