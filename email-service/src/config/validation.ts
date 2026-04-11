type EnvConfig = Record<string, unknown>;

function isValidUrl(value: unknown): value is string {
  if (typeof value !== 'string' || value.trim() === '') {
    return false;
  }

  try {
    new URL(value);
    return true;
  } catch {
    return false;
  }
}

export function validate(config: EnvConfig): EnvConfig {
  const requiredVars = [
    'DATABASE_URL',
    'SMTP_HOST',
    'SMTP_PORT',
    'SMTP_USER',
    'SMTP_PASS',
    'EMAIL_FROM',
  ];
  for (const variable of requiredVars) {
    if (!config[variable]) {
      throw new Error(`Missing required environment variable: ${variable}`);
    }
  }

  const port = Number(config.PORT ?? 3000);
  if (Number.isNaN(port) || port <= 0) {
    throw new Error('PORT must be a positive number.');
  }

  const smtpPort = Number(config.SMTP_PORT);
  if (Number.isNaN(smtpPort) || smtpPort <= 0) {
    throw new Error('SMTP_PORT must be a positive number.');
  }

  if (config.SHADOW_DATABASE_URL && !isValidUrl(config.SHADOW_DATABASE_URL)) {
    throw new Error('SHADOW_DATABASE_URL must be a valid URL when provided.');
  }

  return {
    ...config,
    PORT: port,
    SMTP_PORT: smtpPort,
  };
}
