from app import create_app

application = create_app()

if __name__ == '__main__':
    #application.debug = True
    #application.run()
    application.run(host='0.0.0.0', port=5020, debug=True)
