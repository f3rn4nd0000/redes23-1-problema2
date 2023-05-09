# redes23-1-problema2

Esse repositório contem a solução para o Problema 2 da disciplina TEC502 no semestre 23.1, a solução implementa uma aplicação
de redes usando o protocolo MQTT para simular a comunicação entre estações de abastecimento de veículos elétricos e os veículos,
usando um broker e servidores distribuídos com o objetivo de reduzir a latência na comunicação entre os dispositivos e reduzir o tempo
de espera para que um veículo recarregue sua bateria.

A estrutura do projeto é orgainzada como:
```
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
```

servidor_central.py: Esse arquivo é responsável por gerenciar as comunicações entre veiculos e postos, aumentando e reduzindo as filas e gerenciando
qual posto possui a menor fila para mostrar para os veiculos

station.py: Representa a classe posto, que é responsável por publicar as mensagens informando a sua localização e tamanho da fila. 

vehicle.py: Representa a classe veículo, essa classe publica as mensagens contendo localização do veículo e 

Executando a aplicação:

Antes de mais nada é necessário rodar um broker localmente, ou usar um serviço remoto, caso opte pela
segunda opção veja [EMQX](https://www.emqx.com/en/blog/how-to-use-mqtt-in-python)


```
git clone https://github.com/f3rn4nd0000/redes23-1-problema2.git
```

Navegue para a pasta raíz do repositório:

```
cd redes23-1-problema2
```
Execute em ordem

```
python3 servidor_central.py
python3 station.py (Execute quantas vezes quiser)
python3 vehicle.py (Execute quantas vezes quiser)
```

