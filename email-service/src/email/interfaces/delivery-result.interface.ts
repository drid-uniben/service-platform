export interface DeliveryResult {
  provider: string;
  status: 'sent' | 'failed';
  messageId?: string;
  errorMessage?: string;
}