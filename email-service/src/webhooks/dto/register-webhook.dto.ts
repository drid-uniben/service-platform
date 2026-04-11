import { ApiProperty } from '@nestjs/swagger';
import { IsString, IsUrl } from 'class-validator';

export class RegisterWebhookDto {
  @ApiProperty({
    example: 'https://drid-intern-backend.example.com/hooks/email-delivery',
  })
  @IsUrl()
  url!: string;

  @ApiProperty({ example: 'whsec_very_long_shared_secret' })
  @IsString()
  secret!: string;
}
