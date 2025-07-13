import { serveStatic } from 'wrangler-static-assets';

export default {
  async fetch(request, env, ctx) {
    return serveStatic(request, env, ctx);
  }
} 