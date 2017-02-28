// initialize debugger
const electronics = require('./electronics.es6');
const debug = require('./debugger.es6');
const initDebug = debug.init('init');
initDebug('Debugger initialized!');
initDebug('Checking node arguments:');
initDebug(`VEBOSE  - ${process.env.VEBOSE}`);
initDebug(`LOCAL  - ${process.env.LOCAL}`);
initDebug(`ALARM  - ${process.env.ALARM}`);

// Incorporate dependencies
const path = require('path');
const bodyParser = require('body-parser');
const express = require('express');
const cookieParser = require('cookie-parser');
const session = require('cookie-session');
const app = express();
const users = require('express-users');  // FYI: Needs modified version
const secret = require('./secret.json');

module.exports = {
  run(_dirname) {
    // This is already set with /register from express-routers,
    //    so not sure what this does:
    initDebug(`Dirname = ${_dirname}/data/users`);
    const userRouter = users({
      store: 'nedb',
      nedb: { filename: `${_dirname}/data/users` },
      data: [
        { username: secret.username, pwd: secret.pwd, email: secret.email},
      ],
    });

    // Configure the app port, etc.
    app.set('port', 3000);
    app.use(express.static('dist'));
    app.use(bodyParser.urlencoded({ extended: false }));
    app.use(cookieParser());
    app.use(session({
      resave: false,
      saveUninitialized: false,
      secret: secret.passport,
    }));
    app.use(userRouter.passport.initialize());
    app.use(userRouter.passport.session());
    app.use(userRouter);

    /**
     * Set Routes
     */

    // Main routes:
    app.get('/', (req, res) => {
      if (req.isAuthenticated())
        return res.redirect('/app');
      return res.sendFile(path.resolve(`${_dirname}/views/login.html`));
    });
    app.get('/app', (req, res) => {
      if (req.isAuthenticated() && req.user.username === secret.username) {
        initDebug(`User (${secret.username}) logged in to /app`);
        return res.sendFile(path.resolve(`${_dirname}/views/index.html`));
      }
      return res.sendFile(path.resolve(`${_dirname}/views/login.html`));
    });

    // Maker requests:
    app.get(`/${secret.maker}/:id`, (req, res) => {
      const id = req.params.id
      if (id === 'enter' || id === 'exit') {
        electronics.send(`[status] @>arg:>>${id}`);
        const filepath = path.resolve(`${_dirname}/views/${id}.html`);
        return res.sendFile(filepath);
      }
      initDebug(`Param not enter or exit: ${req.params.id}`);
      return res.sendFile(path.resolve(`${_dirname}/views/404.html`));
    });

    return app;
  },
};
