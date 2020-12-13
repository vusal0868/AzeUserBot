# Faster & Secure & Special Container #
# Thanks to mkaraniya & zakaryan2004

FROM Vusal/AzeUserBot:latest
RUN git clone https://github.com/vusal0868/AzeUserBot /root/AzeUserBot
WORKDIR /root/AzeUserBot/
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]  
