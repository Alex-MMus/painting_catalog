Для запуска приложения: 
    sudo docker build -t painting_catalog .
    sudo docker run --rm -p 8000:8000 painting_catalog

Для тестов:
    sudo docker build -t painting_catalog_tests -f Dockerfile.tests .
    sudo docker run --rm painting_catalog_tests

    
