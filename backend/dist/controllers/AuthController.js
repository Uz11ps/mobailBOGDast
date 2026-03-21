"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.AuthController = void 0;
const AuthService_1 = require("../services/AuthService");
class AuthController {
    constructor() {
        this.authService = new AuthService_1.AuthService();
        this.login = (req, res) => __awaiter(this, void 0, void 0, function* () {
            try {
                const { phone } = req.body;
                if (!phone) {
                    return res.status(400).json({ message: "Phone number is required" });
                }
                // In a real app, here we would verify the SMS code
                const result = yield this.authService.login(phone);
                res.json(result);
            }
            catch (error) {
                res.status(500).json({ message: "Error during login" });
            }
        });
        this.getProfile = (req, res) => __awaiter(this, void 0, void 0, function* () {
            try {
                res.json(req.user);
            }
            catch (error) {
                res.status(500).json({ message: "Error fetching profile" });
            }
        });
    }
}
exports.AuthController = AuthController;
