# GDS3710 → Nx Witness/Wisenet Wave Integration

Este projeto implementa um servidor HTTP em Python para integração entre o vídeo porteiro Grandstream **GDS3710** e o sistema de monitoramento **Nx Witness** (ou **Hanwha Wisenet Wave**), disparando eventos manuais na VMS sempre que o GDS enviar notificações de chamada ("doorbell call").

## 📋 Visão geral

- Recebe notificações do GDS3710 via HTTP POST.
- Autentica-se automaticamente na API REST do Nx Witness para obtenção de token JWT.
- Envia evento manual para o Nx Witness, referenciando a câmera correspondente.
- Integração desenhada para redes locais (LAN). Variáveis sensíveis via `.env`.

---

## 🚀 Como funciona

1. **Servidor HTTP** escuta na porta `7777` aguardando POST do GDS3710.
2. Ao receber um POST com `content=Call Log(Door Bell Call)`, aciona o envio do evento.
3. Se necessário, realiza autenticação na API REST `/rest/v3/login/sessions` do Nx Witness.
4. Envia evento para `/api/createEvent` autenticado via Bearer Token.

---

## 🛠️ Pré-requisitos

- Python 3.8+
- Grandstream GDS3710 configurado para notificar eventos por HTTP.
- Nx Witness (ou Wisenet Wave) com API REST ativada.
- Instalar dependências:

```bash
pip install requests python-dotenv
