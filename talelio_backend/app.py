from talelio_backend import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
