import { Router } from "express";
import { DocumentController } from "../controllers/DocumentController";

const router = Router();
const controller = new DocumentController();

router.get("/", controller.getAll);
router.post("/", controller.create);
router.delete("/:id", controller.delete);

export default router;
