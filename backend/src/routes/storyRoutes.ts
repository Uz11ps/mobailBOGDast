import { Router } from "express";
import { StoryController } from "../controllers/StoryController";

const router = Router();
const controller = new StoryController();

router.get("/", controller.getAll);
router.post("/", controller.create);
router.delete("/:id", controller.delete);

export default router;
