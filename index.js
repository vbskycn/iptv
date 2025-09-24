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

    // 处理 .txt 文件，直接返回原始内容，让浏览器按原始编码显示
    if (pathname.endsWith('.txt')) {
      try {
        // 直接从 ASSETS 获取原始文件
        const assetRes = await env.ASSETS.fetch(request);
        if (!assetRes.ok) {
          return assetRes;
        }

        // 获取原始字节流
        const originalBytes = await assetRes.arrayBuffer();

        // 创建响应头，不指定 charset，让浏览器自动检测
        const headers = new Headers();
        headers.set('Content-Type', 'text/plain');
        headers.set('Cache-Control', 'public, max-age=3600');
        headers.set('Access-Control-Allow-Origin', '*');
        headers.set('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS');
        headers.set('Access-Control-Allow-Headers', 'Content-Type');

        // 直接返回原始字节流
        return new Response(originalBytes, {
          status: 200,
          headers: headers
        });
      } catch (error) {
        return new Response(`Error: ${error.message}`, {
          status: 500,
          headers: {
            'Content-Type': 'text/plain'
          }
        });
      }
    }

    // 默认交给 ASSETS 处理
    return await env.ASSETS.fetch(request);
  }
};
