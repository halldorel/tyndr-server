module.exports = function(app) {
  var router = app.loopback.Router();

  router.get('/', function(req, res) {
    res.render('index', {
      loginFailed: false
    });
  });

  router.get('/ads', function(req, res) {
    res.render('ads');
  });

  router.post('/ads', function(req, res) {
    var email = req.body.email;
    var password = req.body.password;
    app.models.User.login({
      email: email,
      password: password
    }, function(err, user) {
      if (err) {
        res.render('index', {
          email: email,
          password: password,
          loginFailed: true
        });
      } else {
        res.render('ads', {
          username: user.username,
          accessToken: user.id
        });
      }
    });
  });

  router.get('/logout', function(req, res) {
    var AccessToken = app.models.AccessToken;
    var token = new AccessToken({id: req.query.access_token});
    token.destroy();
    res.redirect('/');
  });

  app.use(router);
};