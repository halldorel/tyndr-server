var debug = require('debug')('boot:create-model-instances');

module.exports = function(app) {
  var User = app.models.user;

  User.create([
    {username: 'tommi', email: 'tommi@tommi.is', password: 'tommi'}
  ], function(err, users) {
    if (err) return debug('%j', err);
    debug(users);
    //create project 1 and make john the owner
    users[0].projects.create({
      name: 'Gæludýr 1',
      lost: true,
      resolved: false,
      location: "-21.89541,64.13548",
      description: "Frekar ljótt dýr",
      reward: "500",
      created_at: new Date()
    }, function(err, project) {
      if (err) return debug(err);
      debug(project);
    });
  });
};