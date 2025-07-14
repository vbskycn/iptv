// index.js

export default {
  async fetch(request, env, ctx) {
    // 获取请求路径
    const url = new URL(request.url);
    const pathname = url.pathname;

    // 如果是 /logo/ 开头的路径，直接返回中文提示，节省 ASSETS 请求额度
    if (pathname.startsWith('/logo/')) {
      return new Response('【提示】logo资源已迁移，请使用：https://livecdn.zbds.top/logo/*.png 访问。', {
        status: 403, // 或用 404 更“安静”
        headers: {
          'Content-Type': 'text/plain; charset=utf-8',
        },
      });
    }

    // 其他正常请求走静态资源绑定
    return await env.ASSETS.fetch(request);
  }
};
