import { Body, Controller, Post, UseGuards } from '@nestjs/common';
import {
  ApiOperation,
  ApiResponse,
  ApiSecurity,
  ApiTags,
} from '@nestjs/swagger';
import { ApiKeyGuard } from '../auth/api-key.guard';
import { CurrentAccount } from '../common/decorators/current-account.decorator';
import { RegisterWebhookDto } from './dto/register-webhook.dto';
import { WebhookService } from './webhook.service';

@ApiTags('Webhooks')
@ApiSecurity('api-key')
@Controller('webhooks')
@UseGuards(ApiKeyGuard)
export class WebhookController {
  constructor(private readonly webhookService: WebhookService) {}

  @Post()
  @ApiOperation({ summary: 'Register a delivery webhook endpoint' })
  @ApiResponse({ status: 201, description: 'Webhook endpoint registered.' })
  async register(
    @CurrentAccount() accountId: string,
    @Body() dto: RegisterWebhookDto,
  ) {
    return this.webhookService.registerEndpoint(accountId, dto);
  }
}
