// index.js

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const pathname = url.pathname;

    /**
     * 处理 /logo/ 路径
     * 如果访问 /logo/ 开头的路径，直接返回提示信息
     * 并且设置 Content-Type 为 UTF-8，避免中文提示乱码
     */
    if (pathname.startsWith('/logo/')) {
      return new Response(
        '【提示】logo资源已迁移，请使用：https://livecdn.zbds.top/logo/*.png 访问。',
        {
          status: 403,
          headers: {
            'Content-Type': 'text/plain; charset=utf-8', // ✅ 避免中文乱码
          },
        }
      );
    }

    /**
     * 处理 .txt 文件
     * 从 ASSETS 中获取文件内容，并转换为 UTF-8 字符串
     * 保证浏览器识别为 UTF-8 文本，避免中文乱码
     */
    if (pathname.endsWith('.txt')) {
      try {
        // 从 ASSETS 获取文件
        const assetRes = await env.ASSETS.fetch(request);
        if (!assetRes.ok) {
          return assetRes; // 如果资源不存在，直接返回原始响应
        }

        // ⚠️ 使用 text() 而不是 arrayBuffer()
        // text() 会自动按 UTF-8 解码成字符串
        const text = await assetRes.text();

        // 设置响应头，明确指定 UTF-8 编码
        const headers = new Headers();
        headers.set('Content-Type', 'text/plain; charset=utf-8'); // ✅ 关键
        headers.set('Cache-Control', 'public, max-age=3600');
        headers.set('Access-Control-Allow-Origin', '*');
        headers.set('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS');
        headers.set('Access-Control-Allow-Headers', 'Content-Type');

        // 返回 UTF-8 文本内容
        return new Response(text, {
          status: 200,
          headers: headers,
        });
      } catch (error) {
        // 错误处理，依然保持 UTF-8 避免中文乱码
        return new Response(`Error: ${error.message}`, {
          status: 500,
          headers: {
            'Content-Type': 'text/plain; charset=utf-8',
          },
        });
      }
    }

    /**
     * 默认情况
     * 交给 ASSETS 处理（比如 html、css、js、图片等静态资源）
     */
    return await env.ASSETS.fetch(request);
  },
};
