"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = require("express");
const FoundationController_1 = require("../controllers/FoundationController");
const router = (0, express_1.Router)();
const controller = new FoundationController_1.FoundationController();
router.get("/", controller.getInfo);
router.put("/", controller.updateInfo);
exports.default = router;
