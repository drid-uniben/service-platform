import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { IsEmail, IsOptional, IsString, IsUrl } from 'class-validator';

export class SendInvitationEmailDto {
  @ApiProperty({ example: 'candidate@example.com' })
  @IsEmail()
  to!: string;

  @ApiProperty({ example: 'https://intern.driduniben.com/invite/abc123token' })
  @IsUrl()
  inviteLink!: string;

  @ApiProperty({ example: 'backend' })
  @IsString()
  category!: string;

  @ApiPropertyOptional({ example: 'DRID Internship Challenge Invitation' })
  @IsOptional()
  @IsString()
  subject?: string;
}
