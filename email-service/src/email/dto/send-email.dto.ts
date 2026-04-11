import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { IsEmail, IsOptional, IsString } from 'class-validator';

export class SendEmailDto {
  @ApiProperty({ example: 'candidate@example.com' })
  @IsEmail()
  to!: string;

  @ApiProperty({ example: 'DRID Internship Update' })
  @IsString()
  subject!: string;

  @ApiProperty({ example: '<p>Your application is now under review.</p>' })
  @IsString()
  html!: string;

  @ApiPropertyOptional({ example: 'Your application is now under review.' })
  @IsOptional()
  @IsString()
  text?: string;
}
