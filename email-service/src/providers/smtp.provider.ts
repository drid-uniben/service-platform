import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import * as nodemailer from 'nodemailer';
import { Transporter } from 'nodemailer';
import { SendEmailDto } from '../email/dto/send-email.dto';
import { DeliveryResult } from '../email/interfaces/delivery-result.interface';
import { EmailProvider } from './provider.interface';

@Injectable()
export class SmtpProvider implements EmailProvider {
  readonly name = 'smtp';

  private readonly transporter: Transporter;
  private readonly fromAddress: string;

  constructor(private readonly configService: ConfigService) {
    const host = this.configService.get<string>('smtp.host', {
      infer: true,
    }) as string;
    const port = this.configService.get<number>('smtp.port', {
      infer: true,
    }) as number;
    const user = this.configService.get<string>('smtp.user', {
      infer: true,
    }) as string;
    const pass = this.configService.get<string>('smtp.pass', {
      infer: true,
    }) as string;

    this.fromAddress = this.configService.get<string>('smtp.from', {
      infer: true,
    }) as string;

    this.transporter = nodemailer.createTransport({
      host,
      port,
      secure: port === 465,
      auth: {
        user,
        pass,
      },
    });
  }

  async send(payload: SendEmailDto): Promise<DeliveryResult> {
    const result = await this.transporter.sendMail({
      from: `"DRID UNIBEN" <${this.fromAddress}>`,
      to: payload.to,
      subject: payload.subject,
      html: payload.html,
      text: payload.text,
    });

    return {
      provider: this.name,
      status: 'sent',
      messageId: result.messageId,
    };
  }
}
