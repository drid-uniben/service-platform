import { Injectable } from '@nestjs/common';
import { randomUUID } from 'crypto';
import { SendEmailDto } from '../email/dto/send-email.dto';
import { DeliveryResult } from '../email/interfaces/delivery-result.interface';
import { EmailProvider } from './provider.interface';

@Injectable()
export class SesProvider implements EmailProvider {
  readonly name = 'ses';

  async send(payload: SendEmailDto): Promise<DeliveryResult> {
    if (payload.subject.toLowerCase().includes('[fail-ses]')) {
      throw new Error('SES simulated failure.');
    }

    return {
      provider: this.name,
      status: 'sent',
      messageId: randomUUID(),
    };
  }
}