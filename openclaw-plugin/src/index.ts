const SERVER_URL = process.env.MANGROVE_TRADER_URL || 'http://localhost:8080';

async function callTool(name: string, params: Record<string, unknown>): Promise<unknown> {
  const response = await fetch(`${SERVER_URL}/api/v1/trader/${name}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params),
  });
  return response.json();
}

export function register() {
  return {
    hooks: {
      before_prompt_build: async () => ({
        prependSystemContext: 'MangroveTrader active. Free: trader_my_stats, trader_performance_report. Paid: trader_get_leaderboard ($0.25), trader_search_trader ($0.02). Trades via Twitter @MangroveTrader.',
      }),
    },
    tools: {
      trader_my_stats: async (p: { twitter_handle: string }) => callTool('trader_my_stats', p),
      trader_performance_report: async (p: { twitter_handle: string; timeframe?: string }) => callTool('trader_performance_report', p),
      trader_get_leaderboard: async (p: { timeframe?: string; limit?: number; payment?: string }) => callTool('trader_get_leaderboard', p),
      trader_search_trader: async (p: { twitter_handle: string; payment?: string }) => callTool('trader_search_trader', p),
    },
  };
}
