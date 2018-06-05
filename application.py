from application import create_app
# # from vendor import application
#
application = create_app()
#
# # application.run(host='0.0.0.0', port=5001, debug=True)
#
if __name__ == '__main__':
    # application.run(host='0.0.0.0')
    application.run(debug=True)
# # app.run(host='0.0.0.0', port=5001, debug=True)