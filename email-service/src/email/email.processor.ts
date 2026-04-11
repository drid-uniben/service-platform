import { Injectable, OnModuleDestroy, OnModuleInit } from '@nestjs/common';
import { Job, Worker } from 'bullmq';
import { PrismaService } from '../database/prisma/prisma.service';
import { ProviderFactory } from '../providers/provider.factory';
import { QueueService } from '../queue/queue.service';
import { WebhookService } from '../webhooks/webhook.service';
import { EmailJobData } from './interfaces/email-job.interface';

@Injectable()
export class EmailProcessor implements OnModuleInit, OnModuleDestroy {
  private worker?: Worker<EmailJobData>;

  constructor(
    private readonly prismaService: PrismaService,
    private readonly providerFactory: ProviderFactory,
    private readonly queueService: QueueService,
    private readonly webhookService: WebhookService,
  ) {}

  onModuleInit(): void {
    this.worker = this.queueService.createWorker(this.handleEmailJob.bind(this));
  }

  async onModuleDestroy(): Promise<void> {
    if (this.worker) {
      await this.worker.close();
    }
  }

  private async handleEmailJob(job: Job<EmailJobData>): Promise<void> {
    const { emailMessageId, requestId } = job.data;

    const emailMessage = await this.prismaService.emailMessage.findUnique({
      where: { id: emailMessageId },
    });

    if (!emailMessage) {
      throw new Error(`Email message not found for job ${emailMessageId}`);
    }

    const providers = this.providerFactory.getProvidersInOrder();

    for (const provider of providers) {
      for (let attempt = 1; attempt <= 3; attempt += 1) {
        const start = Date.now();

        try {
          const result = await provider.send({
            to: emailMessage.to,
            subject: emailMessage.subject,
            html: emailMessage.html,
            text: emailMessage.text ?? undefined,
          });

          const latencyMs = Date.now() - start;
          await this.prismaService.providerAttempt.create({
            data: {
              emailMessageId: emailMessage.id,
              provider: provider.name,
              status: 'sent',
            },
          });

          await this.prismaService.emailMessage.update({
            where: { id: emailMessage.id },
            data: {
              status: 'sent',
              providerUsed: result.provider,
            },
          });

          console.log(
            JSON.stringify({
              requestId,
              provider: provider.name,
              status: 'sent',
              latencyMs,
              failureReason: null,
            }),
          );

          await this.webhookService.emitDeliveryEvent(emailMessage.accountId, {
            emailId: emailMessage.id,
            status: 'sent',
            provider: result.provider,
          });

          return;
        } catch (error) {
          const latencyMs = Date.now() - start;
          const failureReason = error instanceof Error ? error.message : 'Unknown provider failure';

          await this.prismaService.providerAttempt.create({
            data: {
              emailMessageId: emailMessage.id,
              provider: provider.name,
              status: 'failed',
              errorMessage: failureReason,
            },
          });

          console.error(
            JSON.stringify({
              requestId,
              provider: provider.name,
              status: 'failed',
              latencyMs,
              failureReason,
              attempt,
            }),
          );
        }
      }
    }

    await this.prismaService.emailMessage.update({
      where: { id: emailMessage.id },
      data: {
        status: 'failed',
      },
    });

    await this.webhookService.emitDeliveryEvent(emailMessage.accountId, {
      emailId: emailMessage.id,
      status: 'failed',
    });
  }
}