import { Router } from "express";
import { PartnerController } from "../controllers/PartnerController";

const router = Router();
const controller = new PartnerController();

router.get("/", controller.getAll);
router.post("/", controller.create);
router.delete("/:id", controller.delete);

export default router;
