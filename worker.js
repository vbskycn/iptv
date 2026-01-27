/**
 * Cloudflare Worker 脚本
 * 使用 Workers Assets 直接服务静态文件
 * 文件存储在 CF 边缘网络，无需从 GitHub 代理
 */

import { getAssetFromKV } from '@cloudflare/kv-asset-handler';

export default {
    async fetch(request, env, ctx) {
        try {
            // 使用 Workers Assets 获取静态文件
            const response = await getAssetFromKV(
                {
                    request,
                    waitUntil: ctx.waitUntil.bind(ctx),
                },
                {
                    // 必须传入 KV 命名空间绑定
                    ASSET_NAMESPACE: env.__STATIC_CONTENT,
                    // 自定义缓存控制
                    cacheControl: {
                        browserTTL: 3600,        // 浏览器缓存 1 小时
                        edgeTTL: 86400,          // 边缘缓存 24 小时
                        bypassCache: false,
                    },
                    // 自定义路径映射
                    mapRequestToAsset: (req) => {
                        const url = new URL(req.url);
                        let pathname = url.pathname;

                        // 处理根路径
                        if (pathname === '/' || pathname === '') {
                            pathname = '/index.html';
                        }
                        // 如果路径是目录，添加 index.html
                        else if (pathname.endsWith('/')) {
                            pathname = pathname + 'index.html';
                        }

                        url.pathname = pathname;
                        return new Request(url.toString(), req);
                    },
                }
            );

            // 强制修正 Content-Type，确保所有文本文件使用 UTF-8
            const url = new URL(request.url);
            const pathname = url.pathname.toLowerCase();

            // 创建新的响应头
            const headers = new Headers(response.headers);

            // 根据文件扩展名设置正确的 Content-Type（强制覆盖）
            if (pathname.endsWith('.txt') || pathname.endsWith('.m3u')) {
                headers.set('Content-Type', 'text/plain; charset=utf-8');
            } else if (pathname.endsWith('.m3u8')) {
                headers.set('Content-Type', 'application/vnd.apple.mpegurl; charset=utf-8');
            } else if (pathname.endsWith('.html') || pathname.endsWith('.htm')) {
                headers.set('Content-Type', 'text/html; charset=utf-8');
            } else if (pathname.endsWith('.css')) {
                headers.set('Content-Type', 'text/css; charset=utf-8');
            } else if (pathname.endsWith('.js') || pathname.endsWith('.mjs')) {
                headers.set('Content-Type', 'application/javascript; charset=utf-8');
            } else if (pathname.endsWith('.json')) {
                headers.set('Content-Type', 'application/json; charset=utf-8');
            } else if (pathname.endsWith('.xml')) {
                headers.set('Content-Type', 'application/xml; charset=utf-8');
            } else if (pathname.endsWith('.md')) {
                headers.set('Content-Type', 'text/markdown; charset=utf-8');
            } else if (pathname.endsWith('.svg')) {
                headers.set('Content-Type', 'image/svg+xml; charset=utf-8');
            }

            // 添加 CORS 头（允许跨域访问）
            headers.set('Access-Control-Allow-Origin', '*');

            // 返回修改后的响应（强制使用新的 headers）
            return new Response(response.body, {
                status: response.status,
                statusText: response.statusText,
                headers: headers,
            });

        } catch (error) {
            // 如果文件不存在，尝试返回 404 页面
            if (error.status === 404) {
                try {
                    const notFoundRequest = new Request(
                        new URL('/404.html', request.url).toString(),
                        request
                    );
                    const notFoundResponse = await getAssetFromKV(
                        {
                            request: notFoundRequest,
                            waitUntil: ctx.waitUntil.bind(ctx),
                        },
                        {
                            cacheControl: {
                                browserTTL: 3600,
                                edgeTTL: 86400,
                            },
                        }
                    );

                    // 确保 404 页面也使用 UTF-8
                    const headers = new Headers(notFoundResponse.headers);
                    headers.set('Content-Type', 'text/html; charset=utf-8');

                    return new Response(notFoundResponse.body, {
                        status: 404,
                        statusText: 'Not Found',
                        headers: headers,
                    });
                } catch (e) {
                    return new Response('404 Not Found', {
                        status: 404,
                        headers: {
                            'Content-Type': 'text/html; charset=utf-8',
                        },
                    });
                }
            }

            // 其他错误
            return new Response(`Error: ${error.message}`, {
                status: error.status || 500,
                headers: {
                    'Content-Type': 'text/plain; charset=utf-8',
                },
            });
        }
    },
};
