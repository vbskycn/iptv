// index.js

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const pathname = url.pathname;

    // 处理 /logo/ 路径的请求
    if (pathname.startsWith('/logo/')) {
      return new Response('【提示】logo资源已迁移，请使用：https://livecdn.zbds.top/logo/*.png 访问。', {
        status: 403,
        headers: {
          'Content-Type': 'text/plain; charset=utf-8',
        },
      });
    }

    // 处理 .txt 文件，返回 UTF-8 编码的内容
    if (pathname.endsWith('.txt')) {
      try {
        const assetRes = await env.ASSETS.fetch(request);
        if (!assetRes.ok) {
          return assetRes;
        }

        const originalBytes = await assetRes.arrayBuffer();

        const headers = new Headers();
        headers.set('Content-Type', 'text/plain; charset=utf-8'); // ✅ 加上 UTF-8
        headers.set('Cache-Control', 'public, max-age=3600');
        headers.set('Access-Control-Allow-Origin', '*');
        headers.set('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS');
        headers.set('Access-Control-Allow-Headers', 'Content-Type');

        return new Response(originalBytes, {
          status: 200,
          headers: headers
        });
      } catch (error) {
        return new Response(`Error: ${error.message}`, {
          status: 500,
          headers: {
            'Content-Type': 'text/plain; charset=utf-8'
          }
        });
      }
    }

    // 默认交给 ASSETS 处理
    return await env.ASSETS.fetch(request);
  }
};
