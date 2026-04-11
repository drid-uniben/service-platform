import { Body, Controller, Post } from '@nestjs/common';
import { ApiOperation, ApiResponse, ApiTags } from '@nestjs/swagger';
import { AuthService } from './auth.service';
import { CreateApiKeyDto } from './dto/create-api-key.dto';

@ApiTags('Auth')
@Controller('auth')
export class AuthController {
  constructor(private readonly authService: AuthService) {}

  @Post('keys')
  @ApiOperation({ summary: 'Create account API key' })
  @ApiResponse({
    status: 201,
    description: 'API key created successfully.',
    schema: {
      example: {
        accountId: 'cm123exampleaccountid',
        apiKey: 'es_live_xxxxxxxxxxxxxxxxxxxxx',
      },
    },
  })
  async createApiKey(
    @Body() dto: CreateApiKeyDto,
  ): Promise<{ accountId: string; apiKey: string }> {
    return this.authService.createApiKey(dto.accountName);
  }
}
