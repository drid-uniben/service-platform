import {
  CanActivate,
  ExecutionContext,
  Injectable,
  UnauthorizedException,
} from '@nestjs/common';
import { AuthService } from './auth.service';

@Injectable()
export class ApiKeyGuard implements CanActivate {
  constructor(private readonly authService: AuthService) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const request = context.switchToHttp().getRequest<{
      headers: Record<string, string | undefined>;
      accountId?: string;
      apiKeyId?: string;
    }>();

    const rawApiKey = request.headers['x-api-key'];
    if (!rawApiKey) {
      throw new UnauthorizedException('Missing x-api-key header.');
    }

    const apiKeyRecord = await this.authService.validateApiKey(rawApiKey);
    if (!apiKeyRecord) {
      throw new UnauthorizedException('Invalid API key.');
    }

    request.accountId = apiKeyRecord.accountId;
    request.apiKeyId = apiKeyRecord.id;
    return true;
  }
}
