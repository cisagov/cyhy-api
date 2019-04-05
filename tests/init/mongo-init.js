db = db.getSiblingDB("cyhy");

db.createUser({
  user: "api-server",
  pwd: "example",
  roles: [
    {
      role: "readWrite",
      db: "cyhy"
    }
  ]
});

// password: foobar
db.users.insert({
  email: "foo@bar.gov",
  password: "$2b$12$vsQwMGt6iHQY.wBqQpWDNuVf6EjXwPH28OvYtQ2.6iKuWYw2tMLLq"
});
