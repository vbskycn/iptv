/**
 * Cloudflare Worker 脚本
 * 使用 Workers Assets 直接服务静态文件
 * 文件存储在 CF 边缘网络，无需从 GitHub 代理
 */

import { getAssetFromKV } from '@cloudflare/kv-asset-handler';

// MIME 类型映射（确保文本文件使用 UTF-8）
const MIME_TYPES = {
    '.html': 'text/html; charset=utf-8',
    '.htm': 'text/html; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.js': 'application/javascript; charset=utf-8',
    '.mjs': 'application/javascript; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.xml': 'application/xml; charset=utf-8',
    '.txt': 'text/plain; charset=utf-8',
    '.m3u': 'text/plain; charset=utf-8',  // M3U 播放列表
    '.m3u8': 'application/vnd.apple.mpegurl; charset=utf-8',
    '.md': 'text/markdown; charset=utf-8',
    '.svg': 'image/svg+xml; charset=utf-8',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.webp': 'image/webp',
    '.ico': 'image/x-icon',
    '.woff': 'font/woff',
    '.woff2': 'font/woff2',
    '.ttf': 'font/ttf',
    '.eot': 'application/vnd.ms-fontobject',
};

// 获取文件扩展名对应的 MIME 类型
function getMimeType(pathname) {
    const ext = pathname.substring(pathname.lastIndexOf('.')).toLowerCase();
    return MIME_TYPES[ext] || null;
}

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

            // 修正 Content-Type，确保文本文件使用 UTF-8
            const url = new URL(request.url);
            const mimeType = getMimeType(url.pathname);

            if (mimeType) {
                // 创建新的响应，使用正确的 Content-Type
                const headers = new Headers(response.headers);
                headers.set('Content-Type', mimeType);

                return new Response(response.body, {
                    status: response.status,
                    statusText: response.statusText,
                    headers: headers,
                });
            }

            return response;

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
