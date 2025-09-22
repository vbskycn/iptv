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

    // 处理 .txt 文件，确保正确的 UTF-8 编码
    if (pathname.endsWith('.txt')) {
      try {
        const assetRes = await env.ASSETS.fetch(request);
        
        // 检查原始响应状态
        if (!assetRes.ok) {
          return assetRes;
        }

        // 获取原始内容作为 ArrayBuffer
        const arrayBuffer = await assetRes.arrayBuffer();
        
        // 尝试检测编码并转换为 UTF-8
        let content;
        try {
          // 首先尝试作为 UTF-8 读取
          const decoder = new TextDecoder('utf-8', { fatal: false });
          content = decoder.decode(arrayBuffer);
          
          // 检查是否包含乱码字符（简单的启发式检测）
          if (content.includes('\uFFFD')) {
            // 如果包含替换字符，尝试其他编码
            const gbkDecoder = new TextDecoder('gbk', { fatal: false });
            const gbkContent = gbkDecoder.decode(arrayBuffer);
            if (!gbkContent.includes('\uFFFD')) {
              content = gbkContent;
            }
          }
        } catch (error) {
          // 如果解码失败，使用原始内容
          content = new TextDecoder('utf-8', { fatal: false }).decode(arrayBuffer);
        }

        // 创建新的响应头
        const newHeaders = new Headers();
        newHeaders.set('Content-Type', 'text/plain; charset=utf-8');
        newHeaders.set('Cache-Control', 'public, max-age=3600');
        newHeaders.set('Access-Control-Allow-Origin', '*');

        return new Response(content, {
          status: assetRes.status,
          headers: newHeaders
        });
      } catch (error) {
        // 如果处理失败，返回错误信息
        return new Response(`Error processing text file: ${error.message}`, {
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
