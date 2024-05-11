![](docs/assets/assets/wanderai.png)
# WanderAI - Gerador de Roteiros de Viagem com Google Gemini
## 1. Introdução
Este repositório contém um script Python que utiliza o poder do modelo de linguagem Google Gemini para gerar roteiros de viagem personalizados. Através de perguntas sobre suas preferências, o script constrói um roteiro detalhado, incluindo sugestões de atividades, restaurantes e dicas de transporte. O script está hosteado no Render e recebe os dados da chamada para o modelo através de um webapp desenvolvido com Flutter, chamado de [WanderAi](https://hugooleal.github.io/WanderAi_2.0/#/)  (o app foi desenhado tendo em mente uma tela full HD, se abrirem pelo celular já adianto que não está com a melhor responsividade 😁).
## 2. Explicação do Código
O código se divide nas seguintes etapas:
### 2.1 Instalação e Importações:
Instalamos as bibliotecas necessárias através do `requirements.txt`, incluindo nossa maravilhosa google-generativeai. Depois disso, importamos todas elas no script: google.generativeai, pandas, numpy, etc.
### 2.2 Configuração do Modelo Gemini:
Após, definimos a chave da API do Google Gemini (api_key), que está guardada secretamente no servidor do Render :shushing_face:.
Depois disso é hora de definir as configurações do nosso modelo (temperatura, top_p, top_k, max_output_tokens). Nessa etapa, criamos um dicionário contendo 3 configs diferentes cada uma com uma temperatura, sendo elas: 0.5, 0.75 e 1. Mais para frente explico o motivo. Definimos também os parâmetros de segurança para evitar conteúdo inadequado.
### 2.3 Coleta de Informações do Usuário:
Enquanto isso no nosso front-end o usuário vai informar o destino da viagem, período, tipos de atividade que gosta e seu orçamento. Com base nessas informações, o front gera um prompt baseado nas melhores práticas aprendidas durante a imersão. O prompt possui o seguinte template:
```
Você agora é um agente de viagens e possui vasta experiência sobre todos os países do mundo. Crie um roteiro de viagens para mim considerando as seguintes informações:
Destino: [Destino informado]
Duração da viagem: [Duração informada]
Tipos de atividade que mais gosto: [Tipos de atividades selecionados]
Orçamento disponível: [Orçamento informado]
Orientações para montar o roteiro:
1. Monte o roteiro detalhado para cada dia da viagem. Se for preciso, pode consolidar até no máximo 3 dias.
2. Leve em consideração a proximidade de cada atividade para montar os dias.
3. Seja específico e detalhado sobre cada dia e atividade sugerida.
4. Não repita atividades entre os dias.
5. Dê dicas importantes, como por exemplo, se há necessidade de reserva antecipada para a atividade sugerida e inclua os links de reserva quando aplicável.
6. Sugira opões de restaurantes em cada dia.
7. Dê dicas sobre o melhor meio de se locomover na cidade.
8. Informe a média do custo total da viagem com base no roteiro sugerido, em reais. Faça isso apenas ao final.
```
Com o prompt gerado e enviado para o nosso servidor, iniciamos o modelo generativo através de uma iteração entre as 3 configurações criadas nos passos acima. Dessa forma, recebemos 3 respostas diferentes para o mesmo prompt, considerando temperaturas de 0.5, 0.75 e 1. Assim conseguimos explorar diferentes níveis de criatividade.
Essa parte é a que toma mais tempo, já que estamos falando de 3 respostas relativamente grandes, então não se desespere se a tela de carregamento do aplicativo demorar um tempinho. Pode levar até 3 minutos, mas hey, você levaria mais tempo que isso para montar um roteiro do zero, não? No futuro podemos tentar melhorar isso 😄
### 2.4 Processamento das Respostas:
Em seguida, armazenamos as respostas em um DataFrame e usamos a função `embedFunction()` criada no início do código para se utilizar dos modelos de embedding do Google Gemini para gerar embeddings para cada resposta, representando seu significado semanticamente.
### 2.5 Seleção da Melhor Resposta:
Posteriormente, usamos a função `consultarMelhorResposta()`, que também foi criada no início do script, para comparar o embedding do prompt inicial com os embeddings das respostas e
selecionar a resposta com o maior produto escalar, ou seja, aquela que indica maior similaridade semântica com o prompt.
Dessa forma, aplicamos um método de autovalidação pelo próprio Gemini, combinando tanto o modelo gerador de conteúdo quanto o modelo de embedding. 
### 2.6 Apresentação da Melhor Resposta:
A melhor resposta então é retornada e exibida ao usuário no webapp responsável pelo front-end.
## 3. Conclusão
Essa aplicação demonstra o enorme potencial do Google Gemini nas mais diversas áreas que a imaginação pode chegar. A criação de roteiros de viagem personalizados e informativos é apenas uma das milhares de possibilidades. Ao ajustar as configurações do modelo e coletar informações detalhadas do usuário, o script oferece uma experiência de planejamento de viagem interativa e eficiente, de forma rápida. O aplicativo em si é bem simples, mas foi elaborado com o ojetivo de demonstrar as milhares de capacidades do Gemini.
Espero que tenham gostado!
