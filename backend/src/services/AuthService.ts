import { AppDataSource } from "../data-source";
import { User } from "../entities/User";
import jwt from "jsonwebtoken";

export class AuthService {
  private userRepository = AppDataSource.getRepository(User);

  async login(phone: string) {
    let user = await this.userRepository.findOne({ where: { phone } });
    if (!user) {
      user = this.userRepository.create({ phone });
      await this.userRepository.save(user);
    }

    const token = jwt.sign(
      { userId: user.id },
      process.env.JWT_SECRET || "supersecretkey",
      { expiresIn: "7d" }
    );

    return { user, token };
  }

  async updateProfile(userId: string, data: { name?: string; email?: string }) {
    await this.userRepository.update(userId, data);
    return await this.userRepository.findOne({ where: { id: userId } });
  }
}




