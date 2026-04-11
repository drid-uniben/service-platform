import { Module } from '@nestjs/common';
import { AuthModule } from '../auth/auth.module';
import { PrismaModule } from '../database/prisma/prisma.module';
import { ProviderFactory } from '../providers/provider.factory';
import { EMAIL_PROVIDERS } from '../providers/provider.interface';
import { SmtpProvider } from '../providers/smtp.provider';
import { WebhookModule } from '../webhooks/webhook.module';
import { EmailController } from './email.controller';
import { EmailService } from './email.service';

@Module({
  imports: [PrismaModule, AuthModule, WebhookModule],
  controllers: [EmailController],
  providers: [
    EmailService,
    SmtpProvider,
    ProviderFactory,
    {
      provide: EMAIL_PROVIDERS,
      useFactory: (smtpProvider: SmtpProvider) => [smtpProvider],
      inject: [SmtpProvider],
    },
  ],
  exports: [EmailService],
})
export class EmailModule {}
