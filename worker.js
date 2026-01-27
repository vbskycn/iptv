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
            // 文件会被上传到 CF 的 KV 存储，全球边缘节点缓存
            return await getAssetFromKV(
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
                    // 自定义 MIME 类型
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
        } catch (error) {
            // 如果文件不存在，尝试返回 404 页面
            if (error.status === 404) {
                try {
                    const notFoundRequest = new Request(
                        new URL('/404.html', request.url).toString(),
                        request
                    );
                    return await getAssetFromKV(
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
