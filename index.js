// index.js

export default {
  async fetch(request, env, ctx) {
    // 解析请求路径
    const url = new URL(request.url);
    const pathname = url.pathname;

    // 拦截 /logo/ 请求，返回提示
    if (pathname.startsWith('/logo/')) {
      return new Response('【提示】logo资源已迁移，请使用：https://livecdn.zbds.top/logo/*.png 访问。', {
        status: 403,
        headers: {
          'Content-Type': 'text/plain; charset=utf-8',
        },
      });
    }

    // 如果是 .txt 文件，需要设置 charset=utf-8
    if (pathname.endsWith('.txt')) {
      // 获取原始响应
      const assetResponse = await env.ASSETS.fetch(request);

      // 读取响应体（不能直接传 assetResponse，因为只能读取一次）
      const body = await assetResponse.arrayBuffer();

      // 克隆原始响应头，防止丢失缓存控制信息
      const newHeaders = new Headers(assetResponse.headers);
      newHeaders.set('Content-Type', 'text/plain; charset=utf-8');
      // 设置 Content-Disposition 让浏览器直接下载，文件名与请求路径一致
      const filename = pathname.split('/').pop() || 'file.txt';
      newHeaders.set('Content-Disposition', `attachment; filename="${filename}"`);

      // 构造并返回新的 Response
      return new Response(body, {
        status: assetResponse.status,
        statusText: assetResponse.statusText,
        headers: newHeaders,
      });
    }

    // 其他请求交给 ASSETS 处理
    return await env.ASSETS.fetch(request);
  }
};
