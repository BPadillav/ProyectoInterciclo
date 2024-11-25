from backend.app import create_app

app = create_app()

if __name__ == '__main__':
    # Ejecuta la aplicación con soporte para HTTPS
    app.run(
        host='0.0.0.0', 
        port=5000, 
        debug=True, 
        ssl_context=('cert.pem', 'key.pem')  # Ruta a los archivos generados
    )
