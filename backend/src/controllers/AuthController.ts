import { Request, Response } from "express";
import { AuthService } from "../services/AuthService";

export class AuthController {
  private authService = new AuthService();

  login = async (req: Request, res: Response) => {
    try {
      const { phone } = req.body;
      if (!phone) {
        return res.status(400).json({ message: "Phone number is required" });
      }
      // In a real app, here we would verify the SMS code
      const result = await this.authService.login(phone);
      res.json(result);
    } catch (error) {
      res.status(500).json({ message: "Error during login" });
    }
  };

  getProfile = async (req: any, res: Response) => {
    try {
      res.json(req.user);
    } catch (error) {
      res.status(500).json({ message: "Error fetching profile" });
    }
  };
}

