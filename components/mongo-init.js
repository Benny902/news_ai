db.createUser({
    user: 'admin',
    pwd: 'password',
    roles: [
        {
            role: 'readWrite',
            db: 'user_db'
        }
    ]
});

db.createCollection('users');
