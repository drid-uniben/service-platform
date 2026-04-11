import { Inject, Injectable } from '@nestjs/common';
import { EMAIL_PROVIDERS, EmailProvider } from './provider.interface';

@Injectable()
export class ProviderFactory {
  constructor(
    @Inject(EMAIL_PROVIDERS) private readonly providers: EmailProvider[],
  ) {}

  getProvidersInOrder(): EmailProvider[] {
    return this.providers;
  }
}
