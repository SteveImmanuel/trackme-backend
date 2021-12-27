from trackme import create_app

app = create_app()
app.run(debug=True, load_dotenv=True, port=5000)