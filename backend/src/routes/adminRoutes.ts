import { Router } from "express";
import { AdminController } from "../controllers/AdminController";

const router = Router();
const controller = new AdminController();

router.post("/login", controller.login);
router.get("/stats", controller.getDashboardStats);
router.post("/collections", controller.createCollection);

export default router;

