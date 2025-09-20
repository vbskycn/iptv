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

    // 处理 .txt 文件，添加 charset=utf-8
    if (pathname.endsWith('.txt')) {
      const assetRes = await env.ASSETS.fetch(request);
      const contentType = assetRes.headers.get('Content-Type') || 'text/plain';

      // 克隆原始 headers
      const newHeaders = new Headers(assetRes.headers);

      // 强制设置正确的 Content-Type 和编码
      newHeaders.set('Content-Type', contentType.split(';')[0] + '; charset=utf-8');

      const content = await assetRes.text(); // 重新读取文本内容（以 UTF-8）

      return new Response(content, {
        status: assetRes.status,
        headers: newHeaders
      });
    }

    // 默认交给 ASSETS 处理
    return await env.ASSETS.fetch(request);
  }
};
