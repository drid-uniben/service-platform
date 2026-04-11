import { Injectable, OnModuleDestroy } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { Processor, Queue, Worker } from 'bullmq';
import IORedis, { RedisOptions } from 'ioredis';
import { EMAIL_QUEUE_NAME } from './queue.constants';

export interface EmailQueuePayload {
  emailMessageId: string;
  requestId?: string;
}

@Injectable()
export class QueueService implements OnModuleDestroy {
  private readonly redisClient: IORedis;
  private readonly queue: Queue<EmailQueuePayload>;
  private readonly connection: RedisOptions;

  constructor(private readonly configService: ConfigService) {
    const redisUrl = this.configService.get<string>('redis.url', {
      infer: true,
    }) as string;
    const url = new URL(redisUrl);

    this.connection = {
      host: url.hostname,
      port: Number(url.port || 6379),
      username: url.username || undefined,
      password: url.password || undefined,
      db: url.pathname ? Number(url.pathname.replace('/', '')) || 0 : 0,
      maxRetriesPerRequest: null,
    };

    this.redisClient = new IORedis(redisUrl, { maxRetriesPerRequest: null });
    this.queue = new Queue<EmailQueuePayload>(EMAIL_QUEUE_NAME, {
      connection: this.connection,
      defaultJobOptions: {
        removeOnComplete: 100,
        removeOnFail: 100,
      },
    });
  }

  async enqueueEmailJob(payload: EmailQueuePayload): Promise<void> {
    await this.queue.add('send-email', payload);
  }

  createWorker(
    processor: Processor<EmailQueuePayload, void, string>,
  ): Worker<EmailQueuePayload> {
    return new Worker<EmailQueuePayload>(EMAIL_QUEUE_NAME, processor, {
      connection: this.connection,
      concurrency: 5,
    });
  }

  getRedisClient(): IORedis {
    return this.redisClient;
  }

  async onModuleDestroy(): Promise<void> {
    await this.queue.close();
    await this.redisClient.quit();
  }
}
