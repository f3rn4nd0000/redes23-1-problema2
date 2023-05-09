#redes23-1-problema2

Esse repositório contem a solução para o Problema 2 da disciplina TEC502 no semestre 23.1, a solução implementa uma aplicação
de redes usando o protocolo MQTT para simular a comunicação entre estações de abastecimento de veículos elétricos e os veículos,
usando um broker e servidores distribuídos com o objetivo de reduzir a latência na comunicação entre os dispositivos e reduzir o tempo
de espera para que um veículo recarregue sua bateria.

The problem consists of designing and implementing a client-server application that allows clients to send messages to the server, which then broadcasts the messages to all connected clients. The server should be able to handle multiple concurrent connections and ensure that each client receives all the messages.
Repository Structure

A estrutura do projeto é orgainzada como:

├── requirements.txt (Contém dependencias usadas no projeto, veja mais detalhes abaixo)
├── servidor_central
│   ├── Dockerfile
│   ├── requirements.txt
│   └── servidor_central.py
├── station
│   ├── Dockerfile
│   ├── requirements.txt
│   └── station.py
├── vehicle
│   ├── Dockerfile
│   ├── requirements.txt
│   └── vehicle.py

    servidor_central.py: Esse arquivo é responsável por gerenciar as comunicações entre veiculos e postos, aumentando e reduzindo as filas e gerenciando
    qual posto possui a menor fila para mostrar para os veiculos

    station.py: Representa a classe posto, que é responsável por publicar as mensagens informando a sua localização e tamanho da fila. 

    vehicle.py: Representa a classe veículo, essa classe publica as mensagens contendo localização do veículo e 

Executando a aplicação:

    Clone the repository:

    bash

Antes de mais nada é necessário rodar um broker localmente, ou usar um serviço remoto, caso opte pela
segunda opção veja [EMQX](https://www.emqx.com/en/blog/how-to-use-mqtt-in-python)


git clone https://github.com/f3rn4nd0000/redes23-1-problema2.git

Navigate to the repository's directory:

bash

cd redes23-1-problema2

Execute em ordem

bash

python servidor_central.py
python

The server will start listening for client connections on the default port (e.g., localhost:8000).

Open a new terminal window/tab and start a client session by running the following command:

bash

    python client.py

    The client will connect to the server and prompt you to enter a message.

    Enter a message in the client terminal and press Enter to send it to the server. The server will broadcast the message to all connected clients.

    You can open additional client sessions in separate terminal windows/tabs by running the client.py script again. All clients will receive messages broadcasted by the server.

Notes

    By default, the server listens on localhost (loopback interface) on port 8000. If you want to change these settings, you can modify the server.py file accordingly.

    The client application assumes that the server is running on the same machine. If you want to connect to a server running on a different machine, you need to modify the client.py file and provide the appropriate IP address or hostname of the server.

    This application is a basic implementation for educational purposes. It may not handle all possible edge cases or have robust error handling. Use it as a starting point for learning and experimentation.

License

The code in this repository is licensed under the MIT License. Feel free to use and modify it as per the license terms.
