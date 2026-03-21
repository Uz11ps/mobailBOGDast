import { Router } from "express";
import { NewsController } from "../controllers/NewsController";

const router = Router();
const controller = new NewsController();

router.get("/", controller.getAll);
router.post("/", controller.create);
router.delete("/:id", controller.delete);

export default router;
