import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn } from "typeorm";

@Entity()
export class News {
  @PrimaryGeneratedColumn("uuid")
  id!: string;

  @Column()
  title!: string;

  @Column("text")
  content!: string;

  @Column({ nullable: true })
  imageUrl!: string;

  @CreateDateColumn()
  createdAt!: Date;
}
