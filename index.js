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

    // 处理 .txt 文件，直接读取文件内容避免ASSETS编码问题
    if (pathname.endsWith('.txt')) {
      try {
        // 构建文件路径，去掉开头的斜杠
        const filePath = pathname.startsWith('/') ? pathname.slice(1) : pathname;
        
        // 尝试直接读取文件内容
        let content;
        try {
          // 使用fetch直接获取文件内容，绕过ASSETS处理
          const directUrl = new URL(request.url);
          directUrl.hostname = 'raw.githubusercontent.com';
          directUrl.pathname = `/vbskycn/iptv/master/${filePath}`;
          
          const directResponse = await fetch(directUrl.toString());
          if (directResponse.ok) {
            content = await directResponse.text();
          } else {
            // 如果直接获取失败，回退到ASSETS处理
            const assetRes = await env.ASSETS.fetch(request);
            if (!assetRes.ok) {
              return assetRes;
            }
            content = await assetRes.text();
          }
        } catch (directError) {
          // 如果直接获取失败，使用ASSETS处理
          const assetRes = await env.ASSETS.fetch(request);
          if (!assetRes.ok) {
            return assetRes;
          }
          
          // 获取原始内容作为 ArrayBuffer 进行编码处理
          const arrayBuffer = await assetRes.arrayBuffer();
          
          // 尝试多种编码方式
          let decodedContent;
          const encodings = ['utf-8', 'gbk', 'gb2312', 'latin1'];
          
          for (const encoding of encodings) {
            try {
              const decoder = new TextDecoder(encoding, { fatal: false });
              decodedContent = decoder.decode(arrayBuffer);
              
              // 检查是否包含乱码字符
              if (!decodedContent.includes('\uFFFD') && decodedContent.length > 0) {
                content = decodedContent;
                break;
              }
            } catch (e) {
              continue;
            }
          }
          
          if (!content) {
            content = new TextDecoder('utf-8', { fatal: false }).decode(arrayBuffer);
          }
        }

        // 创建响应头
        const headers = new Headers();
        headers.set('Content-Type', 'text/plain; charset=utf-8');
        headers.set('Cache-Control', 'public, max-age=3600');
        headers.set('Access-Control-Allow-Origin', '*');
        headers.set('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS');
        headers.set('Access-Control-Allow-Headers', 'Content-Type');

        return new Response(content, {
          status: 200,
          headers: headers
        });
      } catch (error) {
        // 如果所有方法都失败，返回错误信息
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
