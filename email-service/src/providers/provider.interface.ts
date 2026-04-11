import { SendEmailDto } from '../email/dto/send-email.dto';
import { DeliveryResult } from '../email/interfaces/delivery-result.interface';

export const EMAIL_PROVIDERS = 'EMAIL_PROVIDERS';

export interface EmailProvider {
  readonly name: string;
  send(payload: SendEmailDto): Promise<DeliveryResult>;
}