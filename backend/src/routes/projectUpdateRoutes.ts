import { Router } from "express";
import { ProjectUpdateController } from "../controllers/ProjectUpdateController";

const router = Router();
const controller = new ProjectUpdateController();

router.get("/collection/:collectionId", controller.getByCollection);
router.post("/", controller.create);
router.delete("/:id", controller.delete);

export default router;
