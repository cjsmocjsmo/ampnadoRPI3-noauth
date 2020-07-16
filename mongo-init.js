#!/bin/bash


db.auth('admin-user', 'admin-password')

// db2 = db.getSiblingDB('ampnadoDB')
// db3 = db.getSiblingDB('ampviewsDB')
// db4 = db.getSiblingDB('picDB')

db.createUser({
  user: 'pi',
  pwd: 'piword',
  roles: [
    {
      role: 'userAdminAnyDatabase',
      db: 'admin',
    },
  ],
});
