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

    // 其他请求交给 ASSETS 处理
    return await env.ASSETS.fetch(request);
  }
};
