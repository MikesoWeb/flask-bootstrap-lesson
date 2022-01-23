from company import create_app, db, create_user

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_user()
        # disable debug mode when deploy on server
        # NO GIT push DB
        app.run(debug=True, port=5555)