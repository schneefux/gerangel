const dotenv = require('dotenv')
dotenv.config()

module.exports = {
  apps: [{
    name: 'web',
    port: 7990,
    script: './node_modules/nuxt/bin/nuxt.js',
    args: 'start',
    cwd: './web/',
    watch: false,
    exec_mode: 'cluster_mode',
    instances: 'max',
    env: {
      'NODE_ENV': 'production',
      /* server to server calls - frontend configuration is set during build */
      'API_PORT': 7991,
    },
  }, {
    name: 'api',
    port: 7991,
    script: './manage.py',
    args: 'runserver 0.0.0.0:7991',
    watch: false,
    exec_mode: 'fork',
    exec_interpreter: 'python3',
  }],
  deploy: {
    production: {
      key: process.env.PROD_SSHKEY,
      user: process.env.PROD_USER,
      host: process.env.PROD_HOST,
      ref: 'origin/master',
      repo: 'https://github.com/schneefux/gerangel',
      path: process.env.PROD_PATH,
      'post-setup':
        'echo SECRET_KEY=\'' + Math.floor(Math.random() * 10e12) + '\' >> gerangel/secrets.py',
      'post-deploy':
        'pip3 install -r requirements.txt && ' +
        'python3 manage.py migrate && ' +
        'cd web && ' +
        'npm install && ' +
        'export API_URL_BROWSER=\'' + process.env.PROD_APIURL + '\' && ' +
        'npm run build && ' +
        'cd ../ && ' +
        'npm i dotenv && ' +
        'ln -s ./web/.nuxt/ .nuxt && ' +
        'pm2 startOrRestart ecosystem.config.js',
    },
  },
}
