import {
  Body,
  Controller,
  Get,
  Headers,
  Param,
  Post,
  UseGuards,
} from '@nestjs/common';
import {
  ApiHeader,
  ApiOperation,
  ApiParam,
  ApiResponse,
  ApiSecurity,
  ApiTags,
} from '@nestjs/swagger';
import { CurrentAccount } from '../common/decorators/current-account.decorator';
import { ApiKeyGuard } from '../auth/api-key.guard';
import { SendEmailDto } from './dto/send-email.dto';
import { SendInvitationEmailDto } from './dto/send-invitation-email.dto';
import { EmailService } from './email.service';

@ApiTags('Emails')
@ApiSecurity('api-key')
@Controller('emails')
@UseGuards(ApiKeyGuard)
export class EmailController {
  constructor(private readonly emailService: EmailService) {}

  @Post('send')
  @ApiOperation({ summary: 'Queue a custom HTML email' })
  @ApiHeader({
    name: 'x-request-id',
    required: false,
    description: 'Optional request correlation ID.',
  })
  @ApiResponse({
    status: 201,
    description: 'Email queued successfully.',
    schema: { example: { id: 'cm123exampleemailid', status: 'queued' } },
  })
  async send(
    @CurrentAccount() accountId: string,
    @Body() payload: SendEmailDto,
    @Headers('x-request-id') requestId?: string,
  ): Promise<{ id: string; status: 'queued' }> {
    return this.emailService.queueEmail(accountId, payload, requestId);
  }

  @Post('send-invitation')
  @ApiOperation({
    summary: 'Queue a DRID invitation email using built-in template',
  })
  @ApiHeader({
    name: 'x-request-id',
    required: false,
    description: 'Optional request correlation ID.',
  })
  @ApiResponse({
    status: 201,
    description: 'Invitation email queued successfully.',
    schema: { example: { id: 'cm123exampleemailid', status: 'queued' } },
  })
  async sendInvitation(
    @CurrentAccount() accountId: string,
    @Body() payload: SendInvitationEmailDto,
    @Headers('x-request-id') requestId?: string,
  ): Promise<{ id: string; status: 'queued' }> {
    return this.emailService.queueInvitationEmail(
      accountId,
      payload,
      requestId,
    );
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get delivery status for a queued email' })
  @ApiParam({ name: 'id', description: 'Email message ID.' })
  @ApiResponse({
    status: 200,
    description: 'Current status of the email message.',
  })
  async getStatus(
    @CurrentAccount() accountId: string,
    @Param('id') emailId: string,
  ) {
    return this.emailService.getStatus(accountId, emailId);
  }
}
