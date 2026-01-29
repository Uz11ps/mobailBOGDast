import { Router } from "express";
import { PaymentController } from "../controllers/PaymentController";
import { authMiddleware } from "../middleware/authMiddleware";

const router = Router();
const controller = new PaymentController();

router.post("/intent", authMiddleware, controller.createIntent);
router.post("/confirm", authMiddleware, controller.confirmPayment);
router.get("/my-donations", authMiddleware, controller.getMyDonations);

export default router;




