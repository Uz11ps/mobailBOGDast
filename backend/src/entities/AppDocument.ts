import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn } from "typeorm";

@Entity()
export class AppDocument {
  @PrimaryGeneratedColumn("uuid")
  id!: string;

  @Column()
  title!: string;

  @Column()
  fileUrl!: string;

  @Column({ nullable: true })
  category!: string; // e.g., "Registration", "Reports", "About Us"

  @CreateDateColumn()
  createdAt!: Date;
}
