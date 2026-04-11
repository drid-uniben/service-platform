import { Injectable, NotFoundException } from '@nestjs/common';
import { EmailMessage, AttemptStatus } from '@prisma/client';
import { PrismaService } from '../database/prisma/prisma.service';
import { ProviderFactory } from '../providers/provider.factory';
import { WebhookService } from '../webhooks/webhook.service';
import { SendEmailDto } from './dto/send-email.dto';
import { SendInvitationEmailDto } from './dto/send-invitation-email.dto';

@Injectable()
export class EmailService {
  constructor(
    private readonly prismaService: PrismaService,
    private readonly providerFactory: ProviderFactory,
    private readonly webhookService: WebhookService,
  ) {}

  async queueEmail(
    accountId: string,
    payload: SendEmailDto,
    requestId?: string,
  ): Promise<{ id: string; status: 'queued' }> {
    const emailMessage = await this.prismaService.emailMessage.create({
      data: {
        accountId,
        to: payload.to,
        subject: payload.subject,
        html: payload.html,
        text: payload.text,
        status: 'queued',
      },
    });

    queueMicrotask(() => {
      void this.deliverEmail(emailMessage.id, requestId);
    });

    return {
      id: emailMessage.id,
      status: 'queued',
    };
  }

  async queueInvitationEmail(
    accountId: string,
    payload: SendInvitationEmailDto,
    requestId?: string,
  ): Promise<{ id: string; status: 'queued' }> {
    const normalizedCategory = payload.category.trim().toLowerCase();
    const subject =
      payload.subject?.trim() || 'DRID Internship Challenge Invitation';
    const html = this.buildInvitationHtml(
      payload.inviteLink,
      normalizedCategory,
    );

    return this.queueEmail(
      accountId,
      {
        to: payload.to,
        subject,
        html,
      },
      requestId,
    );
  }

  async getStatus(accountId: string, emailId: string): Promise<EmailMessage> {
    const message = await this.prismaService.emailMessage.findFirst({
      where: {
        id: emailId,
        accountId,
      },
    });

    if (!message) {
      throw new NotFoundException('Email message not found.');
    }

    return message;
  }

  private buildInvitationHtml(inviteLink: string, category: string): string {
    return `
      <p>You have been invited to submit the DRID internship ${category} challenge.</p>
      <p>Use this secure link to continue: <a href="${inviteLink}">${inviteLink}</a></p>
    `;
  }

  private async deliverEmail(
    emailMessageId: string,
    requestId?: string,
  ): Promise<void> {
    const emailMessage = await this.prismaService.emailMessage.findUnique({
      where: { id: emailMessageId },
    });

    if (!emailMessage) {
      return;
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

          await this.recordAttempt(emailMessage.id, provider.name, 'sent');
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
              latencyMs: Date.now() - start,
            }),
          );

          await this.webhookService.emitDeliveryEvent(emailMessage.accountId, {
            emailId: emailMessage.id,
            status: 'sent',
            provider: result.provider,
          });

          return;
        } catch (error) {
          const failureReason =
            error instanceof Error ? error.message : 'Unknown provider failure';

          await this.recordAttempt(
            emailMessage.id,
            provider.name,
            'failed',
            failureReason,
          );

          console.error(
            JSON.stringify({
              requestId,
              provider: provider.name,
              status: 'failed',
              latencyMs: Date.now() - start,
              attempt,
              failureReason,
            }),
          );
        }
      }
    }

    await this.prismaService.emailMessage.update({
      where: { id: emailMessage.id },
      data: { status: 'failed' },
    });

    await this.webhookService.emitDeliveryEvent(emailMessage.accountId, {
      emailId: emailMessage.id,
      status: 'failed',
    });
  }

  private async recordAttempt(
    emailMessageId: string,
    provider: string,
    status: AttemptStatus,
    errorMessage?: string,
  ): Promise<void> {
    await this.prismaService.providerAttempt.create({
      data: {
        emailMessageId,
        provider,
        status,
        errorMessage,
      },
    });
  }
}
