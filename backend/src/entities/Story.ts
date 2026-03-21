import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn } from "typeorm";

@Entity()
export class Story {
  @PrimaryGeneratedColumn("uuid")
  id!: string;

  @Column()
  title!: string;

  @Column()
  imageUrl!: string;

  @Column({ nullable: true })
  caption!: string;

  @CreateDateColumn()
  createdAt!: Date;
}
