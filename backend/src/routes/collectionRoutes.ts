import { Router } from "express";
import { CollectionController } from "../controllers/CollectionController";

const router = Router();
const controller = new CollectionController();

router.get("/", controller.getAll);
router.get("/:id", controller.getOne);
router.post("/", controller.create);

export default router;

