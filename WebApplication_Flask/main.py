from website import create_app

app = create_app()

# Now we want our webserver to run only when we go through the website package. Hence, we will put the if condition below
if __name__ == '__main__':
    app.run(debug=True) # We use Debug =True in order to re run the web server everytime we make any change in the python code
