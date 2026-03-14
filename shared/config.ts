export interface ServerConfig { serverUrl: string; apiKey?: string; }
export function loadConfig(): ServerConfig {
  return { serverUrl: process.env.MANGROVE_TRADER_URL || 'http://localhost:8080', apiKey: process.env.MANGROVE_TRADER_API_KEY || undefined };
}
