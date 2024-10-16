/**
 * source: Create React App Documentation
 * link: https://create-react-app.dev/docs/proxying-api-requests-in-development/
 * date: October 15, 2024
 */

const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/api',
    createProxyMiddleware({
      target: 'http://localhost:8000',
      changeOrigin: true,
    })
  );
};
