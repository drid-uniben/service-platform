import { ApiProperty } from '@nestjs/swagger';
import { IsString, MinLength } from 'class-validator';

export class CreateApiKeyDto {
  @ApiProperty({
    example: 'drid-intern-backend',
    description: 'Logical account name for issued API keys.',
  })
  @IsString()
  @MinLength(2)
  accountName!: string;
}
