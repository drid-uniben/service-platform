import { Injectable } from '@nestjs/common';
import { randomUUID } from 'crypto';
import { SendEmailDto } from '../email/dto/send-email.dto';
import { DeliveryResult } from '../email/interfaces/delivery-result.interface';
import { EmailProvider } from './provider.interface';

@Injectable()
export class MailgunProvider implements EmailProvider {
  readonly name = 'mailgun';

  async send(payload: SendEmailDto): Promise<DeliveryResult> {
    if (payload.subject.toLowerCase().includes('[fail-mailgun]')) {
      throw new Error('Mailgun simulated failure.');
    }

    return {
      provider: this.name,
      status: 'sent',
      messageId: randomUUID(),
    };
  }
}