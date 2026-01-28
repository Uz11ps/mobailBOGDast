import { Router } from "express";
import { AuthController } from "../controllers/AuthController";
import { authMiddleware } from "../middleware/authMiddleware";

const router = Router();
const controller = new AuthController();

router.post("/login", controller.login);
router.get("/profile", authMiddleware, controller.getProfile);

export default router;




