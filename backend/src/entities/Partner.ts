import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn } from "typeorm";

@Entity()
export class Partner {
  @PrimaryGeneratedColumn("uuid")
  id!: string;

  @Column()
  name!: string;

  @Column()
  logoUrl!: string;

  @Column({ nullable: true })
  websiteUrl!: string;

  @CreateDateColumn()
  createdAt!: Date;
}
