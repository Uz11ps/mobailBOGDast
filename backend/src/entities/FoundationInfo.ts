import { Entity, PrimaryGeneratedColumn, Column } from "typeorm";

@Entity()
export class FoundationInfo {
  @PrimaryGeneratedColumn()
  id!: number;

  @Column("text")
  aboutText!: string;

  @Column("text")
  historyText!: string;

  @Column("text")
  leadershipText!: string;

  @Column({ nullable: true })
  frenchConnectionText!: string;
}
