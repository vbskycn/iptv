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

    // 处理 .txt 文件，强制以 UTF-8 文本输出，尽量自动纠正源编码
    if (pathname.endsWith('.txt')) {
      try {
        // 构建文件路径，去掉开头的斜杠
        const filePath = pathname.startsWith('/') ? pathname.slice(1) : pathname;
        
        // 始终以 ArrayBuffer 读取源字节，再尝试多种编码解码为 UTF-8 文本
        let content;
        let sourceBuffer;
        
        // 优先从 GitHub Raw 拉取同路径文件（保证最新内容与正确字节流）
        const directUrl = new URL(request.url);
        directUrl.hostname = 'raw.githubusercontent.com';
        directUrl.pathname = `/vbskycn/iptv/master/${filePath}`;
        
        const directResponse = await fetch(directUrl.toString());
        if (directResponse.ok) {
          sourceBuffer = await directResponse.arrayBuffer();
        } else {
          // 回退到静态资源存储
          const assetRes = await env.ASSETS.fetch(request);
          if (!assetRes.ok) {
            return assetRes;
          }
          sourceBuffer = await assetRes.arrayBuffer();
        }

        // BOM 检测（UTF-8）
        const bytes = new Uint8Array(sourceBuffer);
        const hasUtf8BOM = bytes.length >= 3 && bytes[0] === 0xEF && bytes[1] === 0xBB && bytes[2] === 0xBF;
        if (hasUtf8BOM) {
          content = new TextDecoder('utf-8', { fatal: false }).decode(bytes.subarray(3));
        }

        // 多编码尝试：utf-8 -> gb18030 -> gbk -> gb2312 -> latin1
        if (!content) {
          const tryEncodings = ['utf-8', 'gb18030', 'gbk', 'gb2312', 'latin1'];
          for (const enc of tryEncodings) {
            try {
              const decoder = new TextDecoder(enc, { fatal: false });
              const decoded = decoder.decode(sourceBuffer);
              // 避免大量替换字符导致的乱码
              if (!decoded.includes('\uFFFD')) {
                content = decoded;
                break;
              }
            } catch (_) {
              // 某些运行时可能不支持特定编码，忽略错误
              continue;
            }
          }
        }

        // 兜底按 UTF-8 解码
        if (!content) {
          content = new TextDecoder('utf-8', { fatal: false }).decode(sourceBuffer);
        }

        // 创建响应头
        const headers = new Headers();
        headers.set('Content-Type', 'text/plain; charset=utf-8');
        headers.set('Cache-Control', 'public, max-age=3600');
        headers.set('Access-Control-Allow-Origin', '*');
        headers.set('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS');
        headers.set('Access-Control-Allow-Headers', 'Content-Type');
        headers.set('Vary', 'Accept-Encoding');

        // 为提升在 Windows 记事本等客户端的兼容性，前置 UTF-8 BOM
        const BOM = '\uFEFF';
        const hasLeadingBOM = content.startsWith(BOM);
        const outputContent = hasLeadingBOM ? content : (BOM + content);

        return new Response(outputContent, {
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
